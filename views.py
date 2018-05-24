#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Delivery, DeliverySchema, Shippment, ShippmentSchema
from main import db, app
from flask import request, jsonify, render_template
from datetime import datetime
from flask_migrate import init, migrate, upgrade, Migrate

delivery_schema = DeliverySchema()
deliveries_schema = DeliverySchema(many=True)

shippment_schema = ShippmentSchema()
shippments_schema = ShippmentSchema(many=True)

# Main landing page
@app.route("/")
def homepage():
    """
    Render the homepage template on the / route
    """
    try:
        return render_template('index.html', title="Welcome")
    except:
        return 'Cannot load file specified'

# url to initiate flask migration
@app.route('/admin/dbinit')
def dbinit():
    try:
        migrate_dict = Migrate(app, db)
        print(migrate_dict.directory)
        init(directory=migrate_dict.directory)
        return 'db initiated'
    except Exception as e: 
        return str(e)

# url to update tables in db
@app.route('/admin/dbupgrade')
def dbupgrade():
    try:
        migrate_dict = Migrate(app, db)
        migrate(directory=migrate_dict.directory)
        upgrade(directory=migrate_dict.directory)
        all_tables = ' <br/>'.join(map(str, db.engine.table_names()))
        return 'Tables upgraded in database <br/>' + all_tables
    except Exception as e: 
        return str(e)

def checkKey(data,key):
    if key not in data:
        return ''
    else: 
        return data[key]

# submit data into DB
def add_order_new(rawdata):
    arrShippment = []
    if len(checkKey(rawdata,'order_ID')) > 0:
        order_ID = checkKey(rawdata,'order_ID')
    else:
        return 'Error: unfound key "order_ID"'
    clientname = checkKey(rawdata,'clientname')
    businesstype = checkKey(rawdata,'businesstype')
    delivery_date = checkKey(rawdata,'delivery_date')
    delivery_fee = checkKey(rawdata,'delivery_fee')
    car_type = checkKey(rawdata,'car_type')
    car_ID = checkKey(rawdata,'car_ID')
    good_size = checkKey(rawdata,'good_size')
    comment = checkKey(rawdata,'comment')
    ships = checkKey(rawdata,'ships')
    # 建立Shippments
    for ship in ships:
        if len(checkKey(ship,'ship_ID')) > 0 :
            ship_ID = checkKey(ship,'ship_ID')
        else:
            return 'Error: unfound key "ship_ID"'
        contact_info = checkKey(ship,'contact_info')
        ship_orderStore = checkKey(ship,'ship_orderStore')
        ship_datetime = checkKey(ship,'ship_datetime')
        ship_area = checkKey(ship,'ship_area')
        ship_district = checkKey(ship,'ship_district')
        driver = checkKey(ship,'ship_driver')
        is_elevator = checkKey(ship,'is_elevator')
        floors_byhand = checkKey(ship,'floors_byhand')
        amount_collect = checkKey(ship,'amount_collect')
        ship_comment = checkKey(ship,'comment')
        result_ship = Shippment.query.with_for_update().filter_by(ship_ID=ship_ID).first()
        if result_ship is None: 
            arrShippment.append(Shippment(ship_ID,order_ID,contact_info,ship_orderStore,ship_datetime,ship_area,ship_district,driver,car_type,car_ID,is_elevator,floors_byhand,amount_collect,ship_comment))
        
    # 查詢此Order是否已存在
    result_delivery = Delivery.query.with_for_update().filter_by(order_ID=order_ID).first()
    # 資料庫沒有此Order => 新增Order
    if result_delivery is None:
        new_delivery = Delivery(businesstype,order_ID,clientname,delivery_date,delivery_fee,good_size,comment)
        try:
            db.session.add(new_delivery)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        # 如果Ships超過一筆，逐筆加入
        if len(arrShippment) > 0:
            for oneShip in arrShippment:
                try:
                    db.session.add(oneShip)
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
        else:
            return 'Error: no shippment in this order'
        return '新增成功'
    else: 
        return 'Notice: This order already exists'

# new endpoint to parse post with Json array
@app.route("/order", methods=["POST"])
def acceptPOST():
    if request.json:
        rawdata = request.get_json(force=True)
        # 透過檢查order_ID來確定這是array of jsons還是json
        if len(rawdata) > 1 and len(checkKey(rawdata,'order_ID')) == 0:
            result = ""
            for data in rawdata:
                result = add_order_new(data)
                if len(result) > 0 and result != '新增成功':
                    return result
                else:
                    continue
            return result
        else:
            return add_order_new(rawdata)
    else:
        return 'Error: no data in the POST request'

