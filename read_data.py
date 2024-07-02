import numpy as np
import pandas as pd
from pymongo import MongoClient
import random
import time

# 连接MongoDB数据库
client = MongoClient('mongodb://192.168.1.12:27017/')
database = client.mydatabase
collection = database.taobao
def read_data():

    sale_data = pd.read_csv('taobao_1.csv',encoding='utf-8')
    sale_data.drop_duplicates(inplace=True)
    # print(sale_data.duplicated())
    # duplicate_rows = sale_data[sale_data.duplicated()]
    # print(f"重复的行数：{len(duplicate_rows)}")

    # 将用户名列转换为字符串类型
    sale_data['用户名'] = sale_data['用户名'].astype(str)

    # sale_data.drop('index', axis=1, inplace=True) # 删除索引列

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

if __name__ == '__main__':
    # 清空集合
    # collection.delete_many({})
    # 读取数据并插入MongoDB
    # read_data()
    # 获取集合中文档的总数量

    total_docs = collection.count_documents({})

    # 生成10000个随机的文档ID
    random_ids = np.random.randint(0, total_docs, size=500)

    # 用于记录查询时间的列表
    query_times = []
    queried_data = []

    for doc_id in random_ids:
        start_time = time.time()
        # 查询文档，假设使用_id字段作为唯一标识
        collection.find_one({'index': int(doc_id)})
        end_time = time.time()
        query_times.append(end_time - start_time)

    # 计算平均查询时间
    average_query_time = np.mean(query_times)
    sum_query_time = np.sum(query_times)
    print(f"Average query time for 10000 documents: {average_query_time} seconds, {sum_query_time} seconds")

    # 批量查询
    # batch_size = 100
    # for i in range(0, len(random_ids), batch_size):
    #     batch_ids = random_ids[i:i + batch_size]
    #     start_time = time.time()
    #     # 使用批量查询
    #     batch_ids_int = [int(i) for i in batch_ids]
    #     documents = collection.find({'index': {'$in': batch_ids_int}})
    #     end_time = time.time()
    #     query_times.append(end_time - start_time)
    #
    #     # 收集查询到的数据
    #     for doc in documents:
    #         queried_data.append(doc)
    #
    # # 计算平均查询时间
    # average_query_time = np.mean(query_times)
    # sum_query_time = np.sum(query_times)
    # print(f"Average query time for 10000 documents: {average_query_time} seconds, {sum_query_time} seconds")
    #
    # # 输出查询到的数据
    # for doc in queried_data:
    #     print(doc)


