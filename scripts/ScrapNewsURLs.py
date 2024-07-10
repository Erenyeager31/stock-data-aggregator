from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from simple_chalk import chalk
import json
import time
from datetime import date

def calculateDateParams():
    today = date.today()
    dateend = str(today).split('-')
    dateend.reverse() # conversion to dd-mm-yyyy format in list

    datestart = dateend.copy()
    datestart[1] = '0'+str(int(datestart[1])-1)
    datestart = '-'.join(datestart) # convert back to string

    dateend = '-'.join(dateend) # convert back to string
    print(datestart,dateend)

    return datestart,dateend

# using a single news article source such as timesofindia due to a simple and easy to scrape structure.
# source --> https://www.businesstoday.in/topic/TECHM?lang=en&site=bt&ctype=all&rtype=
#? &datestart=05-06-2024    --> to be changed based on the date
#? &dateend=05-07-2024      --> to be changed based on the date
# &daterange=pastMonth
# &sr=createddatetime
# &sro=desc
# &size=10
# &from=0


def ScrapNews(keyword,driver):
    datestart,dateend = calculateDateParams()
    url = f'https://www.businesstoday.in/topic/{keyword}?lang=en&site=bt&ctype=all&rtype=&datestart={datestart}&dateend={dateend}&daterange=pastMonth&sr=createddatetime&sro=desc&size=10&from=0'

    try:
        driver.get(url)
        all_urls = []
        news_section = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,".//div[@class='news-main']"))
        )

        li_tags = news_section.find_elements(By.TAG_NAME,"li")

        for li_tag in li_tags:
            try:
                anchor_tags = li_tag.find_element(By.TAG_NAME,"a")
            except:
                continue
            title = anchor_tags.get_attribute('title')
            url = anchor_tags.get_attribute('href')
            # print(chalk.red(url))
            if 'author' in url:
                continue
            data = {
                'title':title,
                'url':url
            }
            all_urls.append(data)

        with open(f'./data/ScrappedNews/URL_{keyword}_{dateend}.json','w',encoding='utf-8') as file:
            dataString = json.dumps(all_urls,ensure_ascii=False)
            file.write(dataString)
            print(chalk.green('Anchor tags retrieved succesfully'))

        return {
            'status':True,
            'message':"URL's fetched successfully",
            'data':all_urls
        }

    except Exception as e:
        print(chalk.red('Some error occured :'),e)
        return {
            'status':False,
            'message':"Failed to Scrap the news URL's"
        }