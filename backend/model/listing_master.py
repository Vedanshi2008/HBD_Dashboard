# model/listing_master.py

from extensions import db
from sqlalchemy.sql import func


class ListingMaster(db.Model):
    __tablename__ = "listing_master"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    source = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
