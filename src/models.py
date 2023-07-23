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
        }

class ProductSizesQuantity(db.Model):
    __tablename__= 'product_sizes_quantity'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    size_id = db.Column(db.Integer, db.ForeignKey('sizes.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (db.UniqueConstraint('product_id', 'size_id', name='product_size_unique'),)

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
    sizes_quantity = db.relationship(
        'ProductSizesQuantity', back_populates='product')

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

