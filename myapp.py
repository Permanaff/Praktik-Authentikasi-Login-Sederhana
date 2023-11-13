from flask import Flask, render_template, session, request , redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '!@#$%'

app.config['MYSQL_HOST'] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"]= ''
app.config["MYSQL_DB"] = 'responsipwp'

mysql = MySQL(app)

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'inpUsername' in request.form and 'inpPass' in request.form:
        username = request.form['inpUsername']
        passwd = request.form['inpPass']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users where username = %s and password = %s", (username, passwd))
        result = cur.fetchone()
        cur.close()

        if result:
            session['is_logged_in'] = True
            session['username'] = result[0]
            return redirect(url_for('home'))
        else:
            error_message = "Login Gagal. Username atau password tidak valid."
            flash(error_message, 'error')
            return redirect(url_for('login', error='Login Gagal'))
    else:
        return render_template('login.html')
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST" and "inpUser" in request.form and "inpPass" in request.form:
        nama = request.form['inpnama']
        nim = request.form['inpnim']
        username = request.form["inpUser"]
        passwd = request.form["inpPass"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users where username = %s ", (username,))
        result = cur.fetchone()
        cur.close()

        if result:
            error_message = "Username sudah digunakan."
            flash(error_message, 'error')
            return redirect(url_for('register', error='register Gagal'))

        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO users (nama, nim, username, password) VALUES (%s, %s, %s, %s)", (nama, nim, username, passwd))
            mysql.connection.commit()
            return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/home')
def home():
    if 'is_logged_in' in session : 
        username = session['username']

        cur = mysql.connection.cursor()
        cur.execute("SELECT nama, nim FROM users WHERE username=%s", (username,))
        data = cur.fetchall()
        cur.close() 

        users = [{'nama': row[0], 'nim': row[1]} for row in data]

        return render_template('home.html', users = users)
    else : 
        return redirect(url_for('login'))
    
@app.route('/logout', methods=['GET', 'POST'])
def logout_user(): 
    session.pop('is_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__== "__main__":
    app.run(debug=True)