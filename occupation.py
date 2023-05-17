from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import json

chrome_options = webdriver.ChromeOptions()
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
   ChromeDriverManager().install(), options=chrome_options)


# 發送GET請求獲取網頁內容
url = "https://www.bls.gov/soc/2018/major_groups.htm"
driver.get(url)

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 找到包含職業分類的表格
table = soup.find_all("h3")

class_list={}
i=2
for title in table:
    #title_tag=title.find("a")
    #print(title.text)
    ul_index=i
    #print(ul_index)
    contents=driver.find_element(By.XPATH,"//*[@id='container']/div/div[4]/ul[" + str(ul_index) + "]")
    #print(contents)
    links_text = [link.text for link in contents.find_elements(By.TAG_NAME, "a") if link.get_attribute("class") == "question"]
    result = title.text[len("11-0000\u00a0 "):]
    class_list[result]={'content':links_text}
    i+=1

#print(class_list)

# 寫入 JSON 檔案
with open("data.json", "w") as file:
    json.dump(class_list, file)
