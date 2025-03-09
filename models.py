from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class ActionHub(db.Model):
    __tablename__ = 'gra_action_hub'

    ah_id = db.Column(db.Integer, primary_key=True)
    ah_type = db.Column(db.String(50), nullable=False)
    ah_report_id = db.Column(db.Integer, nullable=False)
    ah_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ah_content = db.Column(JSON)
    ah_created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ah_updated_at = db.Column(db.DateTime)
    ah_status = db.Column(db.SmallInteger, default=1, nullable=False)
    ah_parent_id = db.Column(db.Integer)
    ah_mentioned_user_id = db.Column(db.Integer)
    ah_is_read = db.Column(db.Boolean, default=False)
    ah_section_id = db.Column(db.Integer)
    ah_subsection_id = db.Column(db.Integer)
    ah_last_read_id = db.Column(db.Integer)
    user = db.relationship('User', backref='actions')

    def to_dict(self):
        return {
            'ah_id': self.ah_id,
            'ah_type': self.ah_type,
            'ah_report_id': self.ah_report_id,
            'ah_user_id': self.ah_user_id,
            'username': self.user.username if self.user else 'Anonymous',
            'ah_content': self.ah_content,
            'ah_created_at': self.ah_created_at.isoformat(),
            'ah_updated_at': self.ah_updated_at.isoformat() if self.ah_updated_at else None,
            'ah_status': self.ah_status,
            'ah_parent_id': self.ah_parent_id,
            'ah_mentioned_user_id': self.ah_mentioned_user_id,
            'ah_is_read': self.ah_is_read,
            'ah_section_id': self.ah_section_id,
            'ah_subsection_id': self.ah_subsection_id,
            'ah_last_read_id': self.ah_last_read_id
        }

    def __repr__(self):
        return f'<ActionHub {self.ah_id}>'