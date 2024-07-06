from Xlogin import login_to_website
from SearchXTags import Search
from ScrapNewsURLs import ScrapNews
from ScrapNewsExtract import ScrapNewsExtract
from inference import NERinferenceAPI
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from dotenv import load_dotenv
import json
import os
import pprint
from flask import Flask,jsonify,request
from simple_chalk import chalk

load_dotenv()

# options for selenium driver
options = ChromeOptions();
options.add_argument("--headless=new")
options.page_load_strategy = 'eager'
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# creating the flask app
app = Flask( __name__)

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method == 'GET'):
        args = request.args.get('test')
        data = args
        return jsonify({"data":data})

@app.route('/scraptweets',methods=['GET','POST'])
def ScrapTweets():
    if(request.method == 'GET'):
        keyword = request.args.get('keyword')
        username = os.getenv('USERNAMET')
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        driver = webdriver.Chrome(options=options)

        #? Performing X scrapping -->
        # attempt login of the twitter account
        jsonRes = login_to_website(username, email, password,driver)
        
        # if login not successfull quit the driver
        if not jsonRes['status']:
            driver.quit()
        else:
            tweetScrapeResponse = Search(keyword,driver)
            driver.quit()
            return tweetScrapeResponse

@app.route('/scrapNews',methods=['GET','POST'])
def ScrapNewsApi():
    if(request.method == 'GET'):
        keyword = request.args.get('keyword')
        driver = webdriver.Chrome(options=options)
        scrapNewsURLResponse = ScrapNews(keyword,driver)

        if scrapNewsURLResponse['status']:
            # if urls are scrapped then proceed to scrap the actual news content
            scrapNewsResponse = ScrapNewsExtract(scrapNewsURLResponse['data'],driver,keyword)
            driver.quit()
            if scrapNewsResponse['status']:
                return scrapNewsResponse
            else:
                return scrapNewsResponse
        else:
            driver.quit()
            return scrapNewsURLResponse

@app.route('/inference',methods=['GET','POST'])
def Inference():
    if(request.method == 'GET'):
        filePath = request.args.get('filepath')
        print(chalk.green(filePath))
        with open(filePath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        inferenceResponse = NERinferenceAPI(data)
        pprint(chalk.magenta(inferenceResponse))
        return {
            'message':inferenceResponse
        }

if __name__ == "__main__":
    app.run(debug = True)     