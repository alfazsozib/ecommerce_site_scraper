import selenium
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request


def web_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument('--headless')
    options.add_argument('--dns-prefetch-disable')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(executable_path="D:/chromedriver_96/chromedriver.exe", options=options)



def cat_link():
    driver = web_driver()
    url = ('https://www.metaly.eu/italienische-herstellerfirmen-eisenwaren')
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    

    driver.find_element_by_link_text('Produkte').click()
    time.sleep(3)

    links = driver.find_elements_by_xpath('/html/body/header/nav/ul/li[2]/ul/li/ul/li/a')

    cat_links = []

    for i in links:
        cat_links.append(i.get_attribute('href'))
    df = pd.DataFrame(cat_links)
    df.to_csv('links.csv')    

def product_link():
    driver = web_driver()
    df = pd.read_csv('links.csv')
    lns = df['Links'].values

    all_prod_links =[]
    for ln in lns:
        driver.get(ln)
        driver.maximize_window
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)

        prod_links = driver.find_elements_by_xpath('/html/body/main/section[2]/div/div/div[2]/ul/li/figure/div/a') 
        
        for i in prod_links:
            varlin = i.get_attribute('href')
            print(varlin)

            temp={
                'Links':varlin
            }
            all_prod_links.append(temp)
            df =pd.DataFrame(all_prod_links)
            df.to_csv('Product_Link.csv')

def data_scraper():  
    driver = web_driver()
    df = pd.read_csv('Product_Link.csv')
    lns = df['Links'].values

    all_data_container = []
    for pr_link in lns:
        driver.get(pr_link)
        driver.maximize_window
        url = requests.get(pr_link)
        time.sleep(3)

        soup = BeautifulSoup(url.content,'html.parser')
        tds = soup.find('table',{'class':'table'}).find_all('tr')[1:]
        for i in range(len(tds)):
            try:
                cat_1 = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[1]/div/div/h1').text
            except:
                cat_1 = ''

            try:
                cat_2 = driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/div[1]/div/div/h2').text
                # print(cat_2)
            except:
                cat_2 = ''
            try:
                father_article = driver.find_element_by_xpath('/html/body/main/section[2]/div/div[1]/div[2]/div/h3').text
            except:
                father_article = ''

        for tr in tds:
            code = ''
            child_name = ''
            des=''
            packaging =''
            num_piece =''
            type =''

            t_data = tr.find_all('td')
            code =  t_data[0].text
            child_name= t_data[1].text
            des = t_data[2].text
            packaging = t_data[3].text
            num_piece=t_data[4].text
            type_prod = t_data[5].text     

            temp ={
                'Category-1':cat_1,
                'Category-2':cat_2,
                'Father Article':father_article,
                'Code':code,
                'Child Article':child_name,
                'Description':des,
                'Packaging':packaging,
                'Number of pieces':num_piece,
                'Type':type_prod,
            }   

            all_data_container.append(temp)
            df = pd.DataFrame(all_data_container)
            df.to_csv('Data.csv')
        df = pd.DataFrame(all_data_container)
        df.to_csv('Data.csv')   

        img_num = driver.find_element_by_xpath('/html/body/main/section[2]/div/div[2]/table/tbody/tr[2]/td[1]').text
        img = driver.find_elements_by_xpath('/html/body/main/section[2]/div/div[1]/div[1]/a/img')

        for im in img:
            im_link = im.get_attribute('src')
            print(im_link)
            urllib.request.urlretrieve(im_link,f"E:\projects\METALY\Images\_{img_num}_.jpg")    
            if len(img) > 1:
                urllib.request.urlretrieve(im_link,f"E:\projects\METALY\Images\{img_num}_{chr(97,100)}.jpg")




if __name__ == "__main__":
    data_scraper()


