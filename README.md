# Lab 5: Mini-MapReduce on Amazon EMR

This project implements a distributed WordCount pipeline using the MapReduce programming model on a managed Amazon EMR cluster. It processes a large Wikipedia text dataset stored in HDFS, demonstrating parallel execution, data distribution, and fault tolerance in a cloud environment.

## Setup & Run
1. Enter Master Node and Prepare Data in HDFS
SSH into your EMR Primary (Master) node through command or Putty and run the following to download the dataset and move it to distributed storage:
```bash
wget https://github.com/LGDoor/Dump-of-Simple-English-Wiki/raw/refs/heads/master/corpus.tgz
tar -xvzf corpus.tgz
hdfs dfs -mkdir -p /user/hadoop/input
hdfs dfs -put corpus.txt /user/hadoop/input/
```
2. Submit MapReduce Job
Execute the Hadoop Streaming job by providing the mapper and reducer scripts. This command distributes the Python files to all worker nodes:
```bash
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
  -files mapper.py,reducer.py \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py" \
  -input /user/hadoop/input/ \
  -output /user/hadoop/output/*
```
3. Verify Output
```bash
hdfs dfs -ls /user/hadoop/output/*
```

## System Components
* Mapper (mapper.py): Tokenizes the input text from sys.stdin, cleans whitespaces, and emits each word with an individual count of 1.
* Reducer (reducer.py): Utilizes a defaultdict to aggregate counts for each unique word received from the shuffle phase, ensuring all occurrences are summed before outputting the final result.
* Managed Cluster (Amazon EMR): Orchestrates execution across Primary, Core, and Task nodes, managing resource allocation via YARN.
* Fault Tolerance: The system handles node failures during the Shuffle/Reduce phase (e.g., ShuffleError). If a Task node is lost, the framework automatically re-executes the affected tasks on remaining healthy nodes.
* HDFS Storage: Uses a distributed file system to ensure data is accessible across the entire cluster for parallel processing.
## Dataset
The dataset is the content of the [Simple English Wikipedia](http://simple. wikipedia.org/) in *Plane Text*.

The whole content of this encyclopedia can be downloaded from <http://dumps.wikimedia.org/> but a preprocessed version is provided.

The format of this file is as follows: The first line is the title of the first article, while the following lines (up to the first blank line) form the content of this article, in plain text format. The second article comes after the next blank line, and so on. There are 50,441 articles in total.
