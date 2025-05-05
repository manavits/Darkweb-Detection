from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def _repr_(self):
        return f'<User {self.username}>'

class DarkWebThreat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    threat_description = db.Column(db.String(500), nullable=False)
    threat_category = db.Column(db.String(100), nullable=True)  # New field
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    _table_args_ = (
        db.Index('idx_threat_timestamp', 'timestamp'),
        db.Index('idx_threat_description', 'threat_description'),
    )

    def _repr_(self):
        return f'<Threat {self.url} - {self.threat_category} - {self.threat_description[:20]}>'








