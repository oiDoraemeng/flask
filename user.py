from pymongo import MongoClient
import random

# 连接MongoDB数据库
client = MongoClient('mongodb://localhost:27017/')

# MongoDB 中可存在多个数据库，根据数据库名称获取数据库对象
db = client.student

# 指定集合
collection = db.score

# 读取 MongoDB 中的所有数据库
dblist = client.list_database_names()
print(dblist)

# 要添加属性的查询条件
query = {'name': '褐伟丽'}

# 要添加的新属性
new_property = {'$set': {'password': '123'}}

# 更新文档中符合查询条件的数据，添加新属性
collection.update_one(query, new_property)
"""随机生成100条指定格式的文档
{
        "name": name,
        "age": age,
        "province": province,
        "subject": [
            {"name": "chinese", "score": score},
            {"name": "math", "score": score},
            {"name": "english", "score": score},
            {"name": "chemic", "score": score},
        ]}

# 姓列表
familyNameList = '赵钱孙李周吴郑王冯陈褐卫蒋沈韩杨朱秦尤许何昌施张孔崔卢曹严华金魏刘范陶姜戚谢邹喻柏水左窦章云苏活葛奚范彭郎鲁韦昌马苗风花方'
# 名列表
nameList = "玉媛德华建刚山一泽梓子字明汐芮东霖龙海勇晓伟磊雷爱丹军清飞字冉斌敏玉源静丽燕娜亚芳强楠航千平黎钟明陈菜冰牧沐善研憙德智听璇炫轩"
# 省份列表
provinceList = ["广东", "广西", "山东", "山西", "河南","河北","湖南","湖北","重庆","四川","云南","海南","江西","上海","浙江"]

# 插入随机生成的100条文档
for i in range(100):
    # 随机生成文档
    stu = {
        "name": random.choice(familyNameList) + "".join(random.choices(nameList,k=random.randint(1,2))),
        "age": random.randint(1, 30),
        "province": random.choice(provinceList),
        "subject": [
            {"name": "Chinese", "score": random.randint(0, 100)},
            {"name": "Math", "score": random.randint(0, 100)},
            {"name": "English", "score": random.randint(0, 100)},
            {"name": "Chemic", "score": random.randint(0, 100)},
        ]}
    # 打印生成的文档
    print(stu)
    # 将生成的文档插入集合中，生成一条插入一条
    result_id = collection.insert_one(stu)
    print(result_id)

print("100条文档已全部插入完成!")
"""