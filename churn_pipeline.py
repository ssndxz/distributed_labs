from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# 1. Initialize Spark session
spark = SparkSession.builder.appName("CustomerChurnPipeline").getOrCreate()

# 2. Load dataset from HDFS
data = spark.read.csv("hdfs:///user/hadoop/churn_input/Churn_Modelling.csv", header=True, inferSchema=True)

# 3. Data Cleaning
data = data.na.drop()  

# 4. Feature Engineering
geo_indexer = StringIndexer(inputCol="Geography", outputCol="GeographyIndex")
gender_indexer = StringIndexer(inputCol="Gender", outputCol="GenderIndex")

encoder = OneHotEncoder(
    inputCols=["GeographyIndex", "GenderIndex"],
    outputCols=["GeographyVec", "GenderVec"]
)

assembler = VectorAssembler(
    inputCols=[
        "CreditScore", "Age", "Tenure", "Balance",
        "NumOfProducts", "EstimatedSalary",
        "GeographyVec", "GenderVec"
    ],
    outputCol="features"
)

scaler = StandardScaler(
    inputCol="features",
    outputCol="scaledFeatures"
)

# 5. Split data
train_data, test_data = data.randomSplit([0.8, 0.2], seed=42)

# --- EXPERIMENT: MODEL COMPARISON ---
lr = LogisticRegression(labelCol="Exited", featuresCol="scaledFeatures")

rf = RandomForestClassifier(labelCol="Exited", featuresCol="scaledFeatures", numTrees=20)

# 6. Create Pipelines
pre_processing_stages = [geo_indexer, gender_indexer, encoder, assembler, scaler]

# Pipeline 1: Logistic Regression
pipeline_lr = Pipeline(stages=pre_processing_stages + [lr])
model_lr = pipeline_lr.fit(train_data)
predictions_lr = model_lr.transform(test_data)

# Pipeline 2: Random Forest
pipeline_rf = Pipeline(stages=pre_processing_stages + [rf])
model_rf = pipeline_rf.fit(train_data)
predictions_rf = model_rf.transform(test_data)

# 7. Comprehensive Model Evaluation
def evaluate(predictions, model_name):
    evaluator = MulticlassClassificationEvaluator(labelCol="Exited", predictionCol="prediction")
    
    accuracy = evaluator.evaluate(predictions, {evaluator.metricName: "accuracy"})
    precision = evaluator.evaluate(predictions, {evaluator.metricName: "weightedPrecision"})
    recall = evaluator.evaluate(predictions, {evaluator.metricName: "weightedRecall"})
    f1 = evaluator.evaluate(predictions, {evaluator.metricName: "f1"})
    
    print(f"\n{'*' * 10} {model_name} Performance {'*' * 10}")
    print(f"Accuracy:  {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")

evaluate(predictions_lr, "Logistic Regression")
evaluate(predictions_rf, "Random Forest")

spark.stop()