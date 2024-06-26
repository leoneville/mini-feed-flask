from dataclasses import dataclass

from utils.models import OrmBase
from factory import db


@dataclass
class Role(db.Model):
    __tablename__ = 'role'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(64), unique=True,
                          nullable=False, index=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    can_access_sensitive_information = db.Column(db.Boolean, default=False)
    can_manage_users = db.Column(db.Boolean, default=False)
    can_manage_posts = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Role {self.name}>'


class RoleResponse(OrmBase):
    name: str
    can_access_sensitive_information: bool
    can_manage_users: bool
    can_manage_posts: bool
