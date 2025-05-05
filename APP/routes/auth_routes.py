from flask import Blueprint, request, render_template, redirect, url_for, flash, make_response, current_app
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required
from app.models import User
from app import db
from datetime import timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Blueprint declaration
auth = Blueprint('auth', __name__)

# Rate limiting setup
limiter = Limiter(get_remote_address, app=current_app, default_limits=["10 per minute"])

# --------------------------
# LOGIN ROUTE
# --------------------------
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            # Fix: Convert user.id to string for JWT token
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
            response = make_response(redirect(url_for('admin.dashboard')))  # Ensure this route exists
            set_access_cookies(response, access_token)
            flash("Login successful!", "success")
            return response

        flash('Invalid credentials. Please try again.', 'danger')
        return render_template('auth/login.html')

    return render_template('auth/login.html')


# --------------------------
# LOGOUT ROUTE
# --------------------------
@auth.route('/logout')
@jwt_required()
def logout():
    # Clear JWT from cookies
    response = make_response(redirect(url_for('auth.login')))
    unset_jwt_cookies(response)
    flash("You have been logged out successfully.", "info")
    return response
