import flask
from importlib.metadata import version

app = flask.Flask(__name__)

if __name__ == "__main__":
    print(version("flask"))
    app.run(debug=True)