from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def login_to_website(username, email, password,driver):
    # Access the webdriver
    try:
        # Open the login page
        driver.get('https://x.com/i/flow/login')

        # Page 1: Enter email and click Next
        enter_email(driver, email)

        # Check if username input is required
        try:
            enter_username(driver, username)
        except Exception as e:
            print(f'Username input not required: {e}')

        # Page 2: Enter password and login
        enter_password(driver, password)
        # # Pause to allow you to see the results
        # input("Press Enter to continue...")
    except Exception as e:
        return {
            "status":False,
            "message":"Unable to perform the login operation"
        }
    finally:
        return {
            "status":True,
            "message":"Login successfull"
        }

def enter_email(driver, email):
    emailField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
    )
    emailField.send_keys(email)

    nextButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-184id4b r-13qz1uu r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']"))
    )
    driver.execute_script("arguments[0].click();", nextButton)

def enter_username(driver, username):
    usernameField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@class='r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7']"))
    )
    usernameField.send_keys(username)

    nextButton2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1fkl15p r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']"))
    )
    # driver.execute_script("arguments[0].click();", nextButton2)
    ActionChains(driver).move_to_element(nextButton2).click().perform()

def enter_password(driver, password):
    passwordField = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
    )
    passwordField.send_keys(password)

    loginButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1fkl15p r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']"))
    )
    driver.execute_script("arguments[0].click();", loginButton)

# Example usage:
# if __name__ == "__main__":
#     username = 'DishantShah31'
#     email = 'dishantshah3133@gmail.com'
#     password = 'dishantusestwitter'

#     login_to_website(username, email, password)
