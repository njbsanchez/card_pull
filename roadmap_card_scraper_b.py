# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime, date
import os
import fnmatch


from bs4 import BeautifulSoup
import json

from seleniumbase import Driver
import time

driver = Driver(uc=True)
driver.get("https://nowsecure.nl/#relax")
time.sleep(1)
# driver.quit()

# options = Options()


# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')



# driver = webdriver.Chrome(service=Service(ChromeDriverManager(version="114.0.5735.90").install()))


def parse_main_page(url):
    """
    takes in url of page, returns page source
    """
    
    driver.get(url)
    item_link = driver.find_elements(By.CLASS_NAME, value="item-link")
    cards_dictionary = {}
    
    counter = 0
    
    for link in item_link:
        # 
        
        if link.is_displayed():
            driver.execute_script("arguments[0].click();", link)
            time.sleep(1)
            current_url = driver.current_url
            # print(current_url)
            
        try:
            param = current_url.split("?&p=",1)[1]
            # print(param)
            counter += 1
            
        except:
            param = str("none")
            
        cards_dictionary[param]={'url':current_url}
        
        print("card dictionary url is ", cards_dictionary[param])
        
        # time.sleep(2)
        # url = cards_dictionary[param]['url']
        # driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        content = soup.find_all(class_="modal-inner")  

        cards_dictionary = get_card_info(content, cards_dictionary, param)
        
        
    print("# of cards: " + str(counter))
    print("# of cards in dictionary: " + str(len(cards_dictionary)))
        
    return cards_dictionary 

def desc_cleaner(desc):
    desc_list = desc.split("*^*")
    desc_str = ""
    # print(desc_list)
    for str in desc_list:
        new_str = str
        
        if '[' in str:
            str = str.replace("[","").replace("]","")
            link_lst = str.split("|")[::-1]
            
            new_str = '["' + ('"|'.join(link_lst)) + "]"
            # print("ITS new STRING: ****************" + new_str)
        
            
        desc_str = desc_str + new_str
    
    # print("NEW STRINGGGGGGG:" + desc_str)
    
    return desc_str
    
def get_card_info(content, cards_dictionary, param):
    
      
    for i,card in enumerate(content,start=1):
            
        try:
            title = str(card.h4.string)
        except:
            title = 'none'
        try:
            desc_init = str(((card.find(class_="description"))))
            desc_clean = desc_init.replace('<div class="description text-n900"><p>','').replace('<p class="description text-n900"><p>','').replace("</p></div>",'')
            desc_ = desc_clean.replace('<a href="',"*^*[ ").replace('">'," | ").replace("</a>"," ]*^*").replace("\xa0", "")
            desc = desc_cleaner(desc_).replace('<p>',' ').replace('</p>','').replace("</div>",'').replace('\r\n', "").replace('<p class="description text-n900">', "")
            desc 
        except:
            desc = 'none'
        try:
            status = str(card.find(class_="custom-category").contents[0])
        except:
            category = str("missing")
        try:
            category = str(card.find(class_="custom-category2").contents[0])
        except:
            category = str("none")
        try:
            date = str(card.find(class_="custom-field-1").contents[0])
        except:
            date = str("none")
        
        try:
            products = []
            for product in card.find(class_="custom-product").contents:
                products.append(str(product.string))
        except:
            products = ["none"]
        try:
            for product in card.find(class_="custom-productVersion").contents:
                    products.append(str(product.string))
        except:
            pass
        link_check={}
        links = ""
        try:
            for i, a in enumerate(card.find_all('a', href=True), start=1):
                print("LINK HERE:", a["href"])
                if "link-arrow" in a["class"]:
                    class_bool = "ok"
                else:
                    class_bool = "needs arrow"
                link_check[i]={
                    "title":a.get_text(),
                    "url":a["href"],
                    "arrow":class_bool
                }
                links = links + "[ " + link_check[i]["title"] + " | " + link_check[i]["url"] + " ],"
                # links.append(str(a['href']))
        except:
            pass
    
        cards_dictionary[param].update({
            'param':param,
            'title':title,
            'description':desc,
            'status':status,
            'category':category,
            'date':date,
            'products':products,
            'links':links,
            'link_check': link_check
            })
        
        print("CARD DICTIONARY ITEM:")
        print(cards_dictionary[param])
        print("*********************------**********************")
        
    return cards_dictionary
                
def get_data(url):
    
    
    cards_dictionary = parse_main_page(url)
    # add_to_dictionary(cards_dictionary)
    
    return cards_dictionary


def create_report(cards_dictionary, type, environment):
    
    today = date.today()
    now = datetime.now()
    
    path_name = f"~/Downloads/"
    path = os.path.expanduser(path_name)

    isExist = os.path.exists(path)

    if not isExist:

        os.makedirs(path)
        print("The new directory is created!")

    file_name = f'{type}_cards_{now}'
        
    with open(f'{path}/{file_name}.json', 'w') as outfile:
        json.dump(cards_dictionary, outfile)
    
    y=json.dumps(cards_dictionary)
    
    df = (pd.DataFrame.from_dict(cards_dictionary)).T
    file = f'{path}/{file_name}.csv'
    df.to_csv (file, index = False, header=True)
    
    return file
  
  
def parse_roadmap(roadmap_type, enviro):
    
    if roadmap_type == "cloud":
        route = "cloud"    
    elif str(roadmap_type) in  {"data-center", "dc", "DC"}:
        route = "data-center"
    else:
        return KeyError
    
    
    if enviro in {"author", "proof", "truth"}:
        url = f"https://author.marketing.internal.atlassian.com/wac/roadmap/{route}"
    elif enviro in {"prod", "production"}:
        url = f"https://atlassian.com/roadmap/{route}"
        # url = f"https://www.atlassian.com/wac/roadmap/cloud?&search=Collaborate%20in%20Zoom%20meetings%20to%20resolve%20issues"

        
    cards_dictionary = get_data(url)
    
    filename = create_report(cards_dictionary, roadmap_type, enviro)
    
    return filename

def what_product_area(product_area):
    """ 
    if product_area is Enterprise & Platform
        return link with....

    if product_area is Agile & DevOps
        return link with....

    if product_area is IT Solutions
        return link with....

    if product_area is Work Management
        return link with....

    if product_area is Enterprise & Platform 
        return link with....

    if product_area is DC Products
        return link with....
    """
    return product_area



if __name__ == "__main__":
    
    parse_roadmap('cloud', "author")
    # parse_roadmap('dc', "author")
    