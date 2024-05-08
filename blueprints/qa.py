from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify
from datetime import datetime

from .form import ArticleForm, CommentForm
from models import Article
from decorators import login_required

qa = Blueprint('qa', __name__,url_prefix='/qa')


@qa.route('/')
def index():
    articles = Article.getArticles({"author":g.user.username})
    return render_template('index.html', articles=articles)


@qa.route('/article', methods=['GET', 'POST'])
def article():
    article_id = request.args.get('id')
    article = Article.getArticleById(ObjectId(article_id))
    return render_template('article_detail.html', article=article)


@qa.route('/article/edit', methods=['GET', 'POST'])
@login_required
def article_edit():
    if request.method == 'POST':
        form = ArticleForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            article_data = {
                "title": title,
                "content": content,
                "create_time": datetime.now(),
                "author": g.user.username,
                "author_id": g.user._id
            }
            Article.save(article_data)
            return redirect(url_for('qa.index'))
        else:
            return jsonify(errors=form.errors)
    else:
        return render_template('article.html')


@qa.route('/article/comment', methods=['POST'])
@login_required
def article_comment():
    form = CommentForm(request.form)
    if form.validate():
    else:
        form.errors


