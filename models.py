from database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(30))
    weight = db.Column(db.Float)
    price = db.Column(db.Float)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(80))
    city = db.Column(db.String(80))
    street = db.Column(db.String(120))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    address = db.relationship('Address', backref=db.backref('orders', lazy=True))
    status = db.Column(db.String(20))
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
                       )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    fs_uniquifier = db.Column(db.String(255),
                              unique=True,
                              nullable=False)
    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
