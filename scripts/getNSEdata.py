# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from simple_chalk import chalk
# import json,os,time
# from datetime import date
# import requests

# def calculateDateParams():
#     today = date.today()
#     dateend = str(today).split('-')
#     dateend.reverse() # conversion to dd-mm-yyyy format in list
#     dateend = '-'.join(dateend) # convert back to string

#     return dateend

# def getCurrentPrice(driver,symbol):
#     try:
#         # date = calculateDateParams()
#         # filepath = f'./Current_Price_{symbol}_{date}'
#         # url = f'https://www.nseindia.com/get-quotes/equity?symbol={symbol}'
#         # driver.get(url)

#         # ticker = WebDriverWait(driver,40).until(
#         #     # EC.presence_of_element_located((By.XPATH,".//div[@class='row price-infobox price-infobox-spacing']"))
#         #     EC.presence_of_element_located((By.XPATH,".//h2[@id='quoteName']"))
#         # )

#         # data = ticker.get_attribute('outerHTML')
#         # print(data)

#         # row = WebDriverWait(driver,40).until(
#         #     # EC.presence_of_element_located((By.XPATH,".//div[@class='row price-infobox price-infobox-spacing']"))
#         #     EC.presence_of_element_located((By.XPATH,".//table[@id='priceInfoTable']"))
#         # )

#         # print(chalk.red(row))

#         # # container = row.find_element(By.XPATH,".//div[@class='container']")

#         # # print(chalk.red(container))

#         # # tableBody = container.find_element(By.XPATH,"//table[@id='priceInfoTable']")

#         # htmlData = row.find_element('outerHTML')
#         # print(chalk.red(htmlData))

#         # # all_span_text = ""
#         # # for td in tableBody.find_elements(By.TAG_NAME, "td"):
#         # #     # all_span_text += td.text.strip() + " "
#         # #     print(td)

#         # # print(chalk.green(all_span_text))

#         session = requests.Session()
#         headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
#         }

#         # Make an initial request to the homepage to set the cookies
#         homepage_url = "https://www.nseindia.com/"
#         session.get(homepage_url, headers=headers)

#         print(chalk.blue(session))

#         # Now make the request to the API with the session cookies
#         api_url = "https://www.nseindia.com/api/chart-databyindex?index=INFYEQN"

#         # Add additional necessary headers
#         api_headers = {
#             "Accept": "application/json, text/javascript, */*; q=0.01",
#             "Accept-Encoding": "gzip, deflate, br, zstd",
#             "Accept-Language": "en-US,en;q=0.9",
#             "Referer": "https://www.nseindia.com/get-quotes/equity?symbol=INFY",
#             "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
#             "Sec-Ch-Ua-Mobile": "?0",
#             "Sec-Ch-Ua-Platform": "\"Windows\"",
#             "Sec-Fetch-Dest": "empty",
#             "Sec-Fetch-Mode": "cors",
#             "Sec-Fetch-Site": "same-origin",
#             "X-Requested-With": "XMLHttpRequest"
#         }

#         response = session.get(api_url, headers=api_headers)
#         print(chalk.red(response))

#         return {
#             "status":True,
#             "symbol":symbol,
#             # "data":data
#         }
#     except Exception as e:
#         return {
#             "status":False,
#             "symbol":symbol,
#             "message":e
#         }

import requests
from bs4 import BeautifulSoup

import requests

def getNSECurrentPrice(driver,symbol):
    try:
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        # Make an initial request to the homepage to set the cookies
        homepage_url = "https://www.nseindia.com/"
        initial_response = session.get(homepage_url, headers=headers)

        # Ensure the initial request was successful
        if initial_response.status_code != 200:
            raise Exception(f"Failed to load homepage, status code: {initial_response.status_code}")

        # Print cookies and headers to debug
        print("Cookies after initial request:", session.cookies.get_dict())
        print("Initial Response headers:", initial_response.headers)

        # Now make the request to the API with the session cookies
        api_url = f"https://www.nseindia.com/api/chart-databyindex?index={symbol}"

        # Use the headers from the initial request and add additional necessary headers
        api_headers = {**initial_response.request.headers, **{
            "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol}",
            "X-Requested-With": "XMLHttpRequest"
        }}

        # Make the request to the API with the session cookies and headers
        response = session.get(api_url, headers=api_headers)

        # Print the response status and headers to debug
        print("API Response status:", response.status_code)
        print("API Response headers:", response.headers)

        # Ensure the request was successful
        if response.status_code == 200:
            data = response.json()
            return {
                "status": True,
                "symbol": symbol,
                "data": data
            }
        else:
            raise Exception(f"Failed to fetch data, status code: {response.status_code}")

    except Exception as e:
        return {
            "status": False,
            "symbol": symbol,
            "message": str(e)
        }