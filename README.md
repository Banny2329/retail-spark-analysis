# 数据集说明（retail_data.csv）

## 数据来源
公开零售交易数据集（Online Retail），包含英国某电商 2010–2011 年交易记录。

## 字段说明
- InvoiceNo：订单号（C 开头表示取消订单）
- StockCode：商品编码
- Description：商品名称
- Quantity：购买数量（负数为退货）
- InvoiceDate：订单时间
- UnitPrice：单价
- CustomerID：用户ID
- Country：国家

## 数据规模
- 记录数：约 54 万行
- 字段数：8 列
- 特点：存在缺失值、退货订单、异常单价/数量

## 注意
- 原始数据文件 `retail_data.csv` 不存入 Git（已在 .gitignore 忽略）
- 使用时自行放入 data/ 目录