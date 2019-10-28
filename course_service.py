import os
import time
from selenium import webdriver
from selenium.webdriver import chrome, ChromeOptions
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import verify_code_service
import asyncio
from datetime import datetime, timedelta


def does_course_complete(nobr_element):
    """
    判断课程是否已做完
    :param nobr_element:
    :return:
    """
    try:
        nobr_element.find_element_by_xpath('span[@class ="scorm completed"]')
    except NoSuchElementException as ex:
        return False
    else:
        return True


def try_click_chapter(driver):
    """
    对于PPT的话，要点击最后一页 **************此路不通，只能人工****************
    :return:
    """
    try:
        # 跳出w_code，回到主页
        driver.switch_to.default_content()
        myframe = driver.find_elements_by_xpath("//frame[@name='w_content']//iframe[@name='w_sco']")
        driver.switch_to.frame(myframe)

        driver.find_element_by_xpath('//div[@class="chapter"]/span[last()]').click()
        print('PPT 最后一页已点击')
    except Exception as ex:
        print('做PPT出错了', ex)

    # 跳出w_code，回到主页
    driver.switch_to.default_content()
    driver.switch_to.frame('w_code')


def login(driver, username, password):
    """
    登录
    :param driver:
    :param username:
    :param password:
    :return:
    """

    driver.find_element_by_id('txtLoginName').send_keys(username)
    driver.find_element_by_id('txtPassword').send_keys(password)

    while True:
        # verify_code = input('请输入验证码')
        verify_code = verify_code_service.get_verify_code(driver)
        driver.find_element_by_id('txtVerifyCode').send_keys(verify_code)
        driver.find_element_by_id('login_button').click()
        time.sleep(2)

        try:
            if Alert(driver):
                Alert(driver).accept()
                continue
            else:
                break
        except:
            break


def do_all_course(driver, term='3(2019秋)'):
    """
    做所有课程
    :param driver:
    :param term:
    :return:
    """
    driver.switch_to.frame('f_M00370003')
    tr_list = driver.find_elements_by_xpath("//tr[starts-with(@class,'list_table_row')]")

    for tr_element in tr_list:
        term_element = tr_element.find_elements_by_tag_name('td')[2]
        course_name = tr_element.find_elements_by_tag_name('td')[1].text
        course_percent = tr_element.find_elements_by_tag_name('td')[6].text
        course_percent = float(course_percent[course_percent.rindex('[') + 1:].replace(']', ''))

        if term_element.text == term and course_percent <= 50:
            try:
                print(f'学期：{term_element.text}, 课程：{course_name}, 已看百分比：{course_percent}')
                do_course(driver, tr_element)
            except Exception as ex:
                print('做课程错误', ex)


def do_course(driver, tr_element):
    """
    开始做课程
    :param driver:
    :param tr_element:
    :return:
    """

    start_to_study_link = tr_element.find_element_by_xpath("td/a[contains(text(),'开始学习')]")

    # 点击开始学习，跳转到第三个TAB
    start_to_study_link.click()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[2])
    driver.switch_to.frame('w_main')
    any_link = driver \
        .find_element_by_xpath(
        "//table[@class='topic_border'][2]//a[starts-with(@href,'javascript:showLearnContent')]") \
        .click()

    # 左侧菜单
    time.sleep(5)
    driver.switch_to.frame('w_code')

    # 展开所有菜单
    expand_all_menu(driver)
    # 展开所有菜单,再确认
    expand_all_menu(driver)

    time.sleep(30)

    # 找到所有要做的课程的链接里的一个标记
    all_course_link_span = driver.find_elements_by_xpath('//span[@class = "h_content h_scorm_content"]')
    for course_link_span in all_course_link_span:
        try:
            look_video(driver, course_link_span)
        except Exception as ex:
            print('看视频错误', ex)

    # 做完后，关闭第三个TAB，并回到第二个TAB
    # driver.close()


def expand_all_menu(driver):
    """
    展开所有菜单
    :return:
    """
    while True:
        try:
            has_plus_node = False
            plus_nodes = driver.find_elements_by_xpath("//img[contains(@src,'plusnode.gif')]")

            for plus_node in plus_nodes:
                # print(plus_node.get_property('onclick'))
                if EC.element_to_be_clickable(plus_node):
                    plus_node.click()
                    has_plus_node = True
        except Exception as ex:
            pass

        if not has_plus_node:
            break


def look_video(driver, course_link_span):
    """
    真正看视频的核心
    :return:
    """
    # 课程的链接
    course_link = course_link_span.find_element_by_xpath('..')
    print('课程名:', course_link.text, end='')
    # 课程是否做完的一成功标记
    nobr_element = course_link.find_element_by_xpath('..')

    # 课程链接是否被点击过
    does_course_link_clicked = False
    # 课程开始时间
    course_start_time = datetime.now()

    while True:

        if does_course_complete(nobr_element):
            # 如果课程已完成
            print(', 状态：已完成')
            break
        else:
            # 如果课程未完成，就点击一下此课程链接
            if EC.element_to_be_clickable(course_link) and not does_course_link_clicked:
                course_link.click()
                does_course_link_clicked = True
                print(', 状态：正在做...', end='')

        time.sleep(30)
        print('.', end='')

        # 超时间为5分钟
        timeout_time = course_start_time + timedelta(minutes=5)
        if datetime.now() > timeout_time:
            print('超时，跳过此章节')
            break


def execute(username, password):
    print('start to new a web driver')
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)

    driver.get('http://www.uestcedu.com/')

    login_element = driver.find_element_by_link_text('学生及管理员统一身份认证入口')
    login_element.click()

    # 进入第二个TAB
    driver.switch_to.window(driver.window_handles[1])

    # 登录
    login(driver, username, password)

    # 点击在线学习
    driver.find_element_by_xpath("//a[contains(text(),'在线学习')]").click()
    time.sleep(2)
    if Alert(driver):
        Alert(driver).accept()

    time.sleep(5)

    # 做所有课程
    try:
        do_all_course(driver, '3(2019秋)')
    except Exception as ex:
        print('做所有课程错误', ex)

    # 退出driver
    # driver.quit()
    