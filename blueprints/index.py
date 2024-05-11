



@order.route('/', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        pass
# 默认路由，显示欢迎页面
@app.route('/')
def index():

    if 'username' in session:
        username = session['username']
        return render_template('hello.html', username=username)
    return render_template('hello.html')


# 带参数的路由，函数渲染HTML文件
@app.route('/hello/<username>', methods=['GET', 'POST'])
def hello(username):

    if username == "root":
        data = collection_user.find()
        return render_template('hello.html', username=username, user_data=data)
    else:
        return render_template('hello.html', username=username)



@app.route('/logout/')
def logout():
    # remove the username from the session if it is there
    session.pop('user_id', None)
    flash("您已退出登录")
    return redirect(url_for('index'))


@app.route('/delete/<username>/', methods=['POST', 'GET'])
def delete(username):
    collection_user.delete_one({'username': username})
    # 重定向到当前页面
    return redirect(request.referrer)


@app.route('/score/', methods=['POST', 'GET'])
def score():
    username=session.get('username')
    if username is None:
        flash("您还未登录,请登录后在查询")
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面
    # token是否为空
    # print(request.method)
    # if request.method == 'POST':
    #     token = request.form['token']
    # if request.method == 'GET':
    #     token = request.args.get('token')
    # if not token :
    #     return redirect(request.referrer)
    # # token是否合法

    # 查询MongoDB中的数据
    student_data = collection_score.find()
    # 将数据传递到HTML模板中
    return render_template('score.html', username = username,student_data=student_data)


@app.route('/score/<name>/', methods=['POST', 'GET'])
def score_student(name):
    student_data = collection_score.find_one({'name': name})
    if student_data:
        return render_template('score.html', name=name, student_data=[student_data])


# 路由用于处理提交表单的请求
@app.route('/submit/', methods=['POST'])
def submit():
    name = request.form['name']  # 获取表单中的姓名字段值
    student_data = collection_score.find_one({'name': name})  # 在MongoDB中查找名字
    if student_data:
        # 如果找到名字，返回JSON响应，表示查找成功
        return jsonify({'success': True, 'message': '查找成功'})
    else:
        # 如果未找到名字，返回JSON响应，表示查找失败
        return jsonify({'success': False, 'message': '查找失败'})


@app.route('/order/', methods=['POST', 'GET'])
def order():
    username = session.get('username')
    if username is None:
        flash("您还未登录,请登录后在查询")
        return redirect(url_for('login'))  # 如果用户未登录，则重定向到登录页面
    if request.method == 'GET':
        number = request.args.get('number')
        if number   :
            order_data = collection_purchase.find({"用户名": number},{"_id": 0} )
            # 将ObjectId转换为字符串
            order_data = json.loads(json_util.dumps(order_data))  # 使用json_util处理ObjectId
            return jsonify(order_data)
        else:
            return render_template('order.html', username=username)

@app.route('/setcookie/', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['name']
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie('userID', user)
        return resp


# 尾部斜线(/) 使用/python或/python/返回相同的输出。URL:/flask/会导致404 Not Found页面。
@app.route('/getcookie/')
def getcookie():
    name = request.cookies.get('userID')
    print(name)
    return '<h1>welcome, ' + name + '</h1>'

