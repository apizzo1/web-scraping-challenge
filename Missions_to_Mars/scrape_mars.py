#import dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time

#create function for opening browser
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #*****NASA Mars News*****
    # URL of Mars News page to be scraped
    mars_news_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Go to url
    browser.visit(mars_news_url)
    #allow browser to load (source: Jeremy Hamley in Slack channel ask-the-class)
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'lxml'
    html = browser.html
    soup = bs(html, 'lxml')

    #find part of webpage with article titles and article teasers
    basic_info = soup.find('div', class_="list_text")

    #Find latest article title
    news_title = basic_info.find('a').text
    #Find latest article teaser
    news_p = basic_info.find('div', class_="article_teaser_body").text


    #*****JPL Mars Space Images - Featured Image*****
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Go to url
    browser.visit(jpl_url)
    #set up beautiful soup for the jpl link
    html2 = browser.html
    soup2 = bs(html2, 'lxml')

    # Click the 'Full Image' button to get Full image url
    browser.click_link_by_partial_text('FULL IMAGE')

    #continue navigating to find 'largesize' picture
    browser.click_link_by_partial_text('more info')

    #set beautiful soup for more info page
    html3 = browser.html
    soup3 = bs(html3, 'lxml')

    #find part with image info
    jpl_info = soup3.find_all('figure', class_="lede")

    #show only first (and only) item in the list
    jpl_list_item = jpl_info[0]

    #get partial image link
    featured_image_partial_link = jpl_list_item.a['href']

    #concat full image link
    jpl_main_link = 'https://www.jpl.nasa.gov'
    featured_image_url = jpl_main_link+featured_image_partial_link

    #*****Mars Weather*****
    mars_twitter = 'https://twitter.com/marswxreport?lang=en'
    # Go to url
    browser.visit(mars_twitter)
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'lxml'
    html_twitter = browser.html
    soup4 = bs(html_twitter, 'lxml')

    #find part with tweet information
    twitter_tweets = soup4.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_weather  = twitter_tweets[0].text
    mars_weather = mars_weather.replace('\n',',')

    #*****Mars Facts*****
    mars_facts_url = 'https://space-facts.com/mars/'

    #read the html using pandas to get tables
    mars_tables = pd.read_html(mars_facts_url)

    #use first table for mars facts
    mars_df = mars_tables[0]

    #rename columns and set index
    mars_df.columns = ['Mars Fact', 'Value']
    mars_df.set_index('Mars Fact', inplace=True)

    #create html table string and remove \n
    mars_fact_html_table = mars_df.to_html()
    mars_fact_html_table.replace('\n', '')

    #*****Mars Hemispheres*****
    mars_hemi_link = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Go to Mars Hemispheres url
    browser.visit(mars_hemi_link)

    #set up beautiful soup for the link
    mars_hemi_html = browser.html
    soup5 = bs(mars_hemi_html, 'html.parser')

    #find the hemisphere names and append to list
    mars_hemispheres = []
    headers = soup5.find_all('a',class_="itemLink product-item")
    for header in headers:
        title = str(header.find('h3'))
        #strip out the Nonetypes and tags
        if title != 'None':
            title = title.lstrip('<h3>')
            title = title.rstrip('</h3>')
            mars_hemispheres.append(title)

    #loop through the hemisphere names to find the image urls
    hemisphere_image_urls = []
    for hemisphere in mars_hemispheres:
        # Click the hemisphere name link to get image url information
        browser.click_link_by_partial_text(hemisphere)
        mars_hemisphere_link = browser.html
        #get url to full resolution image
        soup_mars_hemi = bs(mars_hemisphere_link, 'html.parser')
        hemi_results = soup_mars_hemi.find_all('div',class_="downloads")
        hemi_pic_url = hemi_results[0].find('a')['href']
        #return to main page
        browser.visit(mars_hemi_link)
        #clean up hemisphere name
        hemisphere = hemisphere.replace(" Enhanced",'')
        #create hemisphere dictionary
        mars_dict = {}
        mars_dict = {
            'title':hemisphere,
            'img_url':hemi_pic_url
        }
        #append to list of hemisphere dictionaries
        hemisphere_image_urls.append(mars_dict)

    browser.quit()

    #create dictionary with all returned data
    mars_data = {}
    mars_data = {
        "News_Title":news_title,
        "News_Paragraph":news_p,
        "JPL_image":featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Facts":mars_fact_html_table,
        "Hemisphere_pictures":hemisphere_image_urls 
                }

    #return results
    return mars_data
    

