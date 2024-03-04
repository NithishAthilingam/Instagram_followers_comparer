#%%
import os
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import traceback
from selenium.common.exceptions import TimeoutException
from selenium import webdriver


#%%
url = "https://www.instagram.com/"

#%%
with open('credentials.json', 'r') as file:
    credentials = json.load(file)
username = credentials['username']
password = credentials['password']
profile_identifier = credentials.get('profile_identifier', username)

#%%
with open('selectors.json', 'r') as file:
    selectors = json.load(file)
followers_box_selector = selectors['followers_box']
followers_selector = selectors['followers']
followers_username_selector = selectors['followers_username']
followers_name_selector = selectors['followers_name']
close_followers_selector = selectors['close_followers']

following_box_selector = selectors['following_box']
following_selector = selectors['following']
following_username_selector = selectors['following_username']
following_name_selector = selectors['following_name']
close_following_selector = selectors['close_following']

#%%
options = uc.ChromeOptions()
# Other options and configurations...

# Get the current directory path

#dir_path = os.path.dirname(os.path.realpath(__file__))
#driver_path = os.path.join(dir_path, 'chromedriver')
driver = webdriver.Chrome()
# Instantiate the undetected Chrome driver with the explicit path
#driver = uc.Chrome(executable_path=driver_path, options=options)

#%%
# Open the desired URL
driver.get(url)

#%%
try:
    # Wait for the username field to be available and input the username
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username_field.send_keys(username)
except Exception as e:
    print(e)
#%%
try:
    # Wait for the password field to be available and input the password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys(password)
except Exception as e:
    print(e)
#%%
try:
    # Wait for the login button to be clickable and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
    )
    login_button.click()
except Exception as e:
    print(e)
#%%
try:
    # Wait for the first "Not now" button to be clickable and click it
    first_not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Not now']"))
    )
    first_not_now_button.click()
except Exception as e:
    print(e)
#%%
try:
    # Wait for the second "Not now" button to be clickable and click it
    second_not_now_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Not Now']"))
    )
    second_not_now_button.click()
except Exception as e:
    print(e)
#%%
try:
    profile_button_xpath = f"//a[contains(@href, '/{profile_identifier}/')]"
    profile_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, profile_button_xpath))
    )
    profile_button.click()
except Exception as e:
    print(e)
#%%
try:
    followers_link_xpath = f"//a[contains(@href, '/{username}/followers/')]"
    followers_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, followers_link_xpath))
    )
    followers_link.click()
except Exception as e:
    print(e)
#%%
try:
    # Define the CSS selector for the followers box
    css_selector_for_followers_box = followers_box_selector  # Replace with the actual CSS selector

    # Find the followers box using the correct method
    #followers_box = driver.find_element(By.CSS_SELECTOR, css_selector_for_followers_box)
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, followers_box_selector))
        )
        followers_box = driver.find_element(By.CSS_SELECTOR, followers_box_selector)
    except TimeoutException:
        print("Timed out waiting for followers box to load")
    except Exception as e:
        print("Error:", e)
    
    # Scroll within this element
    last_height = driver.execute_script("return arguments[0].scrollHeight", followers_box)
    while True:
        # Scroll down inside the element
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", followers_box)
        time.sleep(3)  # Wait to load more followers

        # Check if the scroll is at the bottom
        new_height = driver.execute_script("return arguments[0].scrollHeight", followers_box)
        if new_height == last_height:
            break
        last_height = new_height
except Exception as e:
    print(e)

#%%
try:
    # Extract HTML content from the followers box
    followers_html = followers_box.get_attribute('innerHTML')
        
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(followers_html, 'html.parser')

    # Find all the relevant divs
    divs = soup.find_all('div', class_=followers_selector)

    data = []
    for div in divs:
        username_span = div.find('span', class_=followers_username_selector)
        name_span = div.find('span', class_=followers_name_selector)

        # Ensure both username and name are found
        if username_span and name_span:
            username = username_span.get_text()
            name = name_span.get_text()
            data.append([username, name])

    # Writing to CSV
    with open('followers_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Name'])
        writer.writerows(data)
        
    print("Data extraction complete. CSV file created.")

except Exception as e:
    print("Error during data extraction:", e)
#%%
try:
    # Wait for the close button to be clickable and click it
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._abl-"))
    )
    close_button.click()
except Exception as e:
    print(e)

#%%
try:
    # Construct the XPath for the "Following" link
    following_link_xpath = f"//a[contains(@href, '/{username}/following/')]"
    
    # Wait for the "Following" link to be clickable and click it
    following_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, following_link_xpath))
    )
    following_link.click()
except Exception as e:
    print("Error:", e)
    print("Traceback:", traceback.format_exc())

#%%
try:
    # Define the CSS selector for the followers box
    css_selector_for_following_box = following_box_selector  # Replace with the actual CSS selector

    # Find the followers box using the correct method
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, following_box_selector))
        )
        following_box = driver.find_element(By.CSS_SELECTOR, following_box_selector)
    except TimeoutException:
        print("Timed out waiting for following box to load")
    except Exception as e:
        print("Error:", e)


    # Scroll within this element
    last_height = driver.execute_script("return arguments[0].scrollHeight", following_box)
    while True:
        # Scroll down inside the element
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", following_box)
        time.sleep(3)  # Wait to load more followers

        # Check if the scroll is at the bottom
        new_height = driver.execute_script("return arguments[0].scrollHeight", following_box)
        if new_height == last_height:
            break
        last_height = new_height
except Exception as e:
    print(e)

#%%
try:
    # Extract HTML content from the followers box
    following_html = following_box.get_attribute('innerHTML')
        
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(following_html, 'html.parser')

    # Find all the relevant divs
    divs = soup.find_all('div', class_=following_selector)

    data = []
    for div in divs:
        username_span = div.find('span', class_=following_username_selector)
        name_span = div.find('span', class_=following_name_selector)

        # Ensure both username and name are found
        if username_span and name_span:
            username = username_span.get_text()
            name = name_span.get_text()
            data.append([username, name])

    # Writing to CSV
    with open('following_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Name'])
        writer.writerows(data)
        
    print("Data extraction complete. CSV file created.")

except Exception as e:
    print("Error during data extraction:", e)
#%%
try:
    # Wait for the close button to be clickable and click it
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button._abl-"))
    )
    close_button.click()
except Exception as e:
    print(e)

#%%
# driver.implicitly_wait(10) 
# driver.quit()

# %%
