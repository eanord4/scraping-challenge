from flask import Flask, render_template
import pymongo

app = Flask(__name__)





if __name__ == "__main__":
    app.run(debug=True)