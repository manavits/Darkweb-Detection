# change_password.py

import getpass
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

# Initialize Flask app context
app = create_app()

with app.app_context():
    email = input("Enter user email: ")
    user = User.query.filter_by(email=email).first()

    if user:
        new_password = getpass.getpass("Enter new password: ")
        confirm_password = getpass.getpass("Confirm new password: ")

        if new_password != confirm_password:
            print("Passwords do not match.")
        else:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            print("✅ Password updated successfully.")
    else:
        print("❌ User not found.")
