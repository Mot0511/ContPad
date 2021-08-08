from flask import *
import sqlite3 as sq
import random
import os

app = Flask(__name__, static_folder="static")


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
        post_names = []
        file_names = []
        login = request.form.get('login')
        password = request.form.get('password')
        with sq.connect('db.db') as con:
            cur = con.cursor()
            get = cur.execute(f"SELECT login, password FROM users WHERE login == '{login}'")
            if get.fetchone()[1] == password:
            
                posts = cur.execute(f"SELECT name FROM posts WHERE login == '{login}'")
                if not(posts == []):
                    for i in posts:
                        post_names.append(i[0])
                        
                if post_names == []:
                    post_names.append('Posts is not found')
                    
                for i in post_names:
                    file_names.append(i.replace('', '_'))
                    
                print(file_names)
                
                return render_template('account.html', login=login, post_names=post_names, file_names=file_names)

            else:
                return render_template('index.html', error='No password')

@app.route("/news")
def news(name=None):
    return render_template('news.html', name=name)

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import sys

UPLOAD_FOLDER = 'static/post_images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
def read_img(n):
    try:
        with open(n, "rb") as f:
            return f.read()
    except IOError as e:
        print(e)
        return False
        
@app.route('/public', methods=['GET', 'POST'])
def upload_file():
    name = request.form.get('name')
    login = request.form.get('login')
    post_names = []
    number = random.randint(0, 100000)
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
        filename = secure_filename(name + '.png')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        with sq.connect('db.db') as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO posts VALUES (?, ?)", (login, name))
            posts = cur.execute(f"SELECT name FROM posts WHERE login == '{login}'")
            if not(posts == []):
                for i in posts:
                    post_names.append(i[0])
                    
            
            return render_template('account.html', login=login, post_names=post_names)
            

        
        

app.run()
