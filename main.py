from flask import *
import sqlite3 as sq
import random

app = Flask(__name__)


@app.route("/")
def index(name=None):
    return render_template('index.html', error='')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        with sq.connect('db.db') as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO users VALUES (?, ?)", (login, password))
            return render_template('account.html', login=login)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        with sq.connect('db.db') as con:
            cur = con.cursor()
            get = cur.execute(f"SELECT login, password FROM users WHERE login == '{login}'")
            if get.fetchone()[1] == password:
                return render_template('account.html', login=login)

            else:
                return render_template('index.html', error='No password')

@app.route("/news")
def news(name=None):
    return render_template('news.html', name=name)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        img = 'img'
        number = random.randint(0, 100000)
        img = sq.Binary(open(str(number) + '.png', 'rb').read())
        print(img)
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(number) + '.png')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with sq.connect('db.db') as con:
                cur = con.cursor()
                get = cur.execute("INSERT INTO posts VALUES (?, ? ,?)", (login, name, img))
                return render_template('account.html', login=login)
    

app.run()
