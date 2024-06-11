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
        if 'admin' not in current_user.roles:
            return jsonify(error="Permission denied"), 403
        return func(*args, **kwargs)
    return decorated_function


@method
def get_products() -> list[dict]:
    products = Product.query.all()
    return Success([product.as_dict() for product in products])


@method
def get_product(product_id: int) -> dict:
    product = Product.query.get(product_id)
    if product:
        return Success(product.as_dict())
    else:
        return Error("Product not found", code="0432")


@method
@jwt_required()
def create_product(name: str,
                   price: float,
                   weight: float,
                   color: str) -> dict:

    product = Product(name=name,
                      price=price,
                      weight=weight,
                      color=color)
    db.session.add(product)
    db.session.commit()
    return Success(product.as_dict())


@method
@jwt_required()
@admin_required
def update_product(product_id: int,
                   name: str = None,
                   price: float = None) -> dict:
    product = Product.query.get(product_id)
    if product:
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        db.session.commit()
        return Success(product.as_dict())
    else:
        return Error("Product not found", code="0432")


@method
@jwt_required()
@admin_required
def delete_product(product_id: int) -> str:
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return Success(f"Product {product_id} deleted")
    else:
        return Error("Product not found", code="0432")


@method
@jwt_required()
def create_address(country: str,
                   city: str,
                   street: str) -> dict:

    address = Address(country=country,
                      city=city,
                      street=street)

    db.session.add(address)
    db.session.commit()
    return Success(address.as_dict())


@method
@jwt_required()
def create_order(address_id: int,
                 status: str,
                 order_items: list[dict]) -> dict:

    address = Address.query.get(address_id)
    if not address:
        return Error("Address not found", code="0432")

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
def get_orders() -> list[dict]:
    orders = Order.query.all()
    return Success([order.as_dict() for order in orders])


@method
def get_order(order_id) -> dict:
    order = Order.query.get(order_id)
    if order:
        return Success(order.as_dict())
    else:
        return Error(message="Order not found", code="0432")


@method
@jwt_required()
@admin_required
@shared_task
def update_order(order_id: int, new_status: str) -> str:

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
@jwt_required()
@admin_required
def delete_order(order_id) -> str:
    order = Order.query.get(order_id)
    if not order:
        return Error("Order not found")

    db.session.delete(order)
    db.session.commit()
    return Success(f"Order {order_id} deleted")


@method
@jwt_required()
def create_role(name: str, description: str) -> dict:
    role = Role(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    return Success(role.as_dict())


@method
def get_roles() -> list[dict]:
    roles = Role.query.all()
    return Success([role.as_dict() for role in roles])


@method
def get_role(role_id: int) -> dict:
    role = Role.query.get(role_id)
    if role:
        return Success(role.as_dict())
    else:
        return Error("Role not found", code="0432")


@method
@jwt_required()
@admin_required
def update_role(role_id: int,
                name: str = None,
                description: str = None):
    role = Role.query.get(role_id)
    if role:
        if name is not None:
            role.name = name
        if description is not None:
            role.description = description
        db.session.commit()
        return Success(role.as_dict())
    else:
        return Error("Role not found", code="0432")


@method
@jwt_required()
@admin_required
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return Success(f"Role {role_id} deleted")
    else:
        return Error("Role not found", code="0432")


@jwt_required()
@jsonrpc_bp.route('/jsonrpc', methods=['POST'])
def jsonrpc():
    response = dispatch(request.data)
    return jsonify(response)

