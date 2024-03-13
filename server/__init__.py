from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from server.db import db, origin_db_uri

migrate = Migrate()

def create_app(db_uri=origin_db_uri):
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'my-secret-key'

    db.init_app(app)
    migrate.init_app(app, db)
    
    jwt = JWTManager(app)
    api = Api(app)

    return app


