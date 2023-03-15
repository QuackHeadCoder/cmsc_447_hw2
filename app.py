import sqlite3

from flask import Flask, render_template, url_for, request, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret'




def db_init():
    db = sqlite3.connect('hw2.db')
    with open('schema.sql') as f:
        db.executescript(f.read())
    cur = db.cursor()
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Steve Smith','211',' 80'))
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Jian Wong','122',' 92'))
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Chris Peterson','213',' 91'))
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Sai Patel','524',' 94'))
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Andrew Whitehead','425',' 99'))
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Lynn Roberts','626',' 90'))
    cur.execute("INSERT INTO users (name, id, points) VALUES (?, ?, ?)",('Robert Sanders','287',' 75'))
    db.commit()
    db.close()



def get_user(id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = (?)', (id,)).fetchone()
    db.close()
    if user is None:
        abort(404)
    return user

def get_db():
    db = sqlite3.connect("hw2.db")
    db.row_factory = sqlite3.Row
    return db


@app.route('/', methods = ('GET', 'POST'))
def index():
    #just for displaying error msg
    error = False

    #read operation
    db = get_db()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()

    #create operation
    if request.method == 'POST':
        name = request.form.get('name')
        id = request.form.get('id',type=int)
        points = request.form.get('points',type=int)

        if not name or not id or not points:
            error = True

        else:
            db = get_db()
            db.execute('INSERT INTO users (name, id, points) VALUES (?,?,?)',(name,id,points))
            db.commit()
            db.close()
            return redirect(url_for('index'))

    return render_template('main.html', users=users, error=error)


@app.route('/<int:id>/edit/', methods = ('GET','POST'))
def edit(id):
    user = get_user(str(id))
    error = False

    if request.method == 'POST':
        name = request.form.get('name')
        id = request.form.get('id',type=int)
        points = request.form.get('points',type=int)

        if not name or not id or not points:
            error = True
        else:
            db = get_db()
            db.execute('UPDATE users SET name = ?, points = ?  WHERE id = ?',(name, points, id))
            db.commit()
            db.close()
            return redirect(url_for('index'))
            

    return render_template('edit.html', user=user, error=error)

@app.route('/delete/<int:id>')
def delete(id):
    print('runs')
    user = get_user(str(id))
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)