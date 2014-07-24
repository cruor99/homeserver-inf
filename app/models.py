__author__ = 'cruor'

from app import db
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import *

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    usermail = db.Column(db.String(64), unique=True)
    pwdhash = db.Column(db.String(120))
    last_login = db.Column(db.DATETIME)

    def __init__(self, username, password, usermail):
        self.username = username
        self.pwdhash = generate_password_hash(password)
        self.usermail = usermail

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return '%s' %(self.username)