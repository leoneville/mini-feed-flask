from flask import jsonify
from main import app
from factory import db
from datetime import datetime
from models import User


with app.app_context():
    user = User.query.all()
    print(jsonify(user))