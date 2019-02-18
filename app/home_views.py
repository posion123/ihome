import os
import uuid

from flask import Blueprint, render_template, session, jsonify, request
from flask_login import login_required

from app.models import User, Area, Facility, House, HouseImage

house_blue = Blueprint('house', __name__)


@house_blue.route('/hello/', methods=['GET'])
def hello():
    return 'hello'


@house_blue.route('/my_house/', methods=['GET'])
@login_required
def my_house():
    return render_template('myhouse.html')


@house_blue.route('/house_info/', methods=['GET'])
@login_required
def house_info():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    user_id_name = user.id_name
    user_id_card = user.id_card
    if not all([user_id_card, user_id_name]):
        return jsonify({'code': 1001, 'msg': '没有实名认证'})
    houses = House.query.filter_by(user_id=user_id).all()
    data = []
    for house in houses:
        data.append(house.to_dict())
    return jsonify({'code': 200, 'msg': '已经实名认证', 'data': data})


@house_blue.route('/newhouse/', methods=['GET'])
@login_required
def newhouse():
    return render_template('newhouse.html')


@house_blue.route('/newhouse_info/', methods=['GET'])
@login_required
def newhouse_info():
    areas = Area.query.all()
    data = []
    for area in areas:
        data.append(area.to_dict())
    return jsonify({'code': 200, 'msg': '请求成功', 'data': data})


@house_blue.route('/func_info/', methods=['GET'])
@login_required
def func_info():
    funcinfos = Facility.query.all()
    data = []
    for funcinfo in funcinfos:
        data.append(funcinfo.to_dict())

    return jsonify({'code': 200, 'msg': '请求成功', 'data': data})


@house_blue.route('/newhouse/', methods=['POST'])
@login_required
def my_newhouse():
    facilitys = request.form.getlist('facility')
    title = request.form.get('title')
    price = request.form.get('price')
    area_id = request.form.get('area_id')
    address = request.form.get('address')
    room_count = request.form.get('room_count')
    acreage = request.form.get('acreage')
    unit = request.form.get('unit')
    capacity = request.form.get('capacity')
    beds = request.form.get('beds')
    deposit = request.form.get('deposit')
    min_days = request.form.get('min_days')
    max_days = request.form.get('max_days')
    user_id = session.get('user_id')

    house = House()
    house.title = title
    house.price = price
    house.area_id = area_id
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days
    house.user_id = user_id
    house.add_update()
    facility = []
    for i in facilitys:
        facility.append(Facility.query.filter_by(id=int(i)).first())

    house.facilities = facility
    house.add_update()

    return jsonify({'code': 200, 'msg': '请求成功', 'data': house.id})


@house_blue.route('/newhouse/', methods=['PATCH'])
@login_required
def newhouse_image():
    image_url = request.files.get('house_image')
    id = request.form.get('house_id')
    BASE_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
    filename = str(uuid.uuid4())
    a = image_url.mimetype.split('/')[-1:][0]
    name = filename + '.' + a
    path = os.path.join(MEDIA_DIR, name)
    image_url.save(path)
    house = House.query.filter_by(id=id).first()
    if not house.index_image_url:
        house.index_image_url = name
        house.add_update()
    image = HouseImage()
    image.house_id = id
    image.url = name
    image.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@house_blue.route('/detail/', methods=['GET'])
def detail():

    return render_template('detail.html')


@house_blue.route('/my_detail/<int:id>/', methods=['GET'])
def my_detail(id):
    #房屋信息
    house = House.query.filter_by(id=id).first()
    houseinfo = house.to_full_dict()
    # 设施对象
    icon = house.facilities
    # 当前用户需要返回的
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    username = user.name
    userimage = user.avatar
    #房屋城区
    area = Area.query.get(house.area_id)
    area_name = area.name
    data = [houseinfo, username, userimage, area_name]
    return jsonify({'code': 200, 'msg': '请求成功', 'data':data})
