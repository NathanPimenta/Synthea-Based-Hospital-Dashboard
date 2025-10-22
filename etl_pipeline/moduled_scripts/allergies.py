from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, to_date, when

def extract():
    allergies_spark = SparkSession.builder.appName("Allergies-ETL").config("spark.driver.memory", "512m").getOrCreate()
    allergies_data = "../../Datasets/csv/allergies.csv"
    return allergies_spark, allergies_data

def transform(allergies_spark, allergies_data):
    df = allergies_spark.read.csv(path=allergies_data, header=True, inferSchema=True)
    print("Data is loaded")

    new_cols_list=["uuid", "birth_date", "death_date", "social_security_number", "driver's_license_number", "passport_number", "salutation", "first_name",
                "middle_name", "last_name", "marital_status", "skin_color", "hispanic", "gender", "address", "city", "state", "postal_code","latitude","longitude",
                "family_income"]

    old_cols = df.columns

    for old_col, new_col in zip(old_cols, new_cols_list):
        df = df.withColumnRenamed(old_col, new_col)

    df = df.withColumn(
        "marital_status",
        when(col("marital_status") == "S", "Not married")
        .otherwise("Married")
    )

    print(df.show(5))
    print(df.columns)

def load():
    pass

if __name__ == "__main__":
    spark_obj, path = extract()
    transform(spark_obj, path)