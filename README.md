# 电商零售用户行为分析（PySpark）

## 项目简介
本项目基于公开电商订单数据集，使用 PySpark 进行大规模数据清洗与统计分析，旨在挖掘用户购买行为、商品销售表现及区域分布等核心业务指标。

## 技术栈
- 语言：Python 3.x
- 大数据引擎：PySpark 3.x
- 核心能力：数据清洗、缺失值处理、异常值过滤、分组统计

## 运行说明
1.  安装依赖：
    ```bash
    pip install pyspark
2. 运行代码：
    ```bash
    python retail_analysis.py
##核心步骤
数据加载与清洗
加载订单数据，过滤空值、异常值（如负数量、负价格）
清洗后有效数据量：397884 条（原始数据 541909 条）
统计分析
订单总量、用户数、国家分布
热门商品销量排行
客户消费金额与频次分析
##项目亮点
使用 PySpark 处理十万级数据，代码可扩展至更大规模数据集
完整的清洗逻辑，保证数据质量
结果清晰易读，可直接用于业务决策参考
## 项目结构
retail-spark-analysis/
├── README.md
├── retail_analysis.py
├── .gitignore
├── data/
│ └── README.md
└── output/
└── result_snapshot.txt
## 可视化分析结果
### 1. 订单国家分布（TOP10）
![订单国家分布](output/country_distribution.png)

### 2. 热门商品销量排行（TOP10）
![热门商品销量](output/top_products.png)

### 3. 高价值客户消费行为分析
![客户消费分析](output/customer_analysis.png)