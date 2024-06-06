from flask_jwt_extended import JWTManager
from celery import Celery
from flask import Flask
from flask_migrate import Migrate
from flask_security import Security
from config import Config
from auth import user_datastore
from auth import auth_bp
from database import db
from jsonprc_methods import jsonrpc_bp
from admin import setup_admin

app = Flask('application')
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(jsonrpc_bp, url_prefix='/jsonrpc')

setup_admin(app)

celery = Celery(app.name, broker_url='redis://localhost:6379/0',include=["tasks"])
celery.config_from_object('config')


db.init_app(app)
migrate = Migrate(app, db)
security = Security(app, user_datastore)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
    celery.start()
