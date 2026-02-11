# Lab 6: Spark ML Pipeline on Amazon EMR (Customer Churn Prediction)

This project implements an end-to-end distributed machine learning pipeline using Apache Spark on an Amazon EMR cluster. It performs feature engineering and compares Logistic Regression and Random Forest models to predict customer churn based on the Bank Customer Churn dataset.

## Setup & Run
1. Upload Dataset and Script to Master Node
From your local terminal, upload the dataset and the python script to the EMR Primary (Master) node:
```bash
scp -i vockey.pem Churn_Modelling.csv churn_pipeline.py hadoop@<MASTER_PUBLIC_DNS>:
```
2. Prepare Data in HDFS
SSH into your EMR Master node and move the dataset to the distributed file system:
```bash
hdfs dfs -mkdir -p /user/hadoop/churn_input
hdfs dfs -put Churn_Modelling.csv /user/hadoop/churn_input/
```
3. Submit Spark Job
Execute the Spark application. This job will be managed by YARN and distributed across the core nodes:
```bash
spark-submit --master yarn --deploy-mode client churn_pipeline.py
```

## System Components
* Spark Session: Initialized on the Master node to coordinate the distributed application.
* Feature Engineering Pipeline:
  * StringIndexer & OneHotEncoder: Transform categorical variables (Geography, Gender) into numerical vectors.
  * VectorAssembler: Consolidates all features (CreditScore, Age, Tenure, Balance, NumOfProducts, EstimatedSalary, and encoded vectors) into a single input vector.
  * StandardScaler: Normalizes feature scales to improve model convergence.
* Machine Learning Models:
  * Logistic Regression: Provides a linear baseline for binary classification (Exited 0 or 1).
  * Random Forest Classifier: An ensemble method used as the experimental comparison to capture non-linear patterns.
* Amazon EMR: Provides the hardware (m4.large instances) and software stack (Spark, Hadoop, YARN) for scalable execution.

## Dataset [https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling]
The data set contains details of a bank's customers and the target variable is a binary variable reflecting the fact whether the customer left the bank (closed his account) or he continues to be a customer.
* Target Variable: Exited (1 = Churn, 0 = Stayed).
* Features: Customer demographics, credit scores, account balances, and product involvement.
