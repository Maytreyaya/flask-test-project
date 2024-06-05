#
# from models import db, Order
# from app import app, celery
#
#
# @celery.task
# def update_order_status(order_id, new_status):
#     with app.app_context():
#         order = Order.query.get(order_id)
#         if order:
#             order.status = new_status
#             db.session.commit()
#             with open('celery.log', 'a') as log_file:
#                 log_file.write(f'Order {order_id} changed status to {new_status}\n')