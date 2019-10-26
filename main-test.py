from dotenv import load_dotenv, find_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver import chrome, ChromeOptions
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import verify_code_service

load_dotenv(find_dotenv(filename='.env'))


def does_course_complete(nobr_element):
    try:
        nobr_element.find_element_by_xpath('span[@class ="scorm completed"]')
    except NoSuchElementException as ex:
        return False
    else:
        return True

# print('Hello')

print(os.getenv('DRIVER_PATH'))

driver = webdriver.Chrome()
driver.implicitly_wait(30)

driver.get('http://www.uestcedu.com/')

login_element = driver.find_element_by_link_text('学生及管理员统一身份认证入口')
login_element.click()
driver.switch_to.window(driver.window_handles[1])

driver.find_element_by_id('txtLoginName').send_keys('V181180044201003')
driver.find_element_by_id('txtPassword').send_keys('237037')

driver.save_screenshot('screen_shoot.png')
driver.get_screenshot_as_base64()




while True:
    # verifyCode = input('请输入验证码')
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

driver.find_element_by_xpath("//a[contains(text(),'在线学习')]").click()
if Alert(driver):
    Alert(driver).accept()

time.sleep(3)
driver.switch_to.frame('f_M00370003')
tr_list = driver.find_elements_by_xpath(
    "//tr[starts-with(@class,'list_table_row')]")

for tr in tr_list:
    term = tr.find_elements_by_tag_name('td')[2]

    if term.text == '3(2019秋)':
        course_name = tr.find_elements_by_tag_name(
            'td')[1].text
        start_to_study_link = tr.find_element_by_xpath(
            "td/a[contains(text(),'开始学习')]")
        print(f'学期：{term.text}, 课程：{course_name}')

        start_to_study_link.click()
        time.sleep(5)

        driver.switch_to.window(driver.window_handles[2])
        driver.switch_to.frame('w_main')
        any_link = driver.find_element_by_xpath(
            "//table[@class='topic_border'][2]//a[starts-with(@href,'javascript:showLearnContent')]").click()

        # 左侧菜单
        time.sleep(5)
        driver.switch_to.frame('w_code')

        # 展开所有菜单
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

        time.sleep(30)
        all_course_link_span = driver.find_elements_by_xpath('//span[@class = "h_content h_scorm_content"]')
        for course_link_span in all_course_link_span:
            # 课程的链接
            course_link = course_link_span.find_element_by_xpath('..')
            print('课程名:', course_link.text, end='')
            # 课程是否做完的一成功标记
            nobr_element = course_link.find_element_by_xpath('..')

            # 课程链接是否被点击过
            does_course_link_clicked = False

            # 真正看视频的核心部分
            while True:
                if does_course_complete(nobr_element):
                    # 如果课程已完成
                    print(', 状态：已完成')
                    break
                else:
                    # 如果课程未完成，就点击一下此课程链接
                    print(', 状态：正在做...')
                    if EC.element_to_be_clickable(course_link) and not does_course_link_clicked:
                        course_link.click()
                        does_course_link_clicked = True
                time.sleep(30)

        break

time.sleep(10)



# driver.quit()
