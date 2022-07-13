import grequests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from collections import OrderedDict
from typing import List, Dict
import yaml
import time
import argparse
import logging
import multiprocessing
import csv
import glob
import os
import pandas as pd
from functools import partial



logging.root.setLevel(logging.INFO)
CONFIG = yaml.load(open("config.yml"), Loader=yaml.FullLoader)


pref = {"profile.managed_default_content_settings.images" : 2}
PATH = Service('C:\Program Files\chromedriver.exe')
options = Options()
options.add_experimental_option('prefs', pref)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# options.headless = True


def init_driver(url, driver):

    """ This function initializes the driver and then bypass the notification pop-ups"""
    
    driver.get(url)

    # Click on the notification pop-up that appears when the page loads
    WebElement 
    button1 = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(((By.XPATH, CONFIG['CANCEL_BUTTON_XPATH'])))
    );
    button1.click();

    WebElement 
    button2 = WebDriverWait(driver, 25).until(
        EC.visibility_of_element_located((By.CLASS_NAME, CONFIG['CANCEL_BUTTON_CLASS']))
    );
    button2.click();

    return driver

def get_parser() -> argparse.ArgumentParser:
     """
    parse command line arguments

    returns:
        parser - ArgumentParser object
    """

    parser = argparse.ArgumentParser(description='TechNext Scraper')
    parser.add_argument(
        '--output_file_name',
        type=str,
        default='technext.csv',
        help='Name of outpit file'
)
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='remove sub-topic csv files created before combining'
)
    return parser
def ReadMore(driver):

    """  This function clicks 'readmore' until it reaches the end of the page """

    while (EC.visibility_of_element_located((By.XPATH, CONFIG['LOAD_MORE_XPATH']))):
        try:
            WebElement 
            button3 = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, CONFIG['LOAD_MORE_XPATH']))
            );
            button3.click();
        except:
            break
    return driver
    


def get_valid_urls(driver) -> List[str]:

    """ This function gets all the valid article urls and returns it in a list-set."""

    
    content = driver.page_source
    soup = bs(content, 'html.parser')
 
    all_urls = soup.findAll("a")
    valid_article_urls = []
    for url in all_urls:
        href = url.get("href")

        if (href.startswith("https://technext.ng/20") \
            and href[21].isdigit() and not href.startswith("https://technext.ng/category")):
            story_url =  href
            valid_article_urls.append(story_url)
       
    return list(OrderedDict.fromkeys(valid_article_urls))

def get_data():

    """ This function makes requests to all urls aschronuously and returns the responses in a list."""

    urls = get_valid_urls(driver)
    reqs = [grequests.get(url) for url in urls]
    resp = grequests.map(reqs)
    return resp

def split_data() -> Dict :

    """ 
    This Function splits the acquired responses from the urls into a nested list
    then converts it into a dictionary for multiprocessing.
    """

    resp = get_data()
    chunk_size = len(resp)//5
    chunked_list = [resp[i:i+chunk_size] for i in range(0, len(resp), chunk_size)]
    index_ = [1,2,3,4,5]
    chunked_dict = dict(zip(index_, chunked_list))
    return chunked_dict






def get_articles( output_file_name, resp, index_):

    """ This function parses the responses, gets the article content and writes it in a file """
    
    
    path = output_file_name.split("/")

    output_file_name = os.path.join(path[0], f"{index_}_{path[1]}")
    with open(output_file_name, "w+", encoding='utf-8') as csv_file:
        headers = ["headline", "story"]
        writer = csv.DictWriter(csv_file, delimiter="\t", fieldnames = headers)
        writer.writeheader() 
       
        for r in resp:
            soup = bs(r.text, 'html.parser')
            headline = soup.find("h1", attrs={"class": CONFIG['HEADLINE_CLASS']}).text.strip()
            story = soup.find("div", attrs={"class": CONFIG['STORY_CLASS']}).text.strip()

            writer.writerow(
                   { headers[0]:headline,
                     headers[1]:story}) 
    logging.info("--------------------------------------")
    logging.info(f"Scraping done for index{index_}...")
    logging.info("--------------------------------------")  

if __name__ == '__main__':  
    url = CONFIG['CATEGORY_URL']
    driver = webdriver.Chrome(service=PATH, options=options)

    init_driver(url, driver)
    logging.info("--------------------------------------")
    logging.info("Initialized driver...")
    logging.info("--------------------------------------")  
    time.sleep(5)
    ReadMore(driver)


    parser = get_parser()
    params, _ = parser.parse_known_args()
  
    
    split_ = split_data()
  
    logging.info("--------------------------------------")
    logging.info("Aquired vaild urls...")
    logging.info("--------------------------------------")   
    
  
   
    driver.close()

    
   
    logging.info("--------------------------------------")
    logging.info("Starting scraping...")
    logging.info("--------------------------------------")    

    pool = multiprocessing.Pool()

    processes = [
        pool.apply_async(
            get_articles, 
            args=(params.output_file_name, resp_, index_) 
            ) for index_, resp_ in split_.items()
        
    ]
    result = [p.get() for p in processes]

    path = params.output_file_name.split("/")
    output_file_pattern = os.path.join(path[0], f"*_{path[1]}")
    category_file_names = glob.glob(output_file_pattern)

    reader = partial(pd.read_csv, sep="\t")
    all_dfs = map(reader, category_file_names)
    corpora = pd.concat(all_dfs)     
    corpora.to_csv(params.output_file_name, sep="\t", index=False)

    if params.cleanup:
        for f in category_file_names:
            os.remove(f)