# new endpoint to parse post with Json array
@app.route("/order_old", methods=["POST"])
def add_order():
    if request.json:
        arrShippment = []
        rawdata = request.get_json(force=True)
        if len(checkKey(rawdata,'order_ID')) > 0:
            order_ID = checkKey(rawdata,'order_ID')
        else:
            return 'Error: unfound key "order_ID"'
        clientname = checkKey(rawdata,'clientname')
        businesstype = checkKey(rawdata,'businesstype')
        delivery_date = checkKey(rawdata,'delivery_date')
        delivery_fee = checkKey(rawdata,'delivery_fee')
        car_type = checkKey(rawdata,'car_type')
        car_ID = checkKey(rawdata,'car_ID')
        good_size = checkKey(rawdata,'good_size')
        comment = checkKey(rawdata,'comment')
        ships = checkKey(rawdata,'ships')
        # 建立Shippments
        for ship in ships:
            if len(checkKey(ship,'ship_ID')) > 0 :
                ship_ID = checkKey(ship,'ship_ID')
            else:
                return 'Error: unfound key "ship_ID"'
            contact_info = checkKey(ship,'contact_info')
            ship_orderStore = checkKey(ship,'ship_orderStore')
            ship_datetime = checkKey(ship,'ship_datetime')
            ship_area = checkKey(ship,'ship_area')
            ship_district = checkKey(ship,'ship_district')
            driver = checkKey(ship,'ship_driver')
            is_elevator = checkKey(ship,'is_elevator')
            floors_byhand = checkKey(ship,'floors_byhand')
            amount_collect = checkKey(ship,'amount_collect')
            ship_comment = checkKey(ship,'comment')
            result_ship = Shippment.query.with_for_update().filter_by(ship_ID=ship_ID).first()
            if result_ship is None: 
                arrShippment.append(Shippment(ship_ID,order_ID,contact_info,ship_orderStore,ship_datetime,ship_area,ship_district,driver,car_type,car_ID,is_elevator,floors_byhand,amount_collect,ship_comment))
        
        # 查詢此Order是否已存在
        result_delivery = Delivery.query.with_for_update().filter_by(order_ID=order_ID).first()
        # 資料庫沒有此Order => 新增Order
        if result_delivery is None:
            new_delivery = Delivery(businesstype,order_ID,clientname,delivery_date,delivery_fee,good_size,comment)
            try:
                db.session.add(new_delivery)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            # 如果Ships超過一筆，逐筆加入
            if len(arrShippment) > 0:
                for oneShip in arrShippment:
                    try:
                        db.session.add(oneShip)
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise
            else:
                return 'Error: no shippment in this order'
            return '新增成功'
        else: 
            return 'Notice: This order already exists'
    else:
        return 'Error: no data in the POST request'
        # return jsonify(rawdata)

# endpoint to create new delivery entry
@app.route("/delivery", methods=["POST"])
def add_delivery():
    result_delivery = Delivery.query.with_for_update().filter_by(order_ID=request.json['order_ID']).first()
    if result_delivery is None:
        new_delivery = Delivery(
            request.json['businesstype'], 
            request.json['order_ID'],
            request.json['clientname'], 
            request.json['delivery_date'],
            request.json['delivery_fee'],
            request.json['good_size'],
            request.json['comment']
            )
        try:
            db.session.add(new_delivery)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
            return '{}'.format(new_delivery)
    else:
        return 'this order is already exist'

# endpoint to show all delivery entries
@app.route("/delivery", methods=["GET"])
def get_delivery():
    all_delivery = Delivery.query.all()
    print(all_delivery)
    # # May use the following to return other JSON format structure
    # results = {}
    # for delivery in all_delivery:
    #     results.update({
    #         delivery.id:{
    #             'name': delivery.name,
    #             'description': delivery.description
    #             }
    #         }
    #     )
    # return jsonify(results)
    result = deliveries_schema.dump(all_delivery)
    return jsonify(result.data)

# endpoint to get delivery entry detail by order id
@app.route("/delivery/<id>", methods=["GET"])
def delivery_detail(id):
    delivery = Delivery.query.filter_by(order_ID=id).first()
    return delivery_schema.jsonify(delivery)

