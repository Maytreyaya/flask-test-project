from flask_jwt_extended import create_access_token, JWTManager
from celery import Celery
from jsonrpcserver import method, Success, Error, dispatch
from flask import Flask
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from config import Config

from models import (db,
                    User,
                    Role,
                    Product,
                    Address,
                    Order,
                    OrderItem)

from flask_security.utils import hash_password
from flask import jsonify, request
from flask_security.utils import verify_password
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token


app = Flask('application')
app.config.from_object(Config)
jwt = JWTManager(app)
celery = Celery(app.name, broker='redis://localhost:6379/0',include=["tasks"])
celery.config_from_object(Config)


@celery.task
def update_order_status(order_id, new_status):
    with app.app_context():
        order = Order.query.get(order_id)
        if order:
            order.status = new_status
            db.session.commit()
            with open('celery.log', 'a') as log_file:
                log_file.write(f'Order {order_id} changed status to {new_status}\n')


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    password = data['password']
    roles = data['roles']

    user = user_datastore.create_user(email=email, password=hash_password(password))

    role = Role.query.filter_by(name=roles).first()

    if role:
        user_datastore.add_role_to_user(user, role)
    else:
        return jsonify({"error": f"Role '{roles}' does not exist"}), 400

    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and verify_password(data['password'], user.password):
        access_token = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token,refresh_token=refresh)
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200


db.init_app(app)
migrate = Migrate(app, db)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class AdminModelView(ModelView):
    @jwt_required()
    def is_accessible(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user and "adminn" in user.roles[0].name:
            return True
        return False


admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(Product, db.session))
admin.add_view(AdminModelView(Address, db.session))
admin.add_view(AdminModelView(Order, db.session))
admin.add_view(AdminModelView(OrderItem, db.session))



@method
def get_products():
    products = Product.query.all()
    return Success([product.as_dict() for product in products])


@method
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return Success(product.as_dict())
    else:
        return Error("Product not found")


@method
def create_product(name, price, weight, color):
    product = Product(name=name,
                      price=price,
                      weight=weight,
                      color=color)
    db.session.add(product)
    db.session.commit()
    return Success(product.as_dict())


@method
def update_product(product_id, name=None, price=None):
    product = Product.query.get(product_id)
    if product:
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        db.session.commit()
        return Success(product.as_dict())
    else:
        return Error("Product not found")


@method
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return Success(f"Product {product_id} deleted")
    else:
        return Error("Product not found")


@method
def create_address(country, city, street):
    address = Address(country=country,
                      city=city,
                      street=street)
    db.session.add(address)
    db.session.commit()
    return Success(address.as_dict())


@method
def create_order(address_id, status, order_items):
    address = Address.query.get(address_id)
    if not address:
        return Error("Address not found")

    order = Order(address_id=address_id, status=status)
    db.session.add(order)
    db.session.flush()  # To get order.id before committing

    for item in order_items:
        product_id = item['product_id']
        quantity = item['quantity']
        product = Product.query.get(product_id)
        if not product:
            db.session.rollback()
            return Error(f"Product with id {product_id} not found")

        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity)
        db.session.add(order_item)

    db.session.commit()
    return Success(order.id)


@method
def get_orders():
    orders = Order.query.all()
    return Success([order.as_dict() for order in orders])


@method
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return Success(order.as_dict())
    else:
        return Error(message="Order not found", code="0432")


@method
def update_order(order_id, new_status):
    # current_user_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order:
        return jsonify(error="Order not found"), 404

    if not new_status:
        return jsonify(error="New status is required"), 400

    order.status = new_status
    db.session.commit()

    update_order_status.delay(order_id, new_status)

    return jsonify({"message": f"Order {order_id} status updated to {new_status}"}), 200


@method
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return Error("Order not found")

    db.session.delete(order)
    db.session.commit()
    return Success(f"Order {order_id} deleted")


@method
def create_role(name, description):
    role = Role(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    return Success(role.as_dict())


@method
def get_roles():
    roles = Role.query.all()
    return Success([role.as_dict() for role in roles])


@method
def get_role(role_id):
    role = Role.query.get(role_id)
    if role:
        return Success(role.as_dict())
    else:
        return Error("Role not found")


@method
def update_role(role_id, name=None, description=None):
    role = Role.query.get(role_id)
    if role:
        if name is not None:
            role.name = name
        if description is not None:
            role.description = description
        db.session.commit()
        return Success(role.as_dict())
    else:
        return Error("Role not found")


@method
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return Success(f"Role {role_id} deleted")
    else:
        return Error("Role not found")


@jwt_required
@app.route('/jsonrpc', methods=['POST'])
def jsonrpc():
    response = dispatch(request.data)
    return jsonify(response)


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
    celery.start()
