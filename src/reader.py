from utils import download_from_blobstorage

BLOBS = [
    "categories.csv",
    "customers.csv",
    "employees.csv",
    "order_details.csv",
    "orders.csv",
    "products.csv",
    "shippers.csv", 
    "suppliers.csv"
]

def read_data(spark):
    dataframes = {}

    for blob in BLOBS:
        name = blob.replace(".csv", "")

        dataframes[name] = (
            spark.read
            .option("header", True)
            .option("inferSchema", True)
            .csv(str(download_from_blobstorage(blob)))
        )

        print(blob)

    return dataframes
