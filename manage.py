
from flask import Flask
from flask_script import Manager

from app.home_views import house_blue
from app.order_views import order_blue
from app.user_views import user_blue, login_manage
from app.models import db


app = Flask(__name__)
app.register_blueprint(user_blue, url_prefix='/user')
app.register_blueprint(house_blue, url_prefix='/house')
app.register_blueprint(order_blue, url_prefix='/order')
# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/tenement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# 初始化数据库
db.init_app(app)

app.secret_key = 'kasdjkfladjflks45s454'

login_manage.init_app(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()

