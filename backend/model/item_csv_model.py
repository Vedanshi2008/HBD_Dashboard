# model/item_csv_model.py

from extensions import db
from sqlalchemy.sql import func


class ItemData(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # REQUIRED
    name = db.Column(db.String(255), nullable=False)

    # OPTIONAL TEXT FIELDS
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(255), nullable=True)
    sub_category = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    area = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # CONTACTS
    phone_no_1 = db.Column(db.String(50), nullable=True)
    phone_no_2 = db.Column(db.String(50), nullable=True)
    phone_no_3 = db.Column(db.String(50), nullable=True)
    whatsapp_no = db.Column(db.String(50), nullable=True)
    virtual_phone_no = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)

    # SOCIAL
    facebook_url = db.Column(db.Text, nullable=True)
    linkedin_url = db.Column(db.Text, nullable=True)
    twitter_url = db.Column(db.Text, nullable=True)

    # META
    source = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    reviews = db.Column(db.Text, nullable=True)

    # NUMERIC
    ratings = db.Column(db.Float, nullable=True)
    avg_spent = db.Column(db.Float, nullable=True)
    cost_for_two = db.Column(db.Float, nullable=True)
    pincode = db.Column(db.Integer, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    price = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
