from main import db, app
from datetime import datetime
from flask_marshmallow import Marshmallow

# Connect Marshmallow to Flask app for schema formating 
ma = Marshmallow(app)

class Delivery(db.Model):
    """
    Create a table name delivery_order for Delivery
    Delivery contains Shippments
    """
    __tablename__ = 'delivery_order'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    businesstype = db.Column(db.String(255), nullable=True)
    clientname = db.Column(db.String(225), nullable=True)
    delivery_date =  db.Column(db.Date, nullable=True)
    delivery_fee =  db.Column(db.String(225), nullable=True)
    good_size =  db.Column(db.String(225), nullable=True)
    # a unique id number for future use
    order_ID = db.Column(db.String(15), unique=True, nullable=True)
    ship_ID = db.relationship('Shippment', backref='Delivery',lazy='dynamic')
    comment = db.Column(db.Text, nullable=True)
    

    def __init__(self, businesstype, order_ID, clientname="", delivery_date="", delivery_fee="",good_size="", comment=""):
        self.businesstype = businesstype
        self.clientname = clientname
        self.order_ID = order_ID
        self.delivery_date = delivery_date
        self.delivery_fee = delivery_fee
        self.good_size = good_size
        self.comment = comment

class DeliverySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('timestamp', 'updated_at', 'businesstype', 'clientname', 'order_ID', 'delivery_date','delivery_fee','good_size', 'comment')

class Shippment(db.Model):
    """
    Create a Shippment table
    """

    __tablename__ = 'ship_order'

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ship_ID = db.Column(db.String(255))
    order_ID = db.Column(db.String(15), nullable=True)
    to_order_ID = db.Column(db.Integer, db.ForeignKey('delivery_order.index'), nullable=True)
    contact_info = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    ship_orderStore = db.Column(db.String(255), nullable=True)
    ship_datetime = db.Column(db.String(225), nullable=True)
    ship_area = db.Column(db.String(255), nullable=True)
    ship_district = db.Column(db.String(255), nullable=True)
    driver = db.Column(db.String(255), nullable=True)
    car_type = db.Column(db.String(255), nullable=True)
    car_ID = db.Column(db.String(255), nullable=True)
    is_elevator = db.Column(db.String(255), nullable=True)
    floors_byhand = db.Column(db.String(255), nullable=True)
    amount_collect = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    
    
    def __init__(self, ship_ID, order_ID, contact_info, ship_orderStore, ship_datetime, ship_area, ship_district, driver, car_type, car_ID, is_elevator, floors_byhand, amount_collect, ship_comment):
        self.ship_ID = ship_ID
        self.order_ID = order_ID        
        self.contact_info = contact_info
        self.ship_orderStore = ship_orderStore
        self.ship_datetime = ship_datetime
        self.ship_area = ship_area
        self.ship_district = ship_district
        self.driver = driver
        self.car_type = car_type
        self.car_ID = car_ID
        self.is_elevator = is_elevator
        self.floors_byhand = floors_byhand
        self.amount_collect = amount_collect
        self.comment = ship_comment
 
class ShippmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('ship_ID','order_ID', 'contact_info', 'updated_at','ship_orderStore','ship_datetime', 'ship_area', 'ship_district', 'driver', 'car_type', 'car_ID', 'is_elevator', 'floors_byhand', 'amount_collect', 'comment')