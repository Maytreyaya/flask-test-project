# from flask import Flask, jsonify
# from flask import request
# from jsonrpcserver import method, Result, Success, Error, dispatch
# from flask import Flask
# from flask_jsonrpc import JSONRPC
# from flask_migrate import Migrate
# from flask_security import Security, SQLAlchemyUserDatastore
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
# from config import Config
# from models import (db,
#                     User,
#                     Role,
#                     Product,
#                     Address,
#                     Order,
#                     OrderItem)
#
#
# app = Flask('application')
# app.config.from_object(Config)
#
#
# db.init_app(app)
# migrate = Migrate(app, db)
#
# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)
#
# admin = Admin(app, name='Admin Panel')
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Role, db.session))
# admin.add_view(ModelView(Product, db.session))
# admin.add_view(ModelView(Address, db.session))
# admin.add_view(ModelView(Order, db.session))
# admin.add_view(ModelView(OrderItem, db.session))
#
#
# @method
# def add(a, b):
#     return Success(a + b)
#
# @method
# def product():
#     return Result(Product.query.all())
#
#
# @app.route('/jsonrpc', methods=['POST'])
# def jsonrpc():
#     response = dispatch(request.data)
#     return jsonify(response)
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)