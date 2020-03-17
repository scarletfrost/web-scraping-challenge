from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)
 

def scrape():
    final_data = {}
    final_data["mars_news"] = scrape_mars_news()
    final_data["mars_paragraph"] = scrape_mars_paragraph()
    final_data["mars_image"] = scrape_mars_jpl_image()
    final_data["mars_weather"] = scrape_mars_weather()
    final_data["mars_facts"] = scrape_mars_facts()
    final_data["mars_hemisphere"] = scrape_mars_hemisphere()

    return final_data

def scrape_mars_news():
    NASA_Mars_News_url = 'https://mars.nasa.gov/news/'
    browser.visit(NASA_Mars_News_url)
    html = browser.html
    results = BeautifulSoup(html, "html.parser")
    title_news = results.find_all('div', class_='content_title')
    news_title = title_news[4].text

    return news_title

def scrape_mars_paragraph():
    NASA_Mars_News_url = 'https://mars.nasa.gov/news/'
    browser.visit(NASA_Mars_News_url)
    html = browser.html
    results = BeautifulSoup(html, "html.parser")
    para = results.find_all('div', class_="rollover_description")
    para_news = para[9].text
    
    return para_news

def scrape_mars_jpl_image():
    JPL_Mars_Space_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(JPL_Mars_Space_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    f_img_url=soup.find("div", class_="carousel_items")
    bg_img_url=soup.find('article')['style']
    bg_img_url_split=bg_img_url.split("'")
    bg_img_url_f=bg_img_url_split[1]
    base='https://www.jpl.nasa.gov'
    featured_image_url = base + bg_img_url_f

    return featured_image_url

def scrape_mars_weather():
    Mars_Weather_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(Mars_Weather_url)
    twitter_soup = BeautifulSoup(response.text, 'lxml')
    t_text = twitter_soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    w_text = 'InSight '
    for t in t_text:
        if w_text in t.text:
            mars_weather = t.text
    
    return mars_weather

def scrape_mars_facts():
    mars_facts_url = "https://space-facts.com/mars/"
    facts_data = pd.read_html(mars_facts_url)
    facts_data_df = facts_data[0]
    facts_df_html = facts_data_df.to_html(classes=['table','thead-dark','table-striped', 'text-center'])
    facts_df_html = facts_df_html.replace("\n",'')

    return facts_df_html

def scrape_mars_hemisphere():
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_url)
    html = browser.html
    hem_soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []
    hem_dict = {'title': [], 'img_url': [],}
    x = hem_soup.find_all('h3')
    for i in x:
        t = i.get_text()
        title = t.strip('Enhanced')
        browser.click_link_by_partial_text(t)
        hem_url = browser.find_link_by_partial_href('download')['href']
        hem_dict = {'title': title, 'img_url': hem_url}
        hemisphere_image_urls.append(hem_dict)
        browser.back()

    return hemisphere_image_urls