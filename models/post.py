from dataclasses import dataclass
from datetime import datetime

from factory import db


@dataclass
class Post(db.Model):
    __tablename__ = 'post'

    id: int = db.Column(db.Integer, primary_key=True)
    text: str = db.Column(db.UnicodeText)
    created: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    author_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<Post: {self.id}>'
