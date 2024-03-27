import requests
import re
import json
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#curl -s https://mib.gov.in/mann-ki-baat | grep -o '<div class="left-col-lg-6" style="float:left">.*</div>' | grep -o '<a[^>]*href="[^"]*\.pdf"' | awk -F '"' '{print $2}'

#this scarps url form html pages of https://mib.gov.in/mann-ki-baat
def return_url():
    base_url = "https://mib.gov.in/mann-ki-baat?page={}"
    pdf_urls = []
    for page_num in range(0, 4):

        url = base_url.format(page_num)
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            div_pattern = r'<div class="left-col-lg-6" style="float:left">(.*?)</div>'
            pdf_link_pattern = r'<a[^>]*href="([^"]*\.pdf)"'
            div_matches = re.findall(div_pattern, html_content, re.DOTALL)

            for div_match in div_matches:
                pdf_links = re.findall(pdf_link_pattern, div_match)
                pdf_urls.extend(pdf_links)
        else:
            print(f"Failed to retrieve content from page {page_num}. Status code: {response.status_code}")

    return pdf_urls

#this filter english urls from all scrapped links 
def filter_english_url(arr_of_txt):
    pattern = re.compile(r"English|english|ENGLISH")
    matches = [element for element in arr_of_txt if pattern.search(element)]
    return matches

#python array to json
def array_to_json(name,array):
    file_path = name
    with open(file_path, 'w') as json_file:
        json.dump(array, json_file)

#reads json array and return to python
def read_json(name):
    file_path = name
    with open(file_path, 'r') as json_file:
        python_array = json.load(json_file)
        return python_array

#this scraps data from offical PM website.
#Do-note its perfectly legal to scrap data and cite source 
# given that its not presneted in deogratry manner
def return_url_txt(driver):
    # url = "https://www.pmindia.gov.in/en/news-updates/"
    url= "https://www.pmindia.gov.in/en/tag/mann-ki-baat/"
    pdf_urls = []
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='news-description ']")))

    last_height = driver.execute_script("return document.body.scrollHeight")
    print("1. it started working")
    while True:
        print("2. in a loop")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(8)  # Adjust the interval (in seconds) as needed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    print("3. parsing started->")
    time.sleep(10)


    
    html_content = driver.page_source

    aside_pattern = r'<div class="news-description ">(.*?)</div>'
    link_pattern = r'<a[^>]*href="([^"]*)"'

    div_matches = re.findall(aside_pattern, html_content, re.DOTALL)

    for div_match in div_matches:
        pdf_links = re.findall(link_pattern, div_match)
        for link in pdf_links:
            pdf_urls.append(link)
    print("array returned-> ")

    return pdf_urls




#initilizing driver for scrapping from https://www.pmindia.gov.in/en/news-updates/

#demo runs




##initilizing driver for scrapping from https://www.pmindia.gov.in/en/news-updates/

# options = webdriver.ChromeOptions()
# options.add_argument("--headless") 
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537.36")
# driver = webdriver.Chrome(options=options)




##script to scarp links from pmo https://www.pmindia.gov.in/en/news-updates/"
# output=return_url_txt(driver)
# print(output)
# print(len(output))
##saving pmo links into json
# array_to_json("pmo_links.json",output)



##script to scarp links from pmo https://mib.gov.in/mann-ki-baat
# output_man=return_url()
# print(output_man)
# print(len(output_man))
##saving mann-ki-baat links into json
# array_to_json("man-ki-baat.json",output_man)


