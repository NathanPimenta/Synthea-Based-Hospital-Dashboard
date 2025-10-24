# patients_etl.py
from pyspark.sql.functions import col, when, split
from etl_pipeline.master import Master
import re

class PatientsETL:

    __patientsetInstance = None
    __master = Master()

    def __new__(cls):
        if cls.__patientsetInstance is None:
            cls.__patientsetInstance = super().__new__(cls)

        return cls.__patientsetInstance

    def etl(self):
        """
        Load the transformed patients DataFrame from CSV if not already loaded.
        """

        path="../../Datasets/csv/patients.csv"
        df = self.__master._master_spark.read.csv(path, header=True, inferSchema=True)
        print("Data is loaded")

        # Drop unwanted columns
        df = df.drop("_c10", "_c12","Pittsfield  Massachusetts  US", "Middlesex County")

        # Rename columns
        new_cols_list = ["uuid", "birth_date", "death_date", "social_security_number", "driver's_license_number", 
                         "passport_number", "salutation", "first_name", "middle_name", "last_name", "maiden_family",
                         "skin_color", "ancestry", "gender", "address", "city", "state", "postal_code", "latitude",
                         "longitude", "family_income"]

        for old_col, new_col in zip(df.columns, new_cols_list):
            df = df.withColumnRenamed(old_col, new_col)

        # Drop numeric-looking column names
        re_patterns = [r'^[-]?[0-9]+.[0-9]+$', r'[0-9]+$']
        dropped_cols = [col for col in df.columns if re.match(re_patterns[0], col)]
        df = df.drop(*dropped_cols)

        # Clean first, middle, last, maiden names
        df = df.withColumn("first_name", split(col("first_name"), re_patterns[1]).getItem(0)) \
               .withColumn("middle_name", split(col("middle_name"), re_patterns[1]).getItem(0)) \
               .withColumn("last_name", split(col("last_name"), re_patterns[1]).getItem(0)) \
               .withColumn("maiden_family", split(col("maiden_family"), re_patterns[1]).getItem(0))

        # Fill missing values
        df = df.withColumn("salutation", when(col("gender") == "M", "Mr.").otherwise("Ms.")) \
               .fillna({"passport_number": "N/A", "maiden_family": "N/A", "middle_name": "N/A"})

        # Store in singleton
        self.__master.setDataframes("patients", df)