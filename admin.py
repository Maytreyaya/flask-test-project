from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Role, Product, Address, Order, OrderItem, db


class AdminModelView(ModelView):
    @jwt_required()
    def is_accessible(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user and "admin" in user.roles[0].name:
            return True
        return False


def setup_admin(app):

    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Role, db.session))
    admin.add_view(AdminModelView(Product, db.session))
    admin.add_view(AdminModelView(Address, db.session))
    admin.add_view(AdminModelView(Order, db.session))
    admin.add_view(AdminModelView(OrderItem, db.session))