from flask import *
import sqlite3 as sq

app = Flask(__name__)


@app.route("/")
def index(name=None):
    return render_template('index.html', error='')

@app.route("/account", methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        with sq.connect("db.db") as con:
            cur = con.cursor()
            get = cur.execute(f"SELECT login, password FROM users WHERE login == '{login}'")
            print(get.fetchone())
            if get.fetchone() is None:
                cur.execute(f"INSERT INTO users VALUES (?, ?)", (login, password))
                print(get.fetchone())
                return render_template('account.html', login=login)
            else:
                if get.fetchone()[2] == password:
                    print(get.fetchone())
                    return render_template('account.html', login=login)

                else:
                    return render_template('index.html', error='No password')


@app.route("/news")
def news(name=None):
    return render_template('news.html', name=name)

app.run()