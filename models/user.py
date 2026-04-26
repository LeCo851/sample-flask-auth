from database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), nullable = False, unique = True)
    password = db.Column(db.String(80),nullable = False)
    role = db.Column(db.String(80), nullable = False, default = 'user')
    
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role