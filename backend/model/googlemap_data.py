# model/googlemap_data.py

from extensions import db
from sqlalchemy.sql import func


class GooglemapData(db.Model):
    __tablename__ = "businesses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(500), nullable=True)
    address = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(500), nullable=True)
    phone_number = db.Column(db.String(100), nullable=True)

    reviews_count = db.Column(db.Integer, nullable=True)
    reviews_average = db.Column(db.Float, nullable=True)

    category = db.Column(db.String(255), nullable=True)
    subcategory = db.Column(db.String(500), nullable=True)

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
