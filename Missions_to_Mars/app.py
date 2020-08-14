#import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mission2mars_app")

#create landing page details
@app.route("/")
def index():
    #query Mongo database and pass the mars data into an HTML template to display the data
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)

#call scrape function from scrape_mars.py
@app.route("/scrape")
def scraper():

    #code from 09-Ins_Scrape_And_Render activity
    mars_data = mongo.db.mars_data
    # Run the scrape function
    mars_details = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars_data.update({}, mars_details, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
