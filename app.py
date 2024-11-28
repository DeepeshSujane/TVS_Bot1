from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'breast cancer' 
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/bike')
def bike():
    return render_template('bike.html')

@app.route('/scoty')
def scoty():
    return render_template('product.html')

@app.route('/mop')
def mop():
    return render_template('mop.html')

@app.route('/three')
def three():
    return render_template('three.html')

@app.route('/elctric')
def electric():
    return render_template('electric.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['name'] = users['name']
            session['email'] = users['email']
            mesage = 'Logged in successfully!'
            return render_template('predict.html', mesage=mesage)
        else:
            mesage = 'Please enter correct email / password'
    return render_template('login.html', mesage=mesage)

@app.route('/register', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        usersName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  # Corrected email regex
            mesage = 'Invalid email address!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  # Corrected email regex
            mesage = 'Invalid email address!'
        elif not usersName or not password or not email:
            mesage = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', (usersName, email, password))

  # Corrected query syntax
            mysql.connection.commit()
            mesage = 'You have successfully registered!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form!'
    return render_template('register.html', mesage=mesage)

if __name__ == "__main__":
    app.secret_key = 'sanjana'  # Add secret key for session management
    app.run(debug=True)