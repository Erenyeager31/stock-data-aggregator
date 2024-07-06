from Xlogin import login_to_website
from SearchXTags import Search
from ScrapNewsURLs import ScrapNews
from ScrapNewsExtract import ScrapNewsExtract
from inference import inferenceML
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from dotenv import load_dotenv
import json
import os

load_dotenv()

if __name__ == "__main__":
    username = os.getenv('USERNAMET')
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    keyword = 'TECHM'

    options = ChromeOptions();
    options.add_argument("--headless=new")
    options.page_load_strategy = 'eager'
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()

    #? Performing X scrapping -->
    # attempt login of the twitter account
    # jsonRes = login_to_website(username, email, password,driver)
    
    # # if login not successfull quit the driver
    # if not jsonRes['status']:
    #     driver.quit()
    # else:
    #     tweetScrapeResponse = Search(keyword,driver)
    
    # scrapNewsURLResponse = ScrapNews(keyword,driver)

    # if scrapNewsURLResponse['status']:
        # if urls are scrapped then proceed to scrap the actual news content
        # scrapNewsResponse = ScrapNewsExtract(scrapNewsURLResponse['data'],driver,keyword)
        # print(scrapNewsResponse)
    
    #! test function call
    # scrapNewsResponse = ScrapNewsExtract(testData,driver,keyword)

    driver.quit()    

    #! test for inference
    with open('./ScrappedData/extracted_TECHM_05-07-2024.json', 'r', encoding='utf-8') as file:
        data = json.load(file)  # Use json.load() instead of json.loads() for file objects
    inferenceResponse = inferenceML(data)