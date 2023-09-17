#create a sample flask app
import flask
from flask import url_for
import json
import config
app = flask.Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"


# create a route that will show go to a latter template that will read dragon.json and create a table of dragons
@app.route("/latter")
def latter():
    # read the json
    with open(config.dragonjson, "r") as file:
        data = json.load(file)
        temp = data["dragons"]
        #sort the dragons
        temp = sorted(temp, key=lambda k: k['latter_position'])

        #pass it to the template
        return flask.render_template("latter.html", dragons=temp)
    



if __name__ == "__main__":
    app.run(debug=True)
#


