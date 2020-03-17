# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# create route that renders index.html template
@app.route("/")
def index():
    mars = client.db.mission_to_mars.find_one()
    return render_template("index.html", mission_to_mars = mars)

@app.route("/scrape")
def scraper():
    mars = client.db.mission_to_mars 
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)