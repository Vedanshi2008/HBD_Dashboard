from extensions import db
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

class AmazonProduct(db.Model):
    __tablename__ = "amazon_products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ASIN = db.Column(db.String(20), unique=True, nullable=True)
    Product_name = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(50), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    Number_of_ratings = db.Column(db.Integer, nullable=True)
    Brand = db.Column(db.String(255), nullable=True)
    Seller = db.Column(db.String(255), nullable=True)
    
    # Allow nulls for these fields so the scraper doesn't crash if data is missing
    category = db.Column(db.String(255), nullable=True)
    subcategory = db.Column(db.String(255), nullable=True)
    sub_sub_category = db.Column(db.String(255), nullable=True)
    category_sub_sub_sub = db.Column(db.String(255), nullable=True)
    
    colour = db.Column(db.String(255), nullable=True)
    size_options = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    link = db.Column(db.Text, nullable=True)
    Image_URLs = db.Column(db.Text, nullable=True)
    About_the_items_bullet = db.Column(db.Text, nullable=True)
    
    Product_details = db.Column(JSON, nullable=True)
    Additional_Details = db.Column(JSON, nullable=True)
    
    Manufacturer_Name = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "ASIN": self.ASIN,
            "Product_name": self.Product_name,
            "price": self.price,
            "rating": self.rating,
            "Number_of_ratings": self.Number_of_ratings,
            "Brand": self.Brand,
            "link": self.link,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }