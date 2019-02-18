import os
import random
import re
import uuid

from flask import Blueprint, render_template, jsonify, session, request
from flask_login import login_user, login_required, LoginManager
from sqlalchemy import desc

login_manage = LoginManager()
login_manage.login_view = 'user.login'

from app.models import User, db, House, Area, Order

user_blue = Blueprint('user', __name__)


@user_blue.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')

# 注册
@user_blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imagecode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整的参数'})
    # 2.验证手机号正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号不正确'})
    # 3.验证图片验证码
    if session['image_code'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码不正确'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})
    #  验证手机号受否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已经被注册，请重新注册'})
    # 　创建注册信息
    user = User()
    user.phone = mobile
    user.name = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@user_blue.route('/code/', methods=['GET'])
def get_code():
    # 获取验证码
    # 方式1：后端生成图片，并返回验证码图片的地址(不推荐)
    # 方式2：后端只生成随机参数，返回给页面，在页面中在生成图片(前端做)
    s = '1234567890qwertyuiopasdfghjklQWERTYUIOPASDFGHJKL'
    code = ''
    for i in range(4):
        code += random.choice(s)
    session['image_code'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@user_blue.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


#登录
@user_blue.route('/login/', methods=['POST'])
def my_login():
    mobile = request.form.get('mobile')
    passwd = request.form.get('passwd')
    if not all([mobile, passwd]):
        return jsonify({'code': 1001, 'msg': '请填写完整的参数'})
    user = User.query.filter_by(phone=mobile).first()
    if not user:
        return jsonify({'code': 1002, 'msg': '用户不存在,请先注册'})
    if not user.check_pwd(passwd):
        return jsonify({'code': 1003, 'msg': '密码不正确'})
    login_user(user)
    return jsonify({'code': 200, 'msg': '登陆成功'})


@login_manage.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@user_blue.route('/my/', methods=['GET'])
@login_required
def my():
    return render_template('my.html')


# 用户信息
@user_blue.route('/user_info/', methods=['GET'])
@login_required
def user_info():
    user_id = session.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict()})


@user_blue.route('/profile/', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')

# 修改用户信息页面
@user_blue.route('/profile/', methods=['PATCH'])
@login_required
def my_profile():
    username = request.form.get('name')
    avatar = request.files.get('avatar')
    if avatar:
        BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
        filename = str(uuid.uuid4())
        a = avatar.mimetype.split('/')[-1:][0]
        name = filename + '.' + a
        path = os.path.join(MEDIA_DIR, name)
        avatar.save(path)
        # 修改用户的头像
        user_id = session.get('user_id')
        stu = User.query.get(user_id)
        stu.avatar = name
        stu.add_update()
    if username:
        user_id = session.get('user_id')
        stu = User.query.get(user_id)
        stu.name = username
        stu.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'data': stu.to_basic_dict()})


@user_blue.route('/auth/', methods=['GET'])
@login_required
def auth():
    return render_template('auth.html')

# 实名认证
@user_blue.route('/auth/', methods=['PATCH'])
@login_required
def my_auth():
    realname = request.form.get('real_name')
    id_card = request.form.get('id_card')
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not all([realname, id_card]):
        return jsonify({'code': 1001, 'msg': '请补全信息'})
    if re.match('(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)', id_card):
        user.id_name = realname
        user.id_card = id_card
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})
    else:
        return jsonify({'code': 1002, 'msg': '你输入的证件号不符合规范'})

# 认证信息
@user_blue.route('/info/', methods=['GET'])
def info():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_id_card = user.id_card
    user_id_name = user.id_name
    if all([user_id_name, user_id_card]):
        return jsonify({'code': 200, 'msg': '请求成功', 'data': user.to_auth_dict()})

    return jsonify({'code': 1001, 'msg': '没有进行实名认证'})





@user_blue.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@user_blue.route('/house_sourse/', methods=['GET'])
def house_sourse():
    houses = House.query.all()[-3:]
    data = []
    for house in houses:
        data.append(house.to_dict())
    user_id = session.get('user_id')
    username = ''
    if user_id:
        username = User.query.filter_by(id=user_id).first().name
    return jsonify({'code': 200, 'msg': '请求成功', 'data':data, 'username':username})

@user_blue.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@user_blue.route('/my_search/', methods=['GET'])
def my_search():

    aid = int(request.args.get('aid'))
    aname = request.args.get('aname')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    data = []
    area = Area.query.filter_by(id=aid).first()
    houses = House.query.filter_by(area_id=area.id).all()

    for house in houses:
        house_sourse = Order.query.filter_by(house_id=house.id).first()
        if house_sourse:
            if house_sourse.status != 'REJECTED':
                order1 = Order.query.filter(str(house_sourse.begin_date) > sd, str(house_sourse.end_date) >= ed, ed>str(house_sourse.begin_date)).all()
                if order1:
                    for order in order1:
                        data.append(order.house_id)
                order2 = Order.query.filter(sd >= str(house_sourse.begin_date), ed <= str(house_sourse.end_date)).all()
                if order2:
                    for order in order2:
                        data.append(order.house_id)
                order3 = Order.query.filter(sd>=str(house_sourse.begin_date), ed>str(house_sourse.end_date), sd<=str(house_sourse.begin_date)).all()
                if order3:
                    for order in order3:
                        data.append(order.house_id)
                order4 = Order.query.filter(sd<str(house_sourse.begin_date), ed>str(house_sourse.end_date)).all()
                if order4:
                    for order in order4:
                        data.append(order.house_id)
    data = list(set(data))
    house_data = []
    for i in houses:
        if i.id not in data:
            house_data.append(i.to_dict())

    # 最新上线
    house_sort = []
    if sk == 'new':
        users = House.query.order_by(desc(House.create_time)).all()
        for i in houses:
            if i.id not in data:
                house_sort.append(i.to_dict())
        house_sort = house_sort[::-1]

    # 入住最多
    if sk == 'booking':
        house_sort1 = []
        users = House.query.order_by(desc(House.order_count)).all()
        for i in houses:
            if i.id not in data:
                house_sort.append(i)
        for user in users:
            for house in house_sort:
                if user == house:
                    house_sort1.append(user)
        house_sort = []
        for house_1 in house_sort1:
            house_sort.append(house_1.to_dict())
    # 价格高到低
    if sk == 'price-des':
        house_sort1 = []
        users = House.query.order_by(desc(House.price)).all()
        for i in houses:
            if i.id not in data:
                house_sort.append(i)
        for user in users:
            for house in house_sort:
                if user == house:
                    house_sort1.append(user)
        house_sort = []
        for house_1 in house_sort1:
            house_sort.append(house_1.to_dict())
    # 价格低到高
    if sk == 'price-inc':
        house_sort1 = []
        users = House.query.order_by(House.price).all()
        for i in houses:
            if i.id not in data:
                house_sort.append(i)
        for user in users:
            for house in house_sort:
                if user == house:
                    house_sort1.append(user)
        house_sort = []
        for house_1 in house_sort1:
            house_sort.append(house_1.to_dict())

    return jsonify({'code': 200, 'msg': '请求成功', 'house_sort': house_sort, 'data':house_data})


@user_blue.route('/logout/', methods=['GET'])
def logout():
    del session['user_id']

    return jsonify({'code': 200, 'msg':'请求成功'})