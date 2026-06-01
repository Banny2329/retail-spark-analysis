# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, count, desc
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------------- 初始化环境（只加，不改你原来的逻辑） ----------------------
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid")

# 自动创建 output 文件夹（和你 README 项目结构一致）
if not os.path.exists("output"):
    os.makedirs("output")

# 初始化 SparkSession（和你原来的完全一致）
spark = SparkSession.builder \
    .appName("RetailAnalysis") \
    .master("local[*]") \
    .getOrCreate()

# ---------------------- 1. 数据加载与清洗（完全和 README 描述一致） ----------------------
df = spark.read.csv(
    "OnlineRetail.csv",
    header=True,
    inferSchema=True,
    encoding="ISO-8859-1"
)

# 过滤空值、异常值（和 README 描述的“过滤空值、负数量、负价格”完全一致）
df_clean = df.filter(
    (col("Quantity") > 0) &
    (col("UnitPrice") > 0) &
    (col("CustomerID").isNotNull()) &
    (~col("InvoiceNo").startswith("C"))
)

print("=== 数据总行数 ===")
print(df.count())
print("\n=== 清洗后有效数据量 ===")
print(df_clean.count())  # 会输出 397884，和你 README 写的完全一样

# 计算订单金额（为可视化做准备，不影响原有统计）
df_clean = df_clean.withColumn("Amount", col("Quantity") * col("UnitPrice"))

# ---------------------- 2. 统计分析（完全覆盖 README 所有点） ----------------------
# 1）订单总量、用户数
print("\n=== 订单总量与用户数 ===")
print("订单总量：", df_clean.select("InvoiceNo").distinct().count())
print("用户数：", df_clean.select("CustomerID").distinct().count())

# 2）国家分布（和 README 描述一致）
country_dist = df_clean.groupBy("Country").count().orderBy(desc("count")).limit(10)
print("\n=== 订单国家分布 TOP10 ===")
country_dist.show()

# 3）热门商品销量排行（和 README 描述一致）
top_products = df_clean.groupBy("StockCode", "Description") \
    .agg(count("*").alias("TotalQuantity")) \
    .orderBy(desc("TotalQuantity")) \
    .limit(10)
print("\n=== 热门商品销量 TOP10 ===")
top_products.show()

# 4）客户消费金额与频次分析（和 README 描述一致）
customer_analysis = df_clean.groupBy("CustomerID") \
    .agg(
        spark_sum("Amount").alias("TotalSpent"),
        count("InvoiceNo").alias("OrderCount")
    ).orderBy(desc("TotalSpent")).limit(10)
print("\n=== 高价值客户 TOP10 ===")
customer_analysis.show()

# ---------------------- 3. 新增可视化（和项目亮点“结果清晰易读”匹配） ----------------------
# 图1：订单国家分布（条形图，和 README 里的“国家分布”对应）
pdf_country = country_dist.toPandas()
plt.figure(figsize=(12, 6))
sns.barplot(data=pdf_country, x="Country", y="count", color="#3498db")
plt.title("Order Distribution by Country (Top 10)", fontsize=16)
plt.xlabel("Country")
plt.ylabel("Order Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/country_distribution.png", dpi=300)
plt.close()

# 图2：热门商品销量（条形图，和 README 里的“热门商品排行”对应）
pdf_prod = top_products.toPandas()
plt.figure(figsize=(12, 6))
sns.barplot(data=pdf_prod, x="Description", y="TotalQuantity", color="#e74c3c")
plt.title("Top 10 Products by Sales Volume", fontsize=16)
plt.xlabel("Product Description")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("output/top_products.png", dpi=300)
plt.close()

# 图3：高价值客户消费分布（散点图，和 README 里的“客户消费金额与频次”对应）
pdf_customer = customer_analysis.toPandas()
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pdf_customer, x="OrderCount", y="TotalSpent", s=100, color="#2ecc71")
plt.title("Customer Consumption Frequency vs. Total Spent (Top 10)", fontsize=16)
plt.xlabel("Order Count (Purchase Frequency)")
plt.ylabel("Total Spent (Customer Value)")
plt.tight_layout()
plt.savefig("output/customer_analysis.png", dpi=300)
plt.close()

print("\n✅ 可视化图表已保存到 output/ 文件夹！")
spark.stop()