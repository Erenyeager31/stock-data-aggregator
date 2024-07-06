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
    dateend = '-'.join(dateend) # convert back to string

    return dateend

# using a single news article source such as timesofindia due to a simple and easy to scrape structure.
# source --> https://www.businesstoday.in/topic/TECHM?lang=en&site=bt&ctype=all&rtype=
#? &datestart=05-06-2024    --> to be changed based on the date
#? &dateend=05-07-2024      --> to be changed based on the date
# &daterange=pastMonth
# &sr=createddatetime
# &sro=desc
# &size=10
# &from=0


def ScrapNewsExtract(URLdata,driver,keyword):
    dateend = calculateDateParams()
    extracted_data = []
    # driver.set_page_load_timeout(10)
    try:
        for index,data in enumerate(URLdata):
            if index == 0:
                continue
            if index % 2 == 0:
                print(chalk.blue(str(index)+":"),chalk.red(data['url']))
            else:
                print(chalk.blue(str(index)+":"),chalk.green(data['url']))

            #? open the url
            try:
                # Open the URL
                url = data['url']
                driver.get(url)

                # Wait for the article section to be present
                article_Section = WebDriverWait(driver, 10).until(
                    # EC.presence_of_element_located((By.TAG_NAME, "p"))
                    EC.presence_of_element_located((By.XPATH, "//div[@class='text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item']"))
                    # EC.presence_of_element_located((By.XPATH, "//div[@id='descriptionStoryId']"))
                )
            except Exception as e:
                print(chalk.yellow(f'Error loading page or finding element: {e}'))
                continue

            all_p_tags = article_Section.find_elements(By.TAG_NAME,"p")

            article = ""
            for p_tag in all_p_tags:
                article += p_tag.text.strip() + " "

            datatoinsert = {
                'url':data['url'],
                'article':article
            }

            extracted_data.append(datatoinsert)

        with open(f'./ScrappedData/extracted_{keyword}_{dateend}.json','w',encoding='utf-8') as file:
            datastring = json.dumps(extracted_data,ensure_ascii=False)
            file.write(datastring)
            print(chalk.red('Data saved succesfully'))

        return {
            'status':True,
            'message':"Data fetched successfully",
            'data':extracted_data,
            'filepath':f'./ScrappedData/extracted_{keyword}_{dateend}.json'
        }
    
    except Exception as e:
        print(chalk.red('Some error occured :'),e)
        return {
            'status':False,
            'message':"Failed to Scrap the news URL's"
        }