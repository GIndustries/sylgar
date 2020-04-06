from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from pythonFiles.forms import LoginForm, RegistrationForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://default:default@localhost/flaskUser'
    
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pymenwkussgixx:4f3cc8043b523110a386ea069e292eaadd6cdeb3755f2e4a22fc0f6ee13bfb9d@ec2-18-235-20-228.compute-1.amazonaws.com:5432/d4v6tgt8p6e93k'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False) #postgres is set up at character[64]
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email})"

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        textbox = request.form['textbox']
        drop_menu = request.form['dropMenu']
        rating = request.form['rating']
        text_area = request.form['textArea']
        print(textbox, drop_menu, rating, text_area)
        return render_template('success.html')

@app.route('/video_stream')
def video_stream():
    return render_template('video-stream.html')

#==========================================================================================================
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'admin':
            flash(f'Successful login for {form.username.data}!', 'success')
            return redirect('index')
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect('index')
    return render_template('register.html', form=form)
#==========================================================================================================

if __name__ == '__main__':
    app.run()