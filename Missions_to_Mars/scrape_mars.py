# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests
import time
import datetime as dt


def scrape():
    # Set chromedriver path
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Find latest News Article Title and Description from the Mars News Site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    mars_news = browser.html
    soup = bs(mars_news, 'html.parser')
    news_title = browser.find_by_css('.content_title')[0].text
    paragraph_text = browser.find_by_css('.article_teaser_body')[0].text

    # Find the Featured Mars Image from JPL Mars Space Images
    space_image_url = 'https://spaceimages-mars.com/'
    browser.visit(space_image_url)
    featured_mars_pic = browser.html
    soup = bs(featured_mars_pic, 'html.parser')
    img_source = soup.find(class_='headerimage fade-in')['src']
    featured_image_url = space_image_url + img_source

    # Scrape the Mars Facts table from the Website
    mars_facts_url = 'https://galaxyfacts-mars.com/'

    # Scrape for tables
    tables = pd.read_html(mars_facts_url)

    # Arrange a df using the 2nd table
    df = tables[1]
    df.columns = ['Attribute', 'Measure']

    # Convert df to html
    html_table = df.to_html()

    mars_html_table = html_table.replace('\n', '')

    # ## Gather Hemisphere Image URLs
    hemisphere_url = 'https://marshemispheres.com/'

    # Retrieve page with the requests module
    response = requests.get(hemisphere_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    results = soup.find_all('div', class_='item')

    url_list = []
    for result in results:
        pic_url = result.find('a', class_='itemLink product-item')['href']
        url_list.append(pic_url)

        
    final_url_list = []
    for url in url_list:
        url = hemisphere_url + url
        final_url_list.append(url)


    final_hemisphere_info = []
    for url in final_url_list:
        
        # Retrieve page with the requests module
        response = requests.get(url)
        time.sleep (4)
        
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = bs(response.text, 'html.parser')
        
        # Find image urls
        src_img = soup.find(class_='wide-image')['src']
        final_img_url = hemisphere_url + src_img
        
        # Find titles
        img_title = soup.find('h2', class_='title').text.rsplit(' ', 1)[0]
        
        # Create dictionary
        dict = {"title": img_title,
            "img_url": final_img_url}
        
        # Append values
        final_hemisphere_info.append(dict)

    #Put scraped items into single dictionary
    mars_data = {

        "article_title": news_title,
        "paragraph_text": paragraph_text,
        "featured_image": featured_image_url,
        "mars_facts": mars_html_table,
        "hemisphere_image_title_1": final_hemisphere_info[0]["title"],
        "hemisphere_image_url_1": final_hemisphere_info[0]["img_url"],
        "hemisphere_image_title_2": final_hemisphere_info[1]["title"],
        "hemisphere_image_url_2": final_hemisphere_info[1]["img_url"],
        "hemisphere_image_title_3": final_hemisphere_info[2]["title"],
        "hemisphere_image_url_3": final_hemisphere_info[2]["img_url"],
        "hemisphere_image_title_4": final_hemisphere_info[3]["title"],
        "hemisphere_image_url_4": final_hemisphere_info[3]["img_url"],
        "scrape_date": dt.datetime.now()

    }

    browser.quit()

    return(mars_data)