# endpoint to update delivery entry by order id for businesstype, clientname, and comment
@app.route("/delivery/<id>", methods=["PUT", "POST"])
def delivery_update(id):
    delivery = Delivery.query.filter_by(order_ID=id).first()
    try:
        businesstype = request.json['businesstype']
        delivery.businesstype = businesstype
    except:
        pass
    try:
        clientname = request.json['clientname']
        delivery.clientname = clientname    
    except:
        pass
    try:
        delivery_date = request.json['delivery_date']
        delivery.delivery_date = delivery_date    
    except:
        pass
    try:
        delivery_fee = request.json['delivery_fee']
        delivery.delivery_date = delivery_fee    
    except:
        pass
    try:
        comment = '\ new comment' + request.json['comment']
        delivery.comment += comment
    except:
        pass
    delivery.updated_at = datetime.utcnow()
    
    db.session.commit()
    return delivery_schema.jsonify(delivery)

# endpoint to delete delivery entry by order id
@app.route("/delivery/<id>", methods=["DELETE"])
def delivery_delete(id):
    delivery = Delivery.query.filter_by(order_ID=id).first()
    db.session.delete(delivery)
    db.session.commit()

    return delivery_schema.jsonify(delivery)

# endpoint to create new shippment entry
@app.route("/shippment", methods=["POST"])
def add_shippment():
    result_ship = Shippment.query.with_for_update().filter_by(ship_ID=request.json['ship_ID']).first()
    if result_ship is None: 
        new_shippment = Shippment(
            request.json['ship_ID'],
            request.json['order_ID'],  
            request.json['contact_info'],
            request.json['ship_orderStore'],
            request.json['ship_datetime'],
            request.json['ship_area'],
            request.json['ship_district'],
            request.json['driver'],
            request.json['car_type'],
            request.json['car_ID'],
            request.json['is_elevator'],
            request.json['floors_byhand'],
            request.json['amount_collect'],
            request.json['ship_comment']
            )
        try:
            db.session.add(new_shippment)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
            return '{}'.format(new_shippment)
    else:
        return 'this shippment is already exist'

# endpoint to show all shippment entries
@app.route("/shippment", methods=["GET"])
def get_shippment():
    all_shippments = Shippment.query.all()
    result = shippments_schema.dump(all_shippments)
    return jsonify(result.data)

# endpoint to get shippment entry detail by ship id
@app.route("/shippment/<id>", methods=["GET"])
def shippment_detail(id):
    shippment = Shippment.query.filter_by(ship_ID=id).first()
    return shippment_schema.jsonify(shippment)

# endpoint to update shippment entry by order id
@app.route("/shippment/<id>", methods=["PUT", "POST"])
def shippment_update(id):
    shippment = Shippment.query.filter_by(order_ID=id).first()

    try:
        contact_info = request.json['contact_info']
        shippment.contact_info = contact_info
    except:
        pass

    try:
        ship_ID = request.json['ship_ID']
        shippment.ship_ID = ship_ID
    except:
        pass

    try:
        ship_orderStore = request.json['ship_orderStore']
        shippment.ship_orderStore = ship_orderStore
    except:
        pass

    try:
        ship_datetime = request.json['ship_datetime']
        shippment.ship_datetime = ship_datetime
    except:
        pass

    try:
        ship_area = request.json['ship_area']
        shippment.ship_area = ship_area
    except:
        pass

    try:
        ship_district = request.json['ship_district']
        shippment.ship_district = ship_district
    except:
        pass

    try:
        driver = request.json['driver']
        shippment.driver = driver
    except:
        pass

    try:
        car_type = request.json['car_type']
        shippment.car_type = car_type
    except:
        pass

    try:
        car_ID = request.json['car_ID']
        shippment.car_ID = car_ID
    except:
        pass

    try:
        is_elevator = request.json['is_elevator']
        shippment.is_elevator = is_elevator
    except:
        pass

    try:
        floors_byhand = request.json['floors_byhand']
        shippment.floors_byhand = floors_byhand
    except:
        pass

    try:
        amount_collect = request.json['amount_collect']
        shippment.amount_collect = amount_collect
    except:
        pass

    try:
        comment = '/ Comment: ' + request.json['ship_comment']
        shippment.comment += comment
    except:
        pass

    db.session.commit()
    return shippment_schema.jsonify(shippment)

# endpoint to delete delivery entry by order id
@app.route("/shippment/<id>", methods=["DELETE"])
def shippment_delete(id):
    shippment = Shippment.query.filter_by(ship_ID=id).first()
    db.session.delete(shippment)
    db.session.commit()

    return shippment_schema.jsonify(shippment)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()