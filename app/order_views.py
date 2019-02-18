from flask import Blueprint, render_template, jsonify, request, session

from app.models import House, Order

order_blue = Blueprint('order', __name__)


@order_blue.route('/hello/', methods=['GET'])
def hello():
    return 'word'


@order_blue.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@order_blue.route('/my_booking/<int:id>/', methods=['GET'])
def my_booking(id):
    house = House.query.get(id)

    return jsonify({'code': 200, 'msg': '请求成功', 'data': house.to_dict()})


@order_blue.route('/booking/', methods=['POST'])
def booking_data():
    house_id = int(request.form.get('house_id'))
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    days = request.form.get('days')
    house_price = request.form.get('house_price')
    amount = request.form.get('amount')
    user_id = session.get('user_id')
    user_order = Order()
    user_order.user_id = user_id
    user_order.house_id = house_id
    user_order.begin_date = start_time
    user_order.end_date = end_time
    user_order.days = days
    user_order.house_price = house_price
    user_order.amount = amount
    user_order.add_update()
    house = House.query.filter_by(id=house_id).first()
    house.order_count += 1
    house.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@order_blue.route('/orders/', methods=['GET'])
def orders():
    return render_template('orders.html')

@order_blue.route('/my_order/', methods=['GET'])
def my_order():

    user_id = session.get('user_id')
    orders = Order.query.filter_by(user_id=user_id).all()
    data = []
    for order in orders:
        data.append(order.to_dict())
    return jsonify({'code': 200, 'msg': '请求成功', 'data':data})


@order_blue.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')

@order_blue.route('/my_lorders/', methods=['GET'])
def my_lorders():
    user_id = session.get('user_id')
    houses = House.query.filter_by(user_id=user_id).all()
    data = []
    for house in houses:
        orders = Order.query.filter_by(house_id=house.id).all()
        for order in orders:
            data.append(order.to_dict())

    return jsonify({'code': 200, 'msg': '请求成功', 'data': data})

# 接单
@order_blue.route('/my_status/', methods=['PATCH'])
def my_status():
    id = int(request.form.get('id'))
    status = request.form.get('status')
    order = Order.query.filter_by(id=id).first()
    order.status = status
    order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})

# 用户评价
@order_blue.route('/my_comment/', methods=['PATCH'])
def my_comment():
    id = int(request.form.get('id'))
    comment = request.form.get('client_comment')
    order = Order.query.filter_by(id=id).first()
    order.comment = comment
    order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})