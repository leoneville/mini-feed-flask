from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass

from pydantic.v1 import BaseModel

from factory import db
from utils.models import OrmBase


@dataclass
class Post(db.Model):
    __tablename__ = 'post'

    id: int = db.Column(db.Integer, primary_key=True)
    text: str = db.Column(db.UnicodeText)
    created: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    author_id: int = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self) -> str:
        return f'<Post: {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class PostCreate(BaseModel):
    text: str


class PostResponse(OrmBase):
    text: str
    author_id: int
    created: datetime


class PostResponseList(BaseModel):
    page: int
    pages: int
    total: int
    posts: List[PostResponse]


class SearchModel(BaseModel):
    search: Optional[str]
    reverse: Optional[bool] = False
    page: Optional[int] = 1
    per_page: Optional[int] = 10
