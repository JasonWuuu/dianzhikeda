import os
from random import Random
from selenium import webdriver


# print(os.getenv('path'))

print(Random().random())


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('https://www.baidu.com')

    driver.find_element_by_name('wd').send_keys('Hello')
    driver.find_element_by_id('su').click()
    result = driver.find_element_by_tag_name('em')
    result.text()
    print(driver.find_element_by_tag_name('em').text)
