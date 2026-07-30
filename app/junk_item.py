from app import db
from datetime import datetime


class JunkItem(db.Model):
    __tablename__ = 'junk_item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='pending')
    condition = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photo_filename = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<JunkItem {self.name}>'
