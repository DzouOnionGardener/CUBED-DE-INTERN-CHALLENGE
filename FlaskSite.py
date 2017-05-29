from flask import Flask, render_template, request
from analyzer import *

app = Flask(__name__)
@app.route('/')
def index():
    a = analyzer()
    correlation, ratio = a.ScoreCorrelations()
    return render_template("home.html", Ratio = ratio, Correlation = correlation)
    ##todo:
    ## tomorrow, create a test form that takes in username and password for the database
    ## to test it, we will post a response message to the template saying "hello, "username"!"
    ## that way we know that we've managed to get username and password and we can GET
    ## then use that data to log into the database and start the storing and shit


if __name__ == "__main__":
    app.run(debug=True)