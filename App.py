from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)             # create an app instance
app.secret_key = '1234'
mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "1234"
app.config["MYSQL_DATABASE_DB"] = "financialbond"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSignUp")
def showSignUp():
    return render_template("signup.html")


@app.route("/signUp", methods=["POST"])
def signUp():
    try:
        # Read values from the UI
        _username = request.form["inputUsername"]
        _password = request.form["inputPassword"]
        _role = request.form["userType"]

        # Validate the values
        if _username and _password and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc("create_user", (_username, _hashed_password, _role))
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({"message": "User created successfully"})
            else:
                return json.dumps({"error": str(data[0])})

        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})

    finally:
        cursor.close()
        conn.close()


@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputUsername']
        _password = request.form['inputPassword']

        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc("validate_user", (_username,))
        data = cursor.fetchall()

        if len(data) > 0:
            if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Username or Password.')
        else:
            return render_template('error.html', error='Wrong Username or Password.')
 
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":        # on running python App.py
    # Schema()
    app.run(debug=True)           # run the flask app
