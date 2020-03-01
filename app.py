from flask import Flask, render_template, jsonify
from pymongo import MongoClient


# set up
app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = MongoClient(conn)
db = client.scrape
coll = db.mars


@app.route("/")
def home():
    pass


@app.route("/scrape")
def scrape():
    from scrape_mars import scrape
    scrape_result = scrape()
    coll.insert_one(scrape_result)
    return jsonify(scrape_result)


if __name__ == "__main__":
    app.run(debug=True)