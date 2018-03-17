import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#application instance
app = Flask(__name__)
app.config.from_object(__name__) # load configs from flask_demo.py
app.secret_key = 'development key'
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('/Users/c100-60/Desktop/FLASK_DEMO/flask_demo/flask_demo/flask_demo.db')
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.route('/')
def show_entries():
    if session.get('logged_in'):
        u = session['u_name']
    else:
        return redirect(url_for('add_std'))

    db = get_db()
    cur = db.execute('select id,title, text, u_name from fi')
    fi = cur.fetchall()
        
    return render_template('show_detail.html',fi=fi,u=u)


@app.route('/add_std', methods=['GET', 'POST'])
def add_std():
    #print(request.method)
    try:
        #print("in try block")
        name = request.form['name']
        username = request.form['uname']
        password = request.form['passw']
        cpassword = request.form['cpass']  
        email = request.form['email']  

        db = get_db()
        db.execute('insert into user (name,username,password,c_password,email) values (?,?,?,?,?)',(name,username,password,cpassword,email))
        db.commit()
        flash("Record successfully added")
        session['reg']=True
        return redirect(url_for('login'))
    except:
        error = 'can not call the view'

    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    c = 0
    if not session.get('reg'):
        error = None
    if request.method == 'POST':
        db = get_db()
        cur = db.execute('select username,password from user')
        a = cur.fetchall()
        db.commit()
        print(a)
        #for i in a:
            #print(i['username'])
            #print(i['password'])

        for i in a:
            if(request.form['username']==i['username']):
                if(request.form['password']==i['password']):
                    c=1

        if(c==1):
            session['logged_in'] = True
            session['u_name'] = request.form['username']
            u= session['u_name']
            flash('You were logged in')
            return redirect(url_for('add_entry'))
        
    #return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':  
        u= session['u_name']  
        db = get_db()
        db.execute('insert into fi (title, text,u) values (?, ?, ?)',[request.form['title'], request.form['text'],u])
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('add_entry'))

    return render_template('list.html')

@app.route('/edit/<a>/', methods=['GET', 'POST'])
def edit(a):
    print("helli")
    print(a)
    print("hello",session.get('logged_in'))
    if session.get('logged_in'):
        u = session['u_name']
        db = get_db()
        fi = db.execute('select * from fi where id=%s' % (a))
        return render_template('update.html',fi=fi,a=a)
    return redirect(url_for('show_entries'))

@app.route('/update/<a>/',methods=['GET', 'POST'])
def update(a):
    if request.method == 'POST':
        print(a)
        print(request.form['title'])
        print(request.form['text'])
        db = get_db()
        db.execute('update fi set title=?,text=? where id=?',(request.form['title'],request.form['text'],a))
        db.commit()
        return redirect(url_for('show_entries'))
    return render_template('update.html',a=a)

@app.route('/delete/<de>/',methods=['GET', 'POST'])
def delete(de):
    if session.get('logged_in'):
        print(de)
        db = get_db()
        db.execute('delete from fi where id=%s' %(de))
        db.commit()
        return redirect(url_for('show_entries'))

    return redirect(url_for('show_entries'))

