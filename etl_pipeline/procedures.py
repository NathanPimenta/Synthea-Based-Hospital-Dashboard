from pyspark.sql.functions import col, regexp_extract
from etl_pipeline.master import Master

class ProceduresETL:
    _proceduresetlInstance = None
    _master = Master()

    def __new__(cls):
        if cls._proceduresetlInstance is None:
            cls._proceduresetlInstance = super().__new__(cls)

        return cls._proceduresetlInstance

    def etl(self):
        """
        Unified Extract–Transform–Load function for procedures data.
        """
        # ✅ Check cache — no reprocessing if already loaded
        if self._master.getDataframes("procedures"):
            print("Procedures dataframe already loaded in singleton cache.")
            return self._master.getDataframes("procedures")

        # --- Extract ---
        path = "../Datasets/csv/procedures.csv"
        spark = self._master._master_spark
        df = spark.read.csv(path, header=True, inferSchema=True)
        print("✅ Extract: Procedures data loaded")

        # --- Transform ---
        new_cols_list = [
            "performed_from", "performed_till", "uuid", "urn_uuid", "_",
            "procedure_code", "procedure_description", "procedure_cost", "_",
            "procedure_observations"
        ]

        for old_col, new_col in zip(df.columns, new_cols_list):
            df = df.withColumnRenamed(old_col, new_col)

        # Drop placeholder columns starting with '_'
        df = df.drop(*[c for c in df.columns if c.startswith('_')])

        # Fill missing observations
        df = df.fillna({"procedure_observations": "No observations recorded (None)"})

        # Extract description & type info
        df = df.withColumn("procedure_type", regexp_extract(col("procedure_description"), r"\((.*?)\)$", 1)) \
               .withColumn("procedure_description", regexp_extract(col("procedure_description"), r"^(.*?)\(", 1))

        df = df.withColumn("observation_type", regexp_extract(col("procedure_observations"), r"\((.*?)\)$", 1)) \
               .withColumn("procedure_observations", regexp_extract(col("procedure_observations"), r"^(.*?)\(", 1))

        print("✅ Transform: Procedures columns cleaned and enriched")

        # --- Load ---
        self._master.setDataframes("procedures", df)
        print("✅ Load: Procedures dataframe stored in ETLSingleton")

        # return df


# Optional: Standalone execution
# if __name__ == "__main__":
#     proc_etl = ProceduresETL()
#     df_proc = proc_etl.etl()
#     df_proc.show(25)
#     print("Columns:", df_proc.columns)
