from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set the executable path and initialize the Chrome browser in Splinter
executable_path = {'executable_path': '/Users/Haylea/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the Mars NASA news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

html = browser.html
news_soup = BeautifulSoup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

slide_elem.find("div", class_='content_title')

news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### Featured Images

# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = BeautifulSoup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

df = pd.read_html('http://space-facts.com/mars/')[0]
df.columns=['description', 'value']
df.set_index('description', inplace=True)
df
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# Hemispheres
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

products = soup.find("div", class_ = "result-list" )
hemispheres = products.find_all("div", class_="item")

for h in hemispheres:
    title = h.find("h3").text
    end_link = h.find("a")["href"]
    image_link = "https://astrogeology.usgs.gov/" + end_link    
    browser.visit(image_link)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    hemisphere_image_urls.append({"title": title, "img_url": image_url})

hemisphere_image_urls

browser.quit()

