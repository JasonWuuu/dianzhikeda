import os
import asyncio
from selenium import webdriver
import time
from datetime import datetime
import aiohttp
import pandas as pd


def toutiao_search(*keywords):
    driver = webdriver.Chrome()
    driver.get('https://www.toutiao.com/')

    result = pd.DataFrame(columns=['title', 'link'])
    for keyword in keywords:
        df = toutiao_get_article(driver, keyword)
        # result.append(df, ignore_index=True)
        # df = pd.DataFrame([{"title":1, 'link':2}],columns=['title','link'])
        result = result.append(df, ignore_index=True)

    result.to_csv('toutiao_result.csv', encoding='utf-8')
    driver.quit()


def toutiao_get_article(driver: webdriver.Chrome, keyword):
    # 进入第一个TAB
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_class_name('tt-input__inner').clear()
    driver.find_element_by_class_name('tt-input__inner').send_keys(keyword)
    driver.find_element_by_class_name('tt-button--default').click()
    # 进入第二个TAB
    driver.switch_to.window(driver.window_handles[1])
    # driver.get(f'https://www.toutiao.com/search/?keyword={keyword}')
    time.sleep(3)

    title_elements = driver.find_elements_by_class_name('title-box')

    result = []
    for title_element in title_elements:
        title = title_element.find_element_by_class_name('J_title')
        link = title_element.find_element_by_tag_name('a')
        result.append(
            {'title': title.text, 'link': link.get_attribute('href')})
    df = pd.DataFrame(result, columns=['title', 'link'])
    driver.close()
    return df


def baidu_search(*keywords):
    driver = webdriver.Chrome()
    driver.get('https://www.baidu.com/')

    result = pd.DataFrame(columns=['title', 'link'])
    for keyword in keywords:
        df = baidu_get_article(driver, keyword)
        # result.append(df, ignore_index=True)
        # df = pd.DataFrame([{"title":1, 'link':2}],columns=['title','link'])
        result = result.append(df, ignore_index=True)

    result.to_csv('baidu_result.csv', encoding='utf-8')
    driver.quit()


def baidu_get_article(driver: webdriver.Chrome, keyword):
    # 进入第一个TAB
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_id('kw').clear()
    driver.find_element_by_id('kw').send_keys(keyword)
    driver.find_element_by_id('su').click()
    time.sleep(3)

    container_elements = driver.find_elements_by_xpath(
        '//div[@id = "content_left"]/div[@tpl = "se_com_default"]')
    result = []
    for item in container_elements:
        link = item.find_element_by_tag_name('a')
        result.append(
            {'title': link.text, 'link': link.get_attribute('href')})

    df = pd.DataFrame(result, columns=['title', 'link'])
    return df

if __name__ == '__main__':
    # toutiao_search('油菜籽种植终获得补贴，下年度产量有望触底反弹', '十月以来，连盘玉米小阳春接受秋冬天气考验')
    # baidu_search('油菜籽种植终获得补贴，下年度产量有望触底反弹', '十月以来，连盘玉米小阳春接受秋冬天气考验')
    name ='wucong'

    names =['congcong','wucong','cong']

    print(name in names)