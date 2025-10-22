from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, trim, to_date, when

def extract():
    procedures_spark = SparkSession.builder.appName("Patients-ETL").config("spark.driver.memory", "512m").getOrCreate()
    procedures_data = "../../Datasets/csv/patients.csv"
    return procedures_spark, procedures_data

def transform(procedures_spark, procedures_data):
    df = procedures_spark.read.csv(path=procedures_data, header=True, inferSchema=True)
    print("Data is loaded")

    new_cols_list=["uuid", "birth_date", "death_date", "social_security_number", "driver's_license_number", "passport_number", "salutation", "first_name",
                "middle_name", "last_name", "marital_status", "skin_color", "hispanic", "gender", "address", "city", "state", "postal_code","latitude","longitude",
                "family_income"]

    old_cols = df.columns

    for old_col, new_col in zip(old_cols, new_cols_list):
        df = df.withColumnRenamed(old_col, new_col)

    print(df.show(5))
    print(df.columns)

def load():
    pass

if __name__ == "__main__":
    spark_obj, path = extract()
    transform(spark_obj, path)