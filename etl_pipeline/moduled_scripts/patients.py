from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, to_date, when, split
import re

def extract():
    patients_spark = SparkSession.builder.appName("Patients-ETL").config("spark.driver.memory", "512m").getOrCreate()
    patients_data = "../../Datasets/csv/patients.csv"
    return patients_spark, patients_data

def transform(patients_spark, patients_data):
    df = patients_spark.read.csv(path=patients_data, header=True, inferSchema=True)
    print("Data is loaded")
    
    df = df.drop("_c10", "_c12","Pittsfield  Massachusetts  US", "Middlesex County")

    # print(df.columns)

    new_cols_list=["uuid", "birth_date", "death_date", "social_security_number", "driver's_license_number", "passport_number", "salutation", "first_name",
                "middle_name", "last_name", "maiden_family", "skin_color", "hispanic", "gender", "address", "city", "state", "postal_code","latitude","longitude",
                "family_income"]

    old_cols = df.columns

    for old_col, new_col in zip(old_cols, new_cols_list):
        df = df.withColumnRenamed(old_col, new_col)

    re_patterns = [r'^[-]?[0-9]+.[0-9]+$', r'[0-9]+$']
    dropped_cols = [col for col in df.columns if re.match(re_patterns[0], col)]
    df = df.drop(*dropped_cols)
    
    df = df.withColumn(

        "first_name", split(col("first_name"), pattern=re_patterns[1]).getItem(0)
    ).withColumn(
        "middle_name", split(col("middle_name"), pattern=re_patterns[1]).getItem(0)
    ).withColumn(
        "last_name", split(col("last_name"), pattern=re_patterns[1]).getItem(0)
    ).withColumn(
        "maiden_family", split(col("maiden_family"), pattern=re_patterns[1]).getItem(0)
    )

    #Fiiling NAN values now

    df = df.withColumn(

        "salutation",

        when(col("gender") == "M", "Mr.").otherwise("Ms.")

    )
    df = df.fillna({"passport_number": "N/A","maiden_family": "N/A", "middle_name": "N/A"})

    print(df.show(30))
    print(df.columns)

def load():
    pass

if __name__ == "__main__":
    spark_obj, path = extract()
    transform(spark_obj, path)