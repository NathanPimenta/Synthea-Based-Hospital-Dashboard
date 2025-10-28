# conditions_etl.py
from pyspark.sql.functions import col, to_date, regexp_extract
from master import Master

class ConditionsETL:

    _conditionsetlInstance = None
    _master = Master()

    def __new__(cls):
        
        if cls._conditionsetlInstance is None:
            cls._conditionsetlInstance = super().__new__(cls)

        return cls._conditionsetlInstance

    def etl(self):
        """
        Load the transformed conditions DataFrame from CSV if not already loaded.
        """

        path="../Datasets/csv/conditions.csv"
        
        df = self._master._master_spark.read.csv(path, header=True, inferSchema=True)
        new_cols_list = ["event_start", "event_end", "uuid", "record_id", "_", "event_code", "event_description"]

        for old_col, new_col in zip(df.columns, new_cols_list):
            df = df.withColumnRenamed(old_col, new_col)

        # Drop placeholder columns
        df = df.drop(*[col for col in df.columns if col.startswith('_')])

        # Convert date columns to proper date format
        df = df.withColumn("event_start", to_date(col("event_start"), "yyyy-MM-dd")) \
               .withColumn("event_end", to_date(col("event_end"), "yyyy-MM-dd"))

        # Extract event type from description
        df = df.withColumn("event_type", regexp_extract(col("event_description"), r"\((.*?)\)$", 1)) \
               .withColumn("event_description", regexp_extract(col("event_description"), r"^(.*?)\(", 1))

        # Store in singleton
        self._master.setDataframes("conditions", df)
    

# Optional: Standalone execution
# if __name__ == "__main__":
#     conditions_etl = ConditionsETL()
#     df_proc = conditions_etl.etl()
#     df_proc.show(10)
#     print("Columns:", df_proc.columns)