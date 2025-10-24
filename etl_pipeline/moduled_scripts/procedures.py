from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, to_date, when, regexp_extract

def extract():
    procedures_spark = SparkSession.builder.appName("Patients-ETL").config("spark.driver.memory", "512m").getOrCreate()
    procedures_data = "../../Datasets/csv/procedures.csv"
    return procedures_spark, procedures_data

def transform(procedures_spark, procedures_data):
    df = procedures_spark.read.csv(path=procedures_data, header=True, inferSchema=True)
    print("Data is loaded")

    # --- Column Renaming ---
    new_cols_list=["performed_from", "performed_till", "uuid", "urn_uuid","_","procedure_code","procedure_description","procedure_cost", "_", "procedure_observations"]

    old_cols = df.columns

    for old_col, new_col in zip(old_cols, new_cols_list):
        df = df.withColumnRenamed(old_col, new_col)
    
    df = df.drop(*[col for col in df.columns if col.startswith('_')])

    df = df.fillna({"procedure_observations": "No observations recorded (None)"})

    df = df.withColumn("procedure_type", regexp_extract(col("procedure_description"), r"\((.*?)\)$", 1)) \
       .withColumn("procedure_description", regexp_extract(col("procedure_description"), r"^(.*?)\(", 1))
    
    df = df.withColumn("observation_type", regexp_extract(col("procedure_observations"), r"\((.*?)\)$", 1)) \
       .withColumn("procedure_observations", regexp_extract(col("procedure_observations"), r"^(.*?)\(", 1))

    print(df.show(150))
    print(df.columns)

def load():
    pass

if __name__ == "__main__":
    spark_obj, path = extract()
    transform(spark_obj, path)