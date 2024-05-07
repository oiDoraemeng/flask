import json
from bson import json_util, ObjectId

from flask import Flask, request, session, g
from flask_session import Session  # 导入Session扩展
from flask_cors import CORS

import config
from exts import mail, mongo
from blueprints.auth import auth
from blueprints.qa import qa
from utils.filters import datetime_format
from models import User

app = Flask(__name__)
app.secret_key = 'poiuytrewqasdfghjklmnopqrstuvwxyz'

# 允许跨域请求
CORS(app)

# 加载配置
app.config.from_object(config)

# 加载扩展
mail.init_app(app)
mongo.init_app(app)
Session(app)

# 注册蓝图
app.register_blueprint(auth)
app.register_blueprint(qa)

app.add_template_filter(datetime_format, 'dformat')


# hook
@app.before_request
def before_request():
    # 记录访问日志
    print(request.url)
    user_id = session.get('user_id')
    if user_id:
        user = User.getUser({"_id": ObjectId(user_id)})
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


@app.context_processor
def context_processor():
    return {'user': g.user}


if __name__ == '__main__':
    app.run(debug=True)
