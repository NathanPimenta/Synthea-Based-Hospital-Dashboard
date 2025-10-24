from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, to_date, when, regexp_extract

def extract():
    conditions_spark = SparkSession.builder.appName("Conditions-ETL").config("spark.driver.memory", "512m").getOrCreate()
    conditions_data = "../../Datasets/csv/conditions.csv"
    return conditions_spark, conditions_data

def transform(conditions_spark, conditions_data):
    df = conditions_spark.read.csv(path=conditions_data, header=True, inferSchema=True)
    print("Data is loaded")


    new_cols_list=["event_start", "event_end", "uuid", "record_id", "_", "event_code", "event_description"]

    old_cols = df.columns

    for old_col, new_col in zip(old_cols, new_cols_list):
        df = df.withColumnRenamed(old_col, new_col)

    df = df.drop(*[col for col in df.columns if col.startswith('_')])

    #Converting date columns to proper date format
    df = df.withColumn("event_start", to_date(col("event_start"), format="yyyy-MM-dd")).withColumn("event_end", to_date(col("event_end"), format="yyyy-MM-dd"))

    df = df.withColumn("event_type", regexp_extract(col("event_description"), r"\((.*?)\)$", 1)) \
       .withColumn("event_description", regexp_extract(col("event_description"), r"^(.*?)\(", 1))
    
    print(df.show(7))
    print(df.columns)

    # ---- Done with the ETL for conditions ---

def load():
    pass

if __name__ == "__main__":
    spark_obj, path = extract()
    transform(spark_obj, path)