import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://tejas:HL5PHNfcuoPwourxKKLvhG6VIMGhbjbs@dpg-cv6mauan91rc73bgi1d0-a:5432/test_db_rfl6'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


#### 4. **Models (models.py)**
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ActionHub(db.Model):
    ah_id = db.Column(db.Integer, primary_key=True)
    ah_type = db.Column(db.String(50), nullable=False)
    ah_report_id = db.Column(db.Integer, nullable=False)
    ah_user_id = db.Column(db.Integer, nullable=False)
    ah_content = db.Column(db.Text)
    ah_created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ah_updated_at = db.Column(db.DateTime)
    ah_status = db.Column(db.SmallInteger, default=1, nullable=False)
    ah_parent_id = db.Column(db.Integer)
    ah_mentioned_user_id = db.Column(db.Integer)
    ah_is_read = db.Column(db.Boolean, default=False)
    ah_section_id = db.Column(db.Integer)
    ah_subsection_id = db.Column(db.Integer)
    ah_last_read_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<ActionHub {self.ah_id}>'