from selenium import webdriver
from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
from datetime import datetime

def scrape():
    """Scrape various data from Mars-related websites. Returns a dictionary of the scraped data."""
    
    date = datetime.today().isoformat()

    # set up Selenium driver
    print("Setting up Selenium driver...")
    driver = webdriver.Firefox()


    ## NASA Mars News ##

    # get html to parse
    print("Getting HTML for Nasa Mars News...")
    url = "https://mars.nasa.gov/news"
    driver.get(url)
    soup = BS(driver.page_source, "html.parser")

    # parse html
    print("Parsing HTML for Nasa Mars News...")
    item = soup.find('li', class_="slide")
    news_date = item.find('div', class_="list_date").text
    title_a = item.find('div', class_="content_title").a
    news_title = title_a.text
    news_href = title_a['href']
    news_para = item.find('div', class_="article_teaser_body").text


    ## JPL Mars Space Images - Featured Image ##

    # get html to parse
    print("Getting HTML for Featured Image...")
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    r = requests.get(url)
    assert(r.status_code == 200)
    soup = BS(r.text, "html.parser")

    # parse html
    print("Parsing HTML for Featured Image...")
    button_a = soup.find('a', id="full_image")
    featured_image_url = "https://www.jpl.nasa.gov" + button_a['data-fancybox-href']
    img_title = button_a['data-title']
    img_desc = button_a['data-description']


    ## Mars Weather ##

    # get html to parse
    print("Getting HTML for Mars Weather...")
    url = "https://twitter.com/marswxreport?lang=en"
    r = requests.get(url)
    assert(r.status_code == 200)
    soup = BS(r.text, "html.parser")

    # parse html
    print("Parsing HTML for Mars Weather...")
    # for some reason this shows up as a `span` via the inspector, but something
    # goes wrong via requests and even selenium. the 'p' tag below was found via
    # <str.find> on the request html but does not appear via the inspector.
    p = soup.find('p', class_="tweet-text")
    mars_weather = p.text.split("pic.twitter.com/")[0]


    ## Mars Facts ##

    #get html to parse
    print("Getting HTML for Mars Facts...")
    url = "http://space-facts.com/mars/"
    r = requests.get(url)
    assert(r.status_code == 200)

    # parse html
    print("Parsing HTML for Mars Facts...")
    # "HTML table string"? i think just a data frame makes sense?
    tables = pd.read_html(r.text)
    mars_facts = tables[0].rename(columns={0: "Property", 1: "Value"}).set_index("Property").to_html()
    earth_comparison = tables[1].rename(columns={"Mars - Earth Comparison": "Property"}).set_index("Property").to_html()


    ## Mars Hemispheres ##

    # get html to parse
    print("Getting HTML for Mars Hemispheres...")
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    driver.get(url)

    # parse html on main page
    print("Parsing main page for Mars Hemispheres...")
    imgs = {}  # initially the urls of the images pages, then replaced with actual image urls
    for a in driver.find_elements_by_tag_name('a'):
        if a.get_attribute('class') == "itemLink product-item" and a.find_elements_by_tag_name('h3'):
            imgs[a.text] = a.get_attribute('href')
            
    # parse html on each image page
    print("Parsing image pages for Mars Hemispheres...")
    for key, value in imgs.items():
        driver.get(value)
        img = driver.find_element_by_tag_name('img')
        imgs[key] = img.get_attribute('src')
    

    return {

        'request_date': date
        
        'news': {
            'date': news_date,
            'title': news_title,
            'paragraph': news_para,
            'more': "https://mars.nasa.gov" + news_href
        },

        'featured_image': {
            'title': img_title,
            'description': img_desc,
            'url': featured_image_url
        },

        'weather': {
            'tweet_text': mars_weather
        },

        'facts': {
            'mars': mars_facts,
            'earth_comparison': earth_comparison
        },

        'hemisphere_img_urls': imgs

    }


if __name__ == "__main__":
    from pprint import pprint
    pprint(scrape())