from flask import Blueprint, render_template, request, redirect, url_for, flash


order= Blueprint('order', __name__,url_prefix='/order' )

@order.route('/', methods=['GET', 'POST'])
def index():
    return render_template('order.html')