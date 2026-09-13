# import reader, transformer, writer, logging
# from pyspark.sql import SparkSession

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
# )

# logger = logging.getLogger(__name__)

# def main():

#     spark = (
#         SparkSession.builder
#         .appName("TradeCorp ETL")
#         .getOrCreate()
#     )

#     try:

#         logger.info("Début du pipeline TradeCorp")

#         logger.info("Etape 1 lecture des données")
#         data = reader.read_data(spark)


#     dataframes = reader.read_data()

#     df_enriched = transformer.build_enriched(dataframes)

#     writer.write_clean(df_enriched)

# if __name__ == "__main__":
#     main()