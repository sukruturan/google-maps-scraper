# GOOGLE MAPS Web Scraper - project initialization
#IMPORT MODULES
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import openpyxl
from bs4 import BeautifulSoup
import random
import re

#DESCIPTION URL AND BASE AGENT 
USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.6668.89 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
} 
BASE_URL="https://www.google.com/maps/"

#CHROME SETTİNGS
options=webdriver.ChromeOptions()
options.add_experimental_option("detach",False)
options.add_argument("--start-maximazed")
options.add_argument(f"--user-agent={USER_AGENT}")

#OPEN CHROME
driver=webdriver.Chrome(options=options)
actions=ActionChains(driver)
try:
    driver.get(BASE_URL)
    driver.maximize_window()
    WebDriverWait(driver,15).until(EC.presence_of_all_elements_located((By.TAG_NAME,"body")))
    print("PAGE OPENED")
except:
    print("PAGE NOT OPEN")
class SeleniumButtons:
    def press_buton_class_name(the_driver,class_name):
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,class_name)))
            buton=the_driver.find_element(By.CLASS_NAME,class_name)
            actions.move_to_element(buton).perform()
            buton.click()
            time.sleep(1)
        except:
            print("class name tuşlama yapılmadı")
            pass
    def press_button_id(the_driver,id):
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,id)))
            button=the_driver.find_element(By.ID,id)
            actions.move_to_element(button).perform()
            button.click()
            time.sleep(1)
        except:
            print("id tuşlama yapılmadı")
            pass
    def press_button_css_selector(the_driver,css_selector):
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,css_selector)))
            buton=the_driver.find_element(By.CSS_SELECTOR,css_selector)
            actions.move_to_element(buton).perform()
            buton.click()
            time.sleep(1)
        
        except:
            print("css selectore göre tuslama yapılmadı")
            pass
    def press_buton_xpath(the_driver,xpath):
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,xpath)))
            buton=the_driver.find_element(By.XPATH,xpath)
            actions.move_to_element(buton).perform()
            buton.click()
            time.sleep(1)
        except:
            print("xpathe göre tuşlama yapılmadı")
            pass
    def scroll_to_bottom(start,finish):
        driver.execute_script(f'window.scrollTo({start},{finish});')
        time.sleep(1)
    def find_elements_css(the_driver,css_selector):
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,css_selector)))
            buton=driver.find_elements(By.CSS_SELECTOR,f"{css_selector}")
            actions.move_to_element(buton).perform()
            buton.click()
            time.sleep(1)
        except:
            print("css selectore göre bulunamadı")
            pass  
    def find_elements_classname(the_driver,css_selector):
        try:
            WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME,css_selector)))
            buton=the_driver.find_elements(By.CLASS_NAME,f"{css_selector}")
            actions.move_to_element(buton).perform()
            buton.click()
            time.sleep(1)
        except:
            print("class name göre bulunamadı")
def search_google(input):
    wait = WebDriverWait(driver, 15)
    # Arama kutusunu bul
    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    # Var olan yazıyı temizle
    search_box.clear()
    # Arama metni
    search_box.send_keys(input)
    # Arama butonuna bas
    wait.until(EC.element_to_be_clickable((By.ID, "searchbox-searchbutton")))
    # Alternatif (buton yerine enter):
    search_box.send_keys(Keys.ENTER)
def get_link(the_driver,link_numbers):
    list_links = []
    while len(list_links) < link_numbers:
        cards = the_driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")

        for card in cards:
            try:
                a_tag = card.find_element(By.XPATH, ".//a[contains(@href,'/maps/place')]")
                href = a_tag.get_attribute("href")
                
                if href and href not in list_links:
                    list_links.append(href)
                    # 30 olunca anında dur
                    if len(list_links) >= link_numbers:
                        break

            except:
                pass

        # Son kart varsa ona scroll yap
        if len(cards) > 0:
            driver.execute_script("arguments[0].scrollIntoView();", cards[-1])
        else:
            # Kart yoksa normal scroll yap
            driver.execute_script("window.scrollBy(0, 800);")

        time.sleep(1.3)

    print("\n✅ Toplam Toplanan Link:", len(list_links))
    return list_links
def open_page(the_driver,the_list_link):
    result=[]
    for link in the_list_link:
        driver.get(link)
        time.sleep(1)
        WebDriverWait(the_driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"keynav-mode-off")))
        title = driver.find_element(By.TAG_NAME, "h1").text.strip()
        address = driver.find_element(By.CSS_SELECTOR, "div.Io6YTe").text.strip()
        try:
            phone = driver.find_element(By.CSS_SELECTOR, "button[data-item-id^='phone:tel:']").get_attribute("data-item-id").replace("phone:tel:", "")
        except:
            print("no number")
        rating = driver.find_element(By.CSS_SELECTOR, "div.F7nice > span > span[aria-hidden='true']").text.replace(",", ".")

        result.append({
                    "title": title,
                    "address": address,
                    "phone": phone,
                    "rating": rating
                })
    return result
search_google("istanbul beşiktaş")
time.sleep(8)
search_google("bar")
list_link=get_link(driver,50)
list_link=list_link[:50]
result=open_page(driver,list_link)
df=pd.DataFrame(result)
df.to_excel("restoran.xlsx")
print(df)

