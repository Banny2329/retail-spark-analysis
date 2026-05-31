from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, month, sum, count

# 初始化 Spark
spark = SparkSession.builder \
    .appName("RetailAnalysis") \
    .master("local[*]") \
    .getOrCreate()

# 读取数据
df = spark.read.csv(
    "OnlineRetail.csv",
    header=True,
    inferSchema=True,
    encoding="ISO-8859-1"
)

# 查看数据基本信息
print("=== 数据总行数 ===")
print(df.count())
print("\n=== 数据前5行 ===")
df.show(5)

# 数据清洗
df_clean = df.filter(
    (col("Quantity") > 0) &
    (col("UnitPrice") > 0) &
    (col("CustomerID").isNotNull()) &
    (~col("InvoiceNo").startswith("C"))
)
print("\n=== 清洗后数据行数 ===")
print(df_clean.count())

# 业务分析：月度销售额统计
df_clean = df_clean.withColumn("InvoiceDate", to_timestamp("InvoiceDate", "dd/MM/yyyy HH:mm"))
df_clean = df_clean.withColumn("TotalPrice", col("Quantity") * col("UnitPrice"))

print("\n=== 月度销售额统计 ===")
df_clean.withColumn("month", month("InvoiceDate")) \
    .groupBy("month") \
    .agg(
        sum("TotalPrice").alias("total_sales"),
        count("InvoiceNo").alias("order_count")
    ) \
    .orderBy("month") \
    .show()

spark.stop()