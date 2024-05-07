from flask import session
import wtforms
from werkzeug.security import check_password_hash
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

# 并导入验证器
class registerForm(wtforms.Form):
    # 定义注册表单
    username = wtforms.StringField('Username', validators=[DataRequired(), Length(min=3, max=20, message='用户名格式错误')])
    password = wtforms.PasswordField('Password', validators=[DataRequired(),Length(min=3, max=20, message='密码格式错误')]) # 密码字段，输入密码时不可见
    password_confirmation = wtforms.PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='两次密码输入不一致')])
    email = wtforms.StringField('Email', validators=[Email(message='邮箱格式错误')])
    identifying_code = wtforms.StringField('Identifying Code', validators=[DataRequired(), Length(min=6, max=6, message='验证码格式错误')])

    def validate_user(self, username):
        # 自定义验证器，检查用户名是否已被注册
        user = User.getUser({'username': username.data})
        if user.username:
            raise ValidationError('用户名已被注册')
        if user.email:
            raise ValidationError('邮箱已被注册')

    def validate_identifying(self, code):
        # 自定义验证器，检查验证码是否正确
        identifying_code = session['code']
        if code.data != identifying_code :
            raise ValidationError('验证码错误')



class loginForm(wtforms.Form):
    # 定义登录表单
    username = wtforms.StringField('Username', validators=[DataRequired(), Length(min=3, max=20, message='用户名格式错误')])
    password = wtforms.PasswordField('Password', validators=[DataRequired(),Length(min=3, max=20, message='密码格式错误')]) # 密码字段，输入密码时不可见


class changePasswordForm(wtforms.Form):
    # 定义修改密码表单
    old_password = wtforms.PasswordField('Old Password', validators=[DataRequired(),Length(min=3, max=20, message='密码格式错误')]) # 密码字段，输入密码时不可见
    new_password = wtforms.PasswordField('New Password', validators=[DataRequired(),Length(min=3, max=20, message='密码格式错误')]) # 密码字段，输入密码时不可见
    new_password_confirmation = wtforms.PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password', message='两次密码输入不一致')])

    def validate_old_password(self, old_password):
        # 自定义验证器，检查旧密码是否正确
        user = User.getUser({'username': session['username']})
        if not user or not check_password_hash(user['password'], old_password.data):
            raise ValidationError('旧密码错误')


class QuestionForm(wtforms.Form):
    # 定义提问表单
    title = wtforms.StringField('Title', validators=[DataRequired(), Length(min=1, max=100, message='标题格式错误')])
    content = wtforms.TextAreaField('Content', validators=[DataRequired(), Length(min=1,  message='内容格式错误')])



