from flask import *
from app import app, db

@app.route('/login', methods=['POST', 'GET'])
def login():
	pass