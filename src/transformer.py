#from pyspark.sql import SparkSession
from pyspark.sql.functions import trim, upper, initcap, when, round, col, concat, lit
from utils import RAW_DATA_DIR

#spark = SparkSession.builder.appName("TradeCorp ETL").getOrCreate()

# df_categories = spark.read.csv(f"{RAW_DATA_DIR}/categories.csv", header=True, inferSchema=True)
# df_customers = spark.read.csv(f"{RAW_DATA_DIR}/customers.csv", header=True, inferSchema=True)
# df_employees = spark.read.csv(f"{RAW_DATA_DIR}/employees.csv", header=True, inferSchema=True)
# df_order_details = spark.read.csv(f"{RAW_DATA_DIR}/order_details.csv", header=True, inferSchema=True)
# df_orders = spark.read.csv(f"{RAW_DATA_DIR}/orders.csv", header=True, inferSchema=True)
# df_products = spark.read.csv(f"{RAW_DATA_DIR}/products.csv", header=True, inferSchema=True)
# df_shippers = spark.read.csv(f"{RAW_DATA_DIR}/shippers.csv", header=True, inferSchema=True)
# df_suppliers = spark.read.csv(f"{RAW_DATA_DIR}/suppliers.csv", header=True, inferSchema=True)

# dataframes = {
#     "categories": df_categories,
#     "customers": df_customers,
#     "employees": df_employees,
#     "order_details": df_order_details,
#     "orders": df_orders,
#     "products": df_products,
#     "shippers": df_shippers,
#     "suppliers": df_suppliers
# }

def clean_customers(df):
    return (
        df.withColumn("company_name", trim(col("company_name")))
        .withColumn("contact_name", initcap(trim(col("contact_name"))))
        .withColumn("country", upper(trim(col("country"))))
        .dropDuplicates(["customer_id"])
    )

def clean_orders(df):
    return (
        df
        .withColumn("order_date", col("order_date").cast("date"))
        .withColumn("required_date", col("required_date").cast("date"))
        .withColumn("shipped_date", col("shipped_date").cast("date"))
        .withColumn("freight", col("freight").cast("float"))
        .withColumnRenamed("ship_via", "shipper_id")
        .withColumn("is_shipped",
                    when(col("shipped_date").isNotNull(), True)
                    .otherwise(False)
        )
        .dropna(subset=["shipped_date"])
    )

def clean_order_details(df):
    return (
        df.withColumn("unit_price", col("unit_price").cast("float"))
        .withColumn("quantity", col("quantity").cast("int"))
        .withColumn("discount", col("discount").cast("float"))
        .withColumnRenamed("unit_price", "prix_unitaire")
        .withColumnRenamed("quantity", "quantite")
    )

def add_sous_total(df):
    return df.withColumn(
        "sous_total", 
        round((
            col("prix_unitaire") 
            * col("quantite") 
            * (1 - col("discount"))), 
            2
        )
    )

def clean_employees(df):
    return df.select(
        "employee_id", 
        "last_name", 
        "first_name", 
        "title", "hire_date", 
        "address", 
        "city", 
        "country"
    )

def clean_products(df):
    return (
        df
        .withColumn("unit_price", col("unit_price").cast("float"))
        .withColumn(
            "en_stock", 
            when(col("units_in_stock") > 0, True)
            .otherwise(False)
        )
    )

def build_enriched(dataframes):

    # df_customers = dataframes["customers"]
    # df_orders = dataframes["orders"]
    # df_order_details = dataframes["order_details"]
    # df_products = dataframes["products"]
    # df_categories = dataframes["categories"]
    # df_employees = dataframes["employees"]
    # df_shippers = dataframes["shippers"]
    # df_suppliers = dataframes["suppliers"]

    # df_customers = clean_customers(df_customers)
    # df_orders = clean_orders(df_orders)
    # df_order_details = clean_order_details(df_order_details)
    # df_order_details = add_sous_total(df_order_details)
    # df_products = clean_products(df_products)
    # df_employees = clean_employees(df_employees)

    df_customers = clean_customers(
        dataframes["customers"]
    )

    df_orders = clean_orders(
        dataframes["orders"]
    )

    df_order_details = clean_order_details(
        add_sous_total(
        dataframes["order_details"]
        )
    )

    df_products = clean_products(
        dataframes["products"]
    )

    df_employees = clean_employees(
        dataframes["employees"]
    )

    df_products = df_products.join(
        df_categories, 
        on="category_id", 
        how="left"
    )
    df_enriched = df_order_details.join(
        df_orders, 
        df_order_details.order_id == df_orders.order_id,
        "left"
    ).join(
        df_customers,
        df_orders.customer_id == df_customers.customer_id,
        "left"
    ).join(
        df_products,
        df_order_details.product_id == df_products.product_id,
        "left"
    ).join(
        df_employees,
        df_orders.employee_id == df_employees.employee_id,
        "left"
    ).join(
        df_shippers,
        df_orders.shipper_id == df_shippers.shipper_id,
        "left"
    )

    return df_enriched

df_enriched = build_enriched(dataframes)

df_enriched.printSchema()