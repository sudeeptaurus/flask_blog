from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from flask_mail import Mail

with open('config.json', 'r') as c:
    params = json.load(c) ["params"]

local_server = True
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD = params['gmail-password']
)
mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)

class Contacts(db.Model):
    # sno, name, email, phone_num, message, date

    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone_num = db.Column(db.String(20), unique=False, nullable=False)
    message = db.Column(db.String(120), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True)

class Posts(db.Model):
    # sno, name, email, phone_num, message, date

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    slug = db.Column(db.String(25), unique=False, nullable=False)
    content = db.Column(db.String(200), unique=False, nullable=False)
    tagline = db.Column(db.String(100), unique=False, nullable=False)
    img_file = db.Column(db.String(20), unique=False, nullable=False)
    date = db.Column(db.String(20), unique=False, nullable=True)


@app.route('/')
def home():
    posts = Posts.query.filter_by().all() [0:params['no_of_posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', params=params)

@app.route('/post/<string:post_slug>', methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=params, post=post)


@app.route('/contact', methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        # Add entry to database
        name = request.form.get('name')
        email = request.form.get('email')
        phone_num = request.form.get('phone_num')
        message = request.form.get('message')

        entry = Contacts(name = name, phone_num = phone_num, message = message, date = datetime.now(), email = email)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name, sender=email, recipients= [params['gmail-user']], body = message + "\n" + phone_num)

    return render_template('contact.html', params=params)

app.run(debug=True)
