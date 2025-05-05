import os
from datetime import timedelta

class Config:
    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///darkweb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'darkashish47@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'Ashishthapa@123')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Twilio Configuration (Optional)
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+1234567890')
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'your_sid')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'your_auth_token')

    # Scan Configuration
    SCAN_INTERVAL_SECONDS = int(os.environ.get('SCAN_INTERVAL_SECONDS', 1800))  # 30 minutes
    SCAN_KEYWORDS = os.environ.get('SCAN_KEYWORDS',
        "password leak,credit card,ransomware,exploit,hacked email,black market,hacking,drugs,guns"
    ).split(',')

    # JWT Configurations
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE', 'False') == 'True'
    JWT_COOKIE_CSRF_PROTECT = os.environ.get('JWT_COOKIE_CSRF_PROTECT', 'False') == 'True'
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # Other
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_DURATION = timedelta(days=7)


# --------------------------
# Config Validator
# --------------------------
def validate_config(app):
    required_keys = ['SECRET_KEY', 'JWT_SECRET_KEY', 'SQLALCHEMY_DATABASE_URI']
    for key in required_keys:
        if not app.config.get(key):
            raise RuntimeError(f"Missing required config: {key}")
    
    # Additional validation for optional but necessary configurations
    if app.config['SCAN_KEYWORDS'] is None or len(app.config['SCAN_KEYWORDS']) == 0:
        raise RuntimeError("SCAN_KEYWORDS must be a non-empty string with at least one keyword.")
    
    if app.config['MAIL_USERNAME'] is None or app.config['MAIL_PASSWORD'] is None:
        raise RuntimeError("MAIL_USERNAME and MAIL_PASSWORD must be set for email functionality.")

    if not app.config.get('TWILIO_PHONE_NUMBER') or not app.config.get('TWILIO_ACCOUNT_SID') or not app.config.get('TWILIO_AUTH_TOKEN'):
        print("Warning: Twilio configuration is missing. SMS functionalities will not work.")
