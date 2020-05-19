from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


app = Flask(__name__)             # create an app instance


mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "1234"
app.config["MYSQL_DATABASE_DB"] = "financialbond"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
mysql.init_app(app)


@app.route("/")                   # at the end point /
def index():                      # call method hello
    time = datetime.now()
    return "Hi, the current time is " + str(time.hour) + ":" + str(time.minute) + "!"        # which returns "hello world"


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


if __name__ == "__main__":        # on running python App.py
    # Schema()
    app.run(debug=True)           # run the flask app
