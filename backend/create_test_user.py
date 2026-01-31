from app import app
from extensions import db
from model.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    existing_user = User.query.filter_by(email="test@test.com").first()
    
    if existing_user:
        print("User 'test@test.com' already exists!")
        existing_user.password_hash = generate_password_hash("abcd1234")
        db.session.commit()
        print("Password reset to 'abcd1234'.")
    else:
        new_user = User(
            email="test@test.com",
            password_hash=generate_password_hash("abcd1234")
            # REMOVED name="Test User" because your DB doesn't have it
        )
        
        db.session.add(new_user)
        db.session.commit()
        print("Success! User 'test@test.com' created.")