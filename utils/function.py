# 外层函数嵌套内层函数
# 外层函数返回内层函数
# 内层函数调用外层函数的参数
from flask import session, redirect, url_for
from functools import wraps

def is_login(func):
    @wraps(func)
    def check(*args, **kwargs):
        if 'user_id' in session:
            #判断session中是否存在登录的标识user_id
            return func(*args, **kwargs)
        else:
            # 没有登录,跳转到登录界面
            return redirect(url_for('user.login'))
    return check