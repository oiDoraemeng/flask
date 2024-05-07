from exts import mongo

# 创建用户类
class User:
    """
    user_data = {
        "username": "admin",
        "password": "password",
        "email": "admin@example.com"
        "token": "<PASSWORD>"
    }
    """
    def __init__(self, user_data):
        self._id = user_data.get("_id")
        self.username = user_data.get("username")
        self.password = user_data.get("password")
        self.email = user_data.get("email")
        self.user_data = user_data
        self.collection = mongo.db.user

    def save(self, user_data):
        # 将用户数据保存到数据库
        self.collection.insert_one(user_data)

    @staticmethod
    def find_by_id(user_id):
        # 根据用户ID查找用户数据
        return mongo.db.user.find_one({"_id": user_id})

    @staticmethod
    def find_by_condition(condition):
        # 根据用户ID查找用户数据
        return mongo.db.user.find_one(condition)

    @staticmethod
    def getUser(condition):
        # 查询用户
        user = User(mongo.db.user.find_one(condition))
        return user

    def update(self, new_data):
        # 更新用户数据
        self.collection.update_one({"_id": self.user_data["_id"]}, {"$set": new_data})

    def delete(self):
        # 删除用户数据
        self.collection.delete_one({"_id": self.user_data["_id"]})

# 创建文章类
class Article:
    """
        article_data = {
        "title": "Sample Article",
        "content": "This is a sample article content.",
        "create_time": datetime.now(),
        author: user,
        "author_id": user._id
    }
    """

    def __init__(self, article_data):
        self._id = article_data.get("_id")
        self.title = article_data.get("title")
        self.content = article_data.get("content")
        self.create_time = article_data.get("create_time")
        self.collection = mongo.db.article


        self.author = article_data.get("author")
        self.author_id = article_data.get("author_id")

    def save(self, article_data):
        # 将文章数据保存到数据库
        self.collection.insert_one(article_data)

    @staticmethod
    def find_by_id(article_id):
        # 根据文章ID查找文章数据
        return mongo.db.article.find_one({"_id": article_id})

    @staticmethod
    def find_by_condition(condition):
        # 根据文章ID查找文章数据
        return mongo.db.article.find_one(condition)


    @staticmethod
    def getArticle(condition):
        # 查询文章
        article = Article(mongo.db.article.find_one(condition))
        return article

    def update(self, new_data):
        # 更新文章数据
        self.collection.update_one({"_id": self.article_data["_id"]}, {"$set": new_data})

    def delete(self):
        # 删除文章数据
        self.collection.delete_one({"_id": self.article_data["_id"]})
