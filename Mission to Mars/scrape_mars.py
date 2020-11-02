from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():

    executable_path = {"executable_path": "driver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    latest_news=soup.find("div",class_="list_text")
    news_title=latest_news.find("div",class_="content_title").get_text()    
    news_p=latest_news.find("div",class_="article_teaser_body").get_text()

    browser.quit()
    return news_title,news_p

def scrape_image():
    browser = init_browser()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    full_image_button=soup.find("a",class_="button fancybox")
    link=full_image_button["data-fancybox-href"]
    featured_image_url="https://www.jpl.nasa.gov"+link

    browser.quit()
    return featured_image_url

def scrape_weather():
    browser = init_browser()

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather=soup.find_all("div",lang="en")[0].text
    
    browser.quit()
    return mars_weather

def scrape_fact():
    
    url = "https://space-facts.com/mars/"
    table = pd.read_html(url)[0]
    mars_df=table
    mars_df.columns=["Info","Facts"]
    mars_df.set_index("Info",inplace=True)
    return mars_df.to_html(classes="table table-striped")

def scrape_hemispheres():
    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(5)
    html=browser.html
    soup=bs(html,"html.parser")

    links=[]
    hemisphere_image_urls=[]

    items=soup.find_all("div",class_="item")
    for item in items:
        links.append('https://astrogeology.usgs.gov'+item.find('a')['href'])

    for link in links:
        hemisphere={}
        browser.visit(link)
        html=browser.html
        soup=bs(html,"html.parser")
        hemisphere["title"]=soup.find('div',class_='content').find('h2').text
        hemisphere["img_url"]=soup.find('div',class_='downloads').find('a')['href']
        hemisphere_image_urls.append(hemisphere)

    browser.quit()
    return hemisphere_image_urls

def scrape():
    browser = init_browser()
    news_title,news_p=scrape_news()
    featured_image_url=scrape_image()
    mars_weather=scrape_weather()
    mars_fact=scrape_fact()
    hemisphere_image_urls=scrape_hemispheres()

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "facts": mars_fact,
        "hemispheres": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

print("Scrape finished.")
