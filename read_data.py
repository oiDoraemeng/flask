import numpy as np
import pandas as pd
from pymongo import MongoClient

# 连接MongoDB数据库
client = MongoClient('mongodb://localhost:27017/')
database = client.taobao
collection = database.purchase

sale_data = pd.read_csv('taobao_1.csv',encoding='utf-8')
sale_data.drop_duplicates(inplace=True)
# print(sale_data.duplicated())
# duplicate_rows = sale_data[sale_data.duplicated()]
# print(f"重复的行数：{len(duplicate_rows)}")

# 将用户名列转换为字符串类型
sale_data['用户名'] = sale_data['用户名'].astype(str)
sale_data.drop('Unnamed: 0', axis=1, inplace=True)

print(sale_data.head())
# 将DataFrame中的数据插入到MongoDB中的集合中
records = sale_data.to_dict(orient='records')
collection.insert_many(records)
"""生成指定格式的文档
{
        "用户名": name,
        "商品名": age,
        "行为": province,
        "物品类名": good,
        "日期": data,
        "小时":hour
        }
"""