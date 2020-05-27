from flask import Flask, render_template, json, request, redirect, session, flash, url_for
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, filename='events.log')


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
                logging.info("Se registro usuario con el nombre: {}".format(_username))
                conn.commit()
                logging.debug("Se agrego usuario a la base de datos")
                return json.dumps({"message": "Usuario creado exitosamente"})
            else:
                logging.debug("Hubo un error al agregar usuario a la base de datos")
                return json.dumps({"error": str(data[0])})

        else:
            return json.dumps({'html': '<span>Introduzca los campos requeridos</span>'})

    except Exception as e:
        message = "Ocurrio un error al crear usuario - {}\n{}".format(e, traceback.format_exc())
        logging.error(message)
        return json.dumps({'error': str(e)})

    finally:
        cursor.close()
        conn.close()
        logging.debug("Conexion a base de datos cerrada")


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
                logging.info("Se inicio sesion con usuario {}".format(_username))
                session['user'] = data[0][0]
                session['role'] = data[0][1]
                return redirect('/userHome')
            else:
                logging.info("Usuario o contrasena incorrecta")
                return render_template('error.html', error='Usuario o contrasena incorrecta.')
        else:
            logging.info("Usuario o contrasena incorrecta")
            return render_template('error.html', error='Usuario o contrasena incorrecta.')
 
    except Exception as e:
        message = "Ocurrio un error al iniciar sesion - {}\n{}".format(e,traceback.format_exc())
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()
        logging.debug("Conexion a base de datos cerrada")


@app.route('/userHome')
def userHome():
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM bonds")
        data = cursor.fetchall()
        logging.debug("Bonos obtenidos de la base de datos")

        if session.get('user'):
            if session.get('role') == 1:
                return render_template('userhome.html', bonds=data)
            else:
                return render_template('userhomeadmin.html', bonds=data)
        else:
            return render_template('error.html', error='Acceso denegado')
    except Exception as e:
        message = "Ocurrio un error al cargar informacion - {}\n{}".format(e,traceback.format_exc())
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()
        logging.debug("Conexion a base de datos cerrada")


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    logging.info("Sesion finalizada")
    return redirect('/')


@app.route("/addBond", methods=["POST"])
def addBond():
    try:
        _idUser = session.get("user")
        _flavor = request.form["flavor"]
        _tickerSymbol = request.form["ticker_symbol"]
        _ticker = request.form["ticker"]
        _currency = request.form["currency"]
        _issueDate = request.form["issue_date"].split("/")[2]+"-"+request.form["issue_date"].split("/")[0]+"-"+request.form["issue_date"].split("/")[1]
        _originalIssueDate = request.form["original_issue_date"]
        _firstCouponDate = request.form["first_coupon_date"].split("/")[2]+"-"+request.form["first_coupon_date"].split("/")[0]+"-"+request.form["first_coupon_date"].split("/")[1]
        _coupon = request.form["coupon"]
        _maturityDate = request.form["maturity_date"].split("/")[2]+"-"+request.form["maturity_date"].split("/")[0]+"-"+request.form["maturity_date"].split("/")[1]
        _auctionDate = request.form["auction_date"].split("/")[2]+"-"+request.form["auction_date"].split("/")[0]+"-"+request.form["auction_date"].split("/")[1]
        _isin = request.form["isin"]
        _totalIssueSize = request.form["total_issue_size"]

        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("INSERT INTO bonds (id_user, flavor, ticker_symbol, ticker, currency, issue_date, original_issue_date, first_coupon_date, coupon, maturity_date, auction_date, isin, total_issue_size) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (_idUser, _flavor, _tickerSymbol, _ticker, _currency, _issueDate, _originalIssueDate, _firstCouponDate, _coupon, _maturityDate, _auctionDate, _isin, _totalIssueSize))
        con.commit()
        flash('Bono anadido exitosamente')
        logging.debug("Se anadio bono correctamente")
        return redirect(url_for('userHome'))
    except Exception as e:
        message = "Ocurrio un error al anadir bono - {}\n{}".format(e,traceback.format_exc())
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()
        logging.debug("Conexion a base de datos cerrada")


@app.route("/editBond/<id>", methods=["POST"])
def editBond(id):
    try:
        _idUser = session.get("user")
        _flavor = request.form["flavor"]
        _tickerSymbol = request.form["ticker_symbol"]
        _ticker = request.form["ticker"]
        _currency = request.form["currency"]
        _issueDate = request.form["issue_date"].split("/")[2] + "-" + request.form["issue_date"].split("/")[0] + "-" + request.form["issue_date"].split("/")[1]
        _originalIssueDate = request.form["original_issue_date"]
        _firstCouponDate = request.form["first_coupon_date"].split("/")[2] + "-" + request.form["first_coupon_date"].split("/")[0] + "-" + request.form["first_coupon_date"].split("/")[1]
        _coupon = request.form["coupon"]
        _maturityDate = request.form["maturity_date"].split("/")[2] + "-" + request.form["maturity_date"].split("/")[0] + "-" + request.form["maturity_date"].split("/")[1]
        _auctionDate = request.form["auction_date"].split("/")[2] + "-" + request.form["auction_date"].split("/")[0] + "-" + request.form["auction_date"].split("/")[1]
        _isin = request.form["isin"]
        _totalIssueSize = request.form["total_issue_size"]

        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("UPDATE bonds SET id_user=%s, flavor=%s, ticker_symbol=%s, ticker=%s, currency=%s, issue_date=%s, original_issue_date=%s, first_coupon_date=%s, coupon=%s, maturity_date=%s, auction_date=%s, isin=%s, total_issue_size=%s WHERE id_bond=%s",(_idUser, _flavor, _tickerSymbol, _ticker, _currency, _issueDate, _originalIssueDate, _firstCouponDate, _coupon,_maturityDate, _auctionDate, _isin, _totalIssueSize, id))
        con.commit()
        flash('Bono actualizado exitosamente')
        logging.debug("Se actualizo bono correctamente")
        return redirect(url_for('userHome'))
    except Exception as e:
        message = "Ocurrio un error al actualizar bono - {}\n{}".format(e,traceback.format_exc())
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()
        logging.debug("Conexion a base de datos cerrada")


@app.route("/showEditBond/<id>", methods=["POST", "GET"])
def getBond(id):
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM bonds WHERE id_bond=%s", (id))
        data = cursor.fetchall()
        logging.debug("Se cargo la informacion exitosamente")
        return render_template("editbond.html", bond=data[0])
    except Exception as e:
        message = "Ocurrio un error al cargar informacion del bono - {}\n{}".format(e,traceback.format_exc())
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()
        logging.debug("Conexion a base de datos cerrada")


if __name__ == "__main__":        # on running python App.py
    # Schema()
    app.run(debug=True)           # run the flask app
