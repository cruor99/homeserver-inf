from flask import *
from flask.ext.login import logout_user
from app import app, db
from models import User
import subprocess
import os
from threading import Thread

subprocess.call(['export DISPLAY=:0.0'], shell=True)

def make_tree(path):
    tree = dict(name=path, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=fn))
    return tree

def playpause():
    print "test"
    subprocess.call("./playpause.sh")

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
    if request.method == "POST" and request.form["submit"] == "playpause":
        playpause()
    if request.method == 'POST' and request.form['submit'] == "Start Stream":
        subprocess.call(["pkill", "vlc"])
        stream = request.form['streamlink']
        thr = Thread(target = startStream, args = (str(stream),))
        thr.start()
        flash("Stream: " + stream + " started")
    if request.method == "POST" and request.form["submit"] == "Youtube":
        thr = Thread(target = startVideo, args = (str(request.form['streamlink']),))
        thr.start()
        flash("Youtube clip: " + str(request.form['streamlink']) + " started")
        return render_template('index.html')
    if request.method == "POST" and request.form["submit"] == "Kill vlc":
        subprocess.call(["pkill", "vlc"])
        flash("VLC stopped")

    return render_template('index.html')

def startStream(stream):
    subprocess.call(["livestreamer", stream, "best", "-p", "vlc -f"])

def startVideo(video):
    subprocess.call(['vlc', '-f', video])
    print video

@app.route('/videos', methods=['POST', 'GET'])
def video():
    item = request.args.get('p')
    print item
    print type(item)
    extensions = ['.mp4', '.m4v','.mkv','.avi']
    if item is not None:
        if item.endswith(tuple(extensions)):
            thr = Thread(target = startVideo, args=(str(item),))
            flash('Video started')
            thr.start()
            return redirect('/')
        else:
            webtree = make_tree(item)
    else:
        webtree = make_tree('/home/liknesserver/Videos/')
    return render_template('videos.html', webtree = webtree)

@app.route('/logout', methods=['post', 'get'])
def logout():
    logout_user()
    session.pop('logged_in', none)
    session.pop('username', none)
    session.pop('usermail', none)
    return redirect(url_for('login'))
