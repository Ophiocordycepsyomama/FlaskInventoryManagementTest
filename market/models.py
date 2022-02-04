from market import db

class Product(db.Model):
    product_id = db.Column(db.String(length=30), primary_key=True)
    qnty = db.Column(db.Integer(), nullable=False, default=1)
    def __repr__(self):
        return f'{self.product_id}|{self.qnty}'

class Location(db.Model):
    location_id = db.Column(db.String(length=30), primary_key=True)
    storage = db.Column(db.Text(length=1000), primary_key=True)
    def __repr__(self):
        return f'{self.location_id}'

class ProductMovement(db.Model):
    movement_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    timestamp = db.Column(db.String(length=30))
    from_location = db.Column(db.String(length=30), nullable=False)
    to_location = db.Column(db.String(length=30), nullable=False)
    product_id = db.Column(db.String(length=30),nullable=False)
    qty = db.Column(db.Integer(), nullable=False, default=1)

    def __repr__(self):
        return f'{self.movement_id}'