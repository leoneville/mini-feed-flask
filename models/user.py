from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime, date

from pydantic.v1 import BaseModel, EmailStr, SecretStr
from werkzeug.security import generate_password_hash, check_password_hash

from factory import db
from utils.models import OrmBase


@dataclass
class User(db.Model):
    __tablename__ = 'user'

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(
        db.String(64), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(128), index=True)
    email: str = db.Column(db.String(128), unique=True,
                           nullable=False, index=True)
    birthdate: date = db.Column(db.Date)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<User: {self.username}>'

    def as_dict(self):
        unprinted_attr = ['password_hash']
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in unprinted_attr}

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)


class UserEdit(BaseModel):
    username: str
    email: EmailStr
    birthdate: Optional[date]


class UserCreate(UserEdit):
    password: SecretStr


class UserResponse(OrmBase):
    username: str
    email: EmailStr
    birthdate: Optional[date]
    created_at: datetime


class UserResponseList(BaseModel):
    __root__: List[UserResponse]
