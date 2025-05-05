import sys
from getpass import getpass
from app import create_app
from app.models import db, User

def prompt_input(prompt, hidden=False):
    try:
        return getpass(prompt) if hidden else input(prompt)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)

def main():
    app = create_app()

    with app.app_context():
        db.create_all()

        username = prompt_input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty.")
            return

        if User.query.filter_by(username=username).first():
            print(f"User '{username}' already exists.")
            return

        password = prompt_input("Enter password: ", hidden=True).strip()
        confirm_password = prompt_input("Confirm password: ", hidden=True).strip()

        if not password:
            print("Password cannot be empty.")
            return
        if password != confirm_password:
            print("Passwords do not match.")
            return

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        print(f"✅ User '{username}' created successfully.")

if __name__ == '__main__':
    main()

