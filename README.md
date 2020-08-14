# web-scraping-challenge

### All files are in the Mission_to_Mars folder:
- Mission to Mars jupyter notebook for data scraping verification
- scrape_mars.py which has a function to perform all scraping from jupyter notebook
- app.py which uses scrape_mars.py scrape function and stores returned data in mongoDB. This file also renders data in index.html
- index.html found in templates folder
- style.css file found in static folder to ensure it works properly with flask
- Images of final application are found in Images folder

When application is launched, click 'Scrape New Data' button to initiate scrape route in app.py (which uses scrape function in scrape_mars.py). A browser instance will launch and navigate through all necessary webpages. Once done, this browser instance will close and the application page will update with most up-to-date information.