from flask import Flask, render_template, jsonify
from pymongo import MongoClient


# set up
app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = MongoClient(conn)
db = client.scrape
coll = db.mars


def context(doc, result=None):
    """turn the document into an unpackable format for the render_template context"""

    if result is None:
        result = {}

    if '_id' in doc:
        doc.pop('_id')

    doc2 = doc.copy()

    for key, value in doc.items():

        if isinstance(value, dict):
            for k, v in doc2.pop(key).items():
                doc2[key + '_' + k.replace(' ', '_')] = v  # preserve information about higher-level key
            return context(doc2, result)
        
        result[key] = doc2.pop(key)
    
    return result


@app.route("/")
def home():
    latest_doc = next(coll.find().sort('request_timestamp', -1).limit(1))
    return render_template("index.html", **context(latest_doc))


@app.route("/scrape")
def scrape():
    from scrape_mars import scrape
    scrape_result = scrape()
    coll.insert_one(scrape_result)
    scrape_result.pop('_id')
    return jsonify(scrape_result)


if __name__ == "__main__":
    app.run(debug=True)