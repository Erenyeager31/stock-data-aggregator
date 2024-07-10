from scripts.Xlogin import login_to_website
from scripts.SearchXTags import Search
from scripts.ScrapNewsURLs import ScrapNews
from scripts.ScrapNewsExtract import ScrapNewsExtract
from MachineLearning.SentimentAnalysis import sentiment_analysis
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

# creating the flask app
app = Flask( __name__)

@app.route('/',methods=['GET','POST'])
def home():
    if(request.method == 'GET'):
        # args = request.args.get('test')
        # data = args
        return {
            'message':'The server is running succesfully'
        }

@app.route('/scraptweets',methods=['GET','POST'])
def ScrapTweets():
    if(request.method == 'GET'):
        options = ChromeOptions();
        options.add_argument("--headless=new")
        keyword = request.args.get('keyword')
        username = os.getenv('USERNAMET')
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')

        driver = webdriver.Chrome(options=options)

        #? Performing X scrapping -->
        # attempt login of the twitter account
        jsonRes = login_to_website(username, email, password,driver)

        print(chalk.red('here'))
        # if login not successfull quit the driver
        if not jsonRes['status']:
            print(chalk.green('here'))
            driver.quit()
            return jsonRes
        else:
            print(chalk.yellow('here'))
            tweetScrapeResponse = Search(keyword,driver)
            driver.quit()
            return tweetScrapeResponse
    else:
        return {
            'status':False
        }

@app.route('/scrapNews',methods=['GET','POST'])
def ScrapNewsApi():
    if(request.method == 'GET'):
        options = ChromeOptions();
        options.page_load_strategy = 'eager'
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
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

@app.route('/SentimentAnalysis',methods=['GET','POST'])
def Inference():
    if(request.method == 'GET'):
        filePath = request.args.get('filepath')
        filePath = './data/ScrappedNews/extracted_RVNL_05-07-2024.json'
        with open(filePath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        # inferenceResponse = SentimentAnalysis(data)
        sentiment_response = sentiment_analysis(data)
        # pprint(chalk.magenta(inferenceResponse))
        return sentiment_response

if __name__ == "__main__":
    app.run(debug = True)