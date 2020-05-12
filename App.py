from flask import Flask
from datetime import datetime


app = Flask(__name__)             # create an app instance


@app.route("/")                   # at the end point /
def index():                      # call method hello
    time = datetime.now()
    return "Hi, the current time is " + str(time.hour) + ":" + str(time.minute) + "!"        # which returns "hello world"


if __name__ == "__main__":        # on running python App.py
    # Schema()
    app.run(debug=True)           # run the flask app
