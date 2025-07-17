import os
import pandas as pd
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import numpy as np

from DAOs import draftDAO, pickDAO, playerDAO, userDAO


draft_id_list = np.load('draft_id_list.npy')
n = len(draft_id_list)

if (not draft_id_list):
    draft_id_list = np.array([])

load_dotenv()

USER_ID=os.getenv("USER_ID")

# Set up Selenium WebDriver (make sure to have ChromeDriver installed)
options = webdriver.ChromeOptions()
options.headless = False  # Disable headless mode for debugging

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)

print(draft_id_list)


## move to completed drafts tab
try:
    comp_button = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(By.XPATH, f'contains(text(), "{os.getenv("COMP_BUTTON")}")]')
    )

    comp_button.click()
except:
    raise Exception('something went wrong clicking complete tab')

## retrieve the draft html elements so that they can be clicked
try:
    draft_element_list = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(By.XPATH, '//div[contains(@class, "draft-list")]')
    )
except:
    raise Exception('something went wrong getting list of drafts from the page')

## prepare list for drafts that have not been analyzed
new_draft_id_list = np.array([])

## manipulate each new draft element / add data to app/server/etc. 
for i in range(0, len(draft_element_list) - n):
    ## ensure that we are back to the page with the list of drafts before clicking on the 
    ## next available draft, starting at the top
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        draft_element_list[i].click()
    ))
    url = driver.current_url

    draft_id = url.split('/')[3]
    # draft_id_list = np.append(draft_id_list, draft_id)
    np.append(new_draft_id_list, draft_id)

    ## get individual draft info (need the draft slot of our user)
    try:
        draft_info = requests.get(f"https://api.sleeper.app/v1/draft/{draft_id}")
    except Exception as e:
        raise Exception(f'sleeper api error - {e}')
    
    ## this is the identifier for our picks
    draft_slot = draft_info["draft_order"][f"{USER_ID}"]

    ## get all picks made by our user in this draft
    try:
        all_picks = requests.get(f"https://api.sleeper.app/v1/draft/{draft_id}/picks")
    except Exception as e:
        raise Exception(f'sleeper api error for picks - {e}')
    
    ## filter all picks by our identifier
    my_picks = [item for item in all_picks if item.get("draft_slot") == f"{draft_slot}"]

    ## do something with pick info
    #############################

    ## navigate back to page of draft list
    driver.back()

## add all new elements to the draft_id_list, save lists
np.append(new_draft_id_list, draft_id_list)

np.save('draft_id_list.npy', draft_id_list)
np.savetxt('draft_id_list.txt', draft_id_list, delimiter=', \n')

## check for accuracy
if len(np.unique(draft_id_list)) < len(draft_id_list):
    raise Exception('duplicate id added to list')

## driver quit
driver.quit()



