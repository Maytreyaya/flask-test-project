from functools import wraps
from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from jsonrpcserver import method, Success, Error, dispatch
from models import Product, Address, Order, OrderItem, Role, User
from database import db
import logging
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

jsonrpc_bp = Blueprint('jsonrpc', __name__)


@jwt_required
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if 'adminn' not in current_user.roles:
            return jsonify(error="Permission denied"), 403
        return func(*args, **kwargs)
    return decorated_function


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
@admin_required
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
@admin_required
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
@admin_required
@shared_task
def update_order(order_id, new_status):
    # current_user_id = get_jwt_identity()
    order = Order.query.get(order_id)

    if not order:
        return Error(message="Order not found", code='0432')

    if not new_status:
        return Error(message="New status is required")

    order.status = new_status

    logging.basicConfig(filename='celery.log', level=logging.INFO)
    log_message = f"Order {order_id} changed status to {new_status}."
    logger.info(log_message)

    db.session.commit()

    return Success(f"Order {order_id} status updated to {new_status}")


@method
@admin_required
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
@admin_required
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
@admin_required
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return Success(f"Role {role_id} deleted")
    else:
        return Error("Role not found")


@jwt_required
@jsonrpc_bp.route('/jsonrpc', methods=['POST'])
def jsonrpc():
    response = dispatch(request.data)
    return jsonify(response)

