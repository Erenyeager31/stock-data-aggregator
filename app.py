from scripts.Xlogin import login_to_website
from scripts.SearchXTags import Search
from scripts.ScrapNewsURLs import ScrapNews
from scripts.ScrapNewsExtract import ScrapNewsExtract
from scripts.getNSEdata import getNSECurrentPrice
from MachineLearning.SentimentAnalysis import sentiment_analysis
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.firefox.options import Options
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

@app.route('/getNSEstock/<action>',methods=['GET','POST'])
def getNSEdata(action):
    # possible parameters
    # 1. current price (cprice)
    options = Options();
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")  # Set window size
    options.add_argument("--disable-extensions")  # Disable extensions
    options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    options.add_argument("--enable-logging")  # Enable logging
    driver = webdriver.Firefox(options=options)

    # fireFoxOptions = Options()  
    # fireFoxOptions.add_argument("--headless") 
    # fireFoxOptions.add_argument("--window-size=1920,1080")
    # fireFoxOptions.add_argument('--start-maximized')
    # fireFoxOptions.add_argument('--disable-gpu')
    # fireFoxOptions.add_argument('--no-sandbox')

    # driver = webdriver.Firefox(options=fireFoxOptions, 
    # # executable_path=r'C:\[your path to firefox webdriver exe file]\geckodriver.exe'
    # )
    
    symbol = request.args.get('symbol')

    
    print(chalk.red('action :'),action)
    if action == 'getNSECMP':
        response = getNSECurrentPrice(driver,symbol)
        print(chalk.green(response))
        return response


if __name__ == "__main__":
    app.run(debug = True)