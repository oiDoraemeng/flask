from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify
from datetime import datetime
from bson.regex import Regex

from .form import ArticleForm, CommentForm
from models import Article, Comment
from decorators import login_required

qa = Blueprint('qa', __name__, url_prefix='/qa')

# 首页
@qa.route('/')
def index():
    articles = Article.getArticles({"author": g.user.username})
    return render_template('index.html', articles=articles)

# 查看文章详情
@qa.route('/article', methods=['GET', 'POST'])
def article():
    article_id = request.args.get('id')
    article = Article.getArticleById(ObjectId(article_id))
    return render_template('article_detail.html', article=article)

# 发表文章
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

# 发表评论
@qa.route('/article/comment', methods=['POST'])
@login_required
def article_comment():
    form = CommentForm(request.form)
    if form.validate():
        content = form.content.data
        article_id = form.article_id.data
        comment_data = {
            "content": content,
            "create_time": datetime.now(),
            # "author": g.user.username,
            "author_id": g.user._id,
            "article_id": ObjectId(article_id)
        }
        Comment.save(comment_data)
        return redirect(url_for('qa.article', id=article_id))
    else:
        form.errors

        return redirect(request.referrer)

# 搜索文章
@qa.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.args.get('keyword')
    if keyword:
        # 构造正则表达式以匹配包含关键字的文章标题
        regex = Regex(keyword, 'i')  # 'i' 表示不区分大小写

        # 使用正则表达式执行查询
        articles = Article.getArticles({"title": {"$regex": regex}})

        # 返回包含关键字的文章列表
        return render_template('index.html', articles=articles)
    else:
        # 如果没有提供关键字，则返回空结果
        return redirect(request.referrer)

