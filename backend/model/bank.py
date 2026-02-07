from extensions import db

class Bank(db.Model):
    __tablename__ = 'bank_data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))         # e.g., "HDFC Bank"
    branch = db.Column(db.String(255))       # e.g., "Indrapuri Branch"
    ifsc = db.Column(db.String(50))          # e.g., "HDFC0001234"
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    contact = db.Column(db.String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "branch": self.branch,
            "ifsc": self.ifsc,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "pincode": self.pincode,
            "contact": self.contact
        }