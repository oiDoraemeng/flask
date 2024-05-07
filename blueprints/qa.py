from flask import Blueprint, render_template, request, redirect
from datetime import datetime

from .form import QuestionForm

qa = Blueprint('qa', __name__,url_prefix='/')


@qa.route('/index/')
def index():
    return render_template('hello.html')

@qa.route('/qa/question/', methods=['GET', 'POST'])
def question():
    if request.method == 'POST':
        form = QuestionForm(request)
        if form.validate():
            title = form.title.data
            content = form.content.data
            article_data = {
                "title": title,
                "content": content,
                "create_time": datetime.now(),
                author: user,
                "author_id": user._id
            }

    return render_template('question.html')