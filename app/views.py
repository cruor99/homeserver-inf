from flask import *
from flask.ext.login import logout_user
from app import app, db
from models import User

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print request.form['password']
        user = User.query.filter_by(username=request.form['username']).first()
        if user is not None and user.check_password(request.form['password']):

            session['logged_in'] = True
            session['username'] = user.username
            session['usermail'] = user.usermail
            return redirect(url_for('index'))
        else:
            flash('Wrong Username or Password')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        form_user = request.form['username']
        form_email = request.form['usermail']
        exiname = User.query.filter_by(username=form_user).first()
        eximail = User.query.filter_by(usermail=form_email).first()
        if eximail or exiname is not None:
            flash('Username or Email already exists')
            return render_template('signup.html')
        else:
            password = request.form['password']
            print password
            user = User(form_user, password, form_email)
            db.session.add(user)
            db.session.commit()
            flash('You are now registered, please log in')
            return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('usermail', None)
    return redirect(url_for('login'))