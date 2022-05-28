from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import List
import csv

url = 'https://technext.ng/category/stories/'
pref = {"profile.managed_default_content_settings.images" : 2}
PATH = Service('C:\Program Files\chromedriver.exe')
options = Options()
options.add_experimental_option('prefs', pref)
# options.headless = True

driver = webdriver.Chrome(service=PATH, options=options)
driver.get(url)

# Click on the notification pop-up that appears when the page loads
WebElement 
button1 = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(((By.XPATH, './/*[@id="onesignal-slidedown-cancel-button"]'))));
button1.click();

WebElement 
button2 = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, 'eicon-close')));
button2.click();

def ReadMore(driver):

    """ This function clicks 'readmore' until it reaches the end of the page """

    while (EC.visibility_of_element_located((By.XPATH, './/*[@id="primary"]/div[2]/div[2]/button'))):
        try:
            WebElement 
            button3 = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, './/*[@id="primary"]/div[2]/div[2]/button')));
            button3.click();
        except:
            break

def get_valid_urls() -> List[str]:

    """ This function gets all the valid article urls and returns it in a list-set """

    ReadMore(driver)
    content = driver.page_source
    soup = bs(content)
    all_urls = soup.findAll("a")
    valid_article_urls = []
    for url in all_urls:
        href = url.get("href")

        if (href.startswith("https://technext.ng/20") \
            and href[21].isdigit() and not href.startswith("https://technext.ng/category")):
            story_url =  href
            valid_article_urls.append(story_url)
            valid_article_urls = list(dict.fromkeys(valid_article_urls))
    return list(set(valid_article_urls))



def get_articles():

    """ This function gets the article content and writes it in a file """

    urls = get_valid_urls()
    with open('data/technext.csv', "w+", encoding='utf-8') as csv_file:
        headers = ["headline", "story"]
        writer = csv.DictWriter(csv_file, delimiter="\t", fieldnames = headers)
        writer.writeheader() 
        for i in urls:
            driver.get(i)
            content = driver.page_source
            soup = bs(content)
            headline = soup.find("h1", attrs={"class": 'cs-entry__title'}).text.strip()
            story = soup.find("div", attrs={"class": 'entry-content'}).text.strip()

            writer.writerow(
                   { headers[0]:headline,
                     headers[1]:story}) 
    print('Done!!!')                            
get_articles()


driver.close()
