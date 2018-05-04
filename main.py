import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# db initialization
db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True)

# connects to Google Cloud SQL within the same instance
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
#app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@/company"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ctdb1:750111@104.155.195.75/company?unix_socket=/cloudsql/ct-erp:asia-east1:ctdb1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# code for migrating db
migrate = Migrate(app, db)

# API routing in view.py
from views import *

if __name__ == '__main__':
    app.run(debug=True)