from flask import Flask


app = Flask(__name__)             # create an app instance


@app.route("/")                   # at the end point /
def index():                      # call method hello
    return "Hello World!"         # which returns "hello world"


if __name__ == "__main__":        # on running python App.py
    # Schema()
    app.run(debug=True)           # run the flask app
