from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class ProductSizesQuantity(db.Model):
    __tablename__= 'product_sizes_quantity'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (db.UniqueConstraint('product_id', 'size_id', name='product_size_unique'),)
    # UniqueConstraint('user_id', 'planet_id', name='favorite_planets_unique')

    product = db.relationship("Product", back_populates="sizes_quantity")
    size = db.relationship("Size", back_populates="products")
    def serialize(self):
        return {
            "size": self.size.name,
            "quantity": self.quantity,
        }


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    # sizes_quantity = db.relationship(
    #     'Size', secondary='product_sizes_quantity', backref='product', lazy=True)
    sizes_quantity = db.relationship(
        'ProductSizesQuantity', back_populates='product')

    # children = relationship("Association", back_populates="parent")
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "sizes_quantity": [size_quantity.serialize() for size_quantity in self.sizes_quantity],
        }


class Size(db.Model):
    __tablename__ = 'sizes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    products = db.relationship(
        'ProductSizesQuantity', back_populates='size')
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

# product_sizes_quantity = db.Table('product_sizes_quantity',
#                                   db.Column('product_id', db.Integer,
#                                             db.ForeignKey('products.id'), ),
#                                   db.Column('size_id', db.Integer,
#                                             db.ForeignKey('sizes.id')),
#                                   db.Column('quantity', db.Integer,
#                                             nullable=False, default=0),
#                                   db.UniqueConstraint(
#                                       'product_id', 'size_id', name='product_sizes_quantity_unique')
#                                   )
