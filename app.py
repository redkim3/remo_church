from flask import Flask
from main import WindowClass

app = Flask(__name__)

@app.route("/")
def hello():
    window = WindowClass()
    return window.render()

if __name__ == "__main__":
    app.run(debug=True)