from extensions import db

class Atm(db.Model):
    __tablename__ = 'atm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    
    # Common fields often found in ATM datasets
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    bank_name = db.Column(db.String(255)) 

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "bank_name": self.bank_name
        }