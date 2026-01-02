# model/amazon_product_model.py

from extensions import db
from sqlalchemy.sql import func


class AmazonProduct(db.Model):
    __tablename__ = "amazon_products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    asin = db.Column(db.String(20), unique=True, nullable=True)
    product_name = db.Column(db.Text, nullable=False)

    price = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    number_of_ratings = db.Column(db.Integer, nullable=True)

    brand = db.Column(db.String(255), nullable=True)
    seller = db.Column(db.String(255), nullable=True)

    category = db.Column(db.String(255), nullable=True)
    subcategory = db.Column(db.String(255), nullable=True)
    sub_sub_category = db.Column(db.String(255), nullable=True)
    category_sub_sub_sub = db.Column(db.String(255), nullable=True)

    colour = db.Column(db.String(255), nullable=True)
    size_options = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)

    link = db.Column(db.Text, nullable=True)
    image_urls = db.Column(db.Text, nullable=True)
    about_the_items_bullet = db.Column(db.Text, nullable=True)

    product_details = db.Column(db.JSON, nullable=True)
    additional_details = db.Column(db.JSON, nullable=True)

    manufacturer_name = db.Column(db.String(500), nullable=True)

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )
