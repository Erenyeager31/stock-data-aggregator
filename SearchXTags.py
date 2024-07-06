from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from simple_chalk import chalk
import json
import time

# div for obtain the tweets
# css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu
# css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim

def Search(keyword,driver):
    try:
        enterKeyword(keyword,driver)
        ScrapTweet(driver,keyword)
        input('Enter -----')
    except Exception as e:
        print(e)
    finally:
        print('Try catch block has ended')

def enterKeyword(keyword,driver):
    searchField = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH,"//input[@class='r-30o5oe r-1dz5y72 r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-xyw6el r-13qz1uu r-fdjqy7']"))
    )

    searchField.send_keys(keyword+'\n')


"""
The following version of scrapper only managers to scrap 4 tweets per session
while the later one manages to scrap the required amount
"""
# def ScrapTweet(driver,keyword,tweet_count=15):
#     tweets = WebDriverWait(driver,10).until(
#         EC.presence_of_all_elements_located((By.XPATH,"//div[@class='css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu']"))
#     )

#     # with open('./ScrappedData/tweets.html','w',encoding='utf-8') as file:
#     #     all_tweets_html = ""
#     #     for tweet in tweets:
#     #         html_content = tweet.get_attribute("outerHTML")
#     #         all_tweets_html += html_content + "\n"

#     #     file.write(all_tweets_html)
#     #     print(chalk.green('Data saved as html succesfully'))

#     with open('./ScrappedData/TweetData'+keyword+'.json','w',encoding='utf-8') as file:
#         all_tweets = []
#         for tweet in tweets:
#             #? obtaining username
#             usernameDiv = tweet.find_element(By.XPATH,".//div[@class='css-175oi2r r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs']")
#             usernameAnchor = usernameDiv.find_element(By.TAG_NAME,"a")
#             username = usernameAnchor.get_attribute("href")

#             #? obtaining the tweet link
#             anchorDivofTweet = tweet.find_element(By.XPATH,".//a[@class='css-175oi2r r-1777fci r-bt1l66 r-bztko3 r-lrvibr r-1ny4l3l r-1loqt21']")
#             tweetLink = anchorDivofTweet.get_attribute('href').split("analytics")[0]

#             #? obtaining the post text
#             child_div_post = tweet.find_element(By.XPATH,".//div[@class='css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim']")
#             all_span_text = ""
#             # post text is obtained for a single post
#             for span in child_div_post.find_elements(By.XPATH,"span"):
#                 all_span_text += span.text.strip() + " "
            
#             #? obtaining the post image for a single post (url)
#             child_div_post_img = tweet.find_element(By.XPATH,".//div[@class='css-175oi2r r-9aw3ui r-1s2bzr4']")
#             all_anchor_tags = child_div_post_img.find_elements(By.TAG_NAME, "a")
#             # print(chalk.blue(all_anchor_tags))

#             all_img_url = []
#             for anchor_tag in all_anchor_tags:
#                 image_tag = anchor_tag.find_element(By.TAG_NAME, "img")
#                 img_url =  image_tag.get_attribute('src')
#                 img_url.replace('amp;','')
#                 all_img_url.append(img_url)
        
#             dataJson = {
#                 "username":username,
#                 "postText":all_span_text,
#                 "imgURLs":all_img_url,
#                 "tweetLink":tweetLink
#             }
#             all_tweets.append(dataJson)
        
#         jsonString = json.dumps(all_tweets)
#         file.write(jsonString)
#         print(chalk.green('Saved to file succesfully'))

def ScrapTweet(driver, keyword, tweet_count=15):
    try:
        all_tweets = []
        while len(all_tweets) < tweet_count:
            tweets = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='css-175oi2r r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu']"))
            )
            for tweet in tweets:
                #? Skip if tweet is already in the list
                if tweet in all_tweets:
                    continue

                #? obtaining username
                usernameDiv = tweet.find_element(By.XPATH, ".//div[@class='css-175oi2r r-1awozwy r-18u37iz r-1wbh5a2 r-dnmrzs']")
                usernameAnchor = usernameDiv.find_element(By.TAG_NAME, "a")
                username = usernameAnchor.get_attribute("href")

                #? obtaining the tweet link
                anchorDivofTweet = tweet.find_element(By.XPATH, ".//a[@class='css-175oi2r r-1777fci r-bt1l66 r-bztko3 r-lrvibr r-1ny4l3l r-1loqt21']")
                tweetLink = anchorDivofTweet.get_attribute('href').split("analytics")[0]

                #? obtaining the post text
                child_div_post = tweet.find_element(By.XPATH, ".//div[@class='css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim']")
                all_span_text = ""
                for span in child_div_post.find_elements(By.XPATH, "span"):
                    all_span_text += span.text.strip() + " "

                #? obtaining the post image for a single post (url)
                try:
                    child_div_post_img = tweet.find_element(By.XPATH, ".//div[@class='css-175oi2r r-9aw3ui r-1s2bzr4']")
                    all_anchor_tags = child_div_post_img.find_elements(By.TAG_NAME, "a")
                    all_img_url = []
                    for anchor_tag in all_anchor_tags:
                        image_tag = anchor_tag.find_element(By.TAG_NAME, "img")
                        img_url = image_tag.get_attribute('src')
                        img_url.replace('amp;', '')
                        all_img_url.append(img_url)
                except Exception as e:
                    all_img_url = []

                dataJson = {
                    "username": username,
                    "postText": all_span_text,
                    "imgURLs": all_img_url,
                    "tweetLink": tweetLink
                }
                all_tweets.append(dataJson)
                
                # Break if we have reached the desired tweet count
                if len(all_tweets) >= tweet_count:
                    break

            # print(chalk.red('Iteration :'),chalk.green(all_tweets))

            # Scroll down to load more tweets
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # wait for tweets to load

        # Save tweets to JSON file
        with open(f'./ScrappedData/TweetData_{keyword}.json', 'w', encoding='utf-8') as file:
            jsonString = json.dumps(all_tweets, ensure_ascii=False)
            file.write(jsonString)
            print(chalk.green('Saved to file successfully'))

            return {
                "status":True,
                "filePath":'./ScrappedData/TweetData_{keyword}.json'
            }
        
    except Exception as e:
        return {
            'status':False,
            'message':'Failed to scrap the tweets'
        }