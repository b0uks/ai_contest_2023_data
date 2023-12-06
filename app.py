import flask

app = flask.Flask(__name__)

if __name__ == "__main__":
    print(flask.__version__)
    app.run(debug=True)
