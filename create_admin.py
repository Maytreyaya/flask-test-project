# from app import db, user_datastore, app
# from models import Role, User
# from flask_security.utils import hash_password
# import uuid
#
#
# # Create an application context
# def create_admin_user():
#     with app.app_context():
#         # Create an admin user
#         admin_user = user_datastore.create_user(email='admin56@example.com',
#                                                 password=hash_password('adminpassword'),
#                                                 role="admin")
#
#         # Assign the 'admin' role to the admin user
#         user_datastore.add_role_to_user(admin_user, 'admin')
#
#         # Commit the changes
#         db.session.commit()