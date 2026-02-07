from extensions import db

class Asklaila(db.Model):
    __tablename__ = 'asklaila'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    number1 = db.Column(db.String(50))
    number2 = db.Column(db.String(50))
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    email = db.Column(db.String(150))
    url = db.Column(db.Text)
    ratings = db.Column(db.String(10))
    address = db.Column(db.Text)
    pincode = db.Column(db.String(20))
    area = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # --- Newly Added Fields from Screenshot ---
    source = db.Column(db.String(50))
    name_address_city_hash = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number1": self.number1,
            "number2": self.number2,
            "category": self.category,
            "subcategory": self.subcategory,
            "email": self.email,
            "url": self.url,
            "ratings": self.ratings,
            "address": self.address,
            "pincode": self.pincode,
            "area": self.area,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "source": self.source,
            "name_address_city_hash": self.name_address_city_hash,
            
            # Frontend Mapping (Convenience)
            "phone_number": self.number1 
        }