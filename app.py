from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=['GET'])
def homepage():
    yt = "https://www.youtube.com/@PW-Foundation/videos"
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.get(yt)
    driver.execute_script("window.scrollBy(0,500)", "")
    data = driver.find_elements(
        By.XPATH, "//ytd-thumbnail[@class='style-scope ytd-rich-grid-media']")
    yt_link = []
    for i in range(5):
        html = data[i].get_attribute('innerHTML')
        html_bs = bs(html, 'html.parser')
        link = 'https://www.youtube.com' + html_bs.a['href']
        yt_link.append(link)
    thumbnail = []
    for i in range(5):
        html = data[i].get_attribute('innerHTML')
        htmlBS = bs(html, 'html.parser')
        img = htmlBS.a.img["src"]
        thumbnail.append(img)
        data1 = driver.find_elements(By.XPATH, "//div[@id='meta']")
    titles = []
    for i in range(5):
        html = data1[i+1].get_attribute('innerHTML')
        htmlBS = bs(html, 'html.parser')
        title = htmlBS.h3.a['title']
        titles.append(title)
    data1 = driver.find_elements(
        By.XPATH, "//span[@class='inline-metadata-item style-scope ytd-video-meta-block']")
    views = []
    for i in range(5):
        html = data1[2*i].get_attribute('innerHTML')
        htmlBS = bs(html, 'html.parser')
        view = htmlBS
        views.append(view)
        times = []
    for i in range(5):
        html = data1[2*i+1].get_attribute('innerHTML')
        htmlBS = bs(html, 'html.parser')
        time = htmlBS
        times.append(time)
    d = {'Link': yt_link, 'Thumbnail': thumbnail,
         'Title': titles, 'Views': views, 'Time': times}
    data = []
    data.append(d)
    df = pd.DataFrame(d, index=[i for i in range(1, 6)])
    df.to_csv('ytData.csv')
    return render_template('result.html', datas = data)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
