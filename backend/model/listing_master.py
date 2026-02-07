from extensions import db
from datetime import datetime

class ListingMaster(db.Model):
    __tablename__ = 'listing_master_table'

    id = db.Column(db.Integer, primary_key=True)
    
    # Source is crucial (e.g., 'JustDial', 'GoogleMap', 'AskLaila')
    source = db.Column(db.String(50), nullable=False, index=True)
    
    # Basic Details
    business_name = db.Column(db.String(255), nullable=False, index=True)
    category = db.Column(db.String(255), index=True)
    sub_category = db.Column(db.String(255))
    owner_name = db.Column(db.String(255))
    
    # Contact Details
    mobile = db.Column(db.String(50), index=True)
    phone = db.Column(db.String(50))
    email = db.Column(db.String(150))
    website = db.Column(db.String(255))
    
    # Address Details
    address = db.Column(db.Text)
    city = db.Column(db.String(100), index=True)
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    area = db.Column(db.String(100))
    
    # Geolocation (Useful for Map View)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Platform Specifics
    rating = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    listing_url = db.Column(db.Text)
    
    # Metadata
    image_url = db.Column(db.Text)
    description = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "business_name": self.business_name,
            "category": self.category,
            "mobile": self.mobile,
            "email": self.email,
            "city": self.city,
            "rating": self.rating,
            "address": self.address
        }