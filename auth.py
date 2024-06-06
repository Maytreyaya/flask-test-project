from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_security import verify_password, hash_password, SQLAlchemyUserDatastore
from models import Role, User
from database import db

auth_bp = Blueprint('auth', __name__)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

@auth_bp.route('/register', methods=['POST'])
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


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and verify_password(data['password'], user.password):
        access_token = create_access_token(identity=user.id)
        refresh = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token,refresh_token=refresh)
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200