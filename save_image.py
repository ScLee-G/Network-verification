from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
import os

def screenshot(save_path, company_name, web_name, input_box_name, url, key_word):
    try:
        # Create driver
        options = webdriver.ChromeOptions()
        # Hide the Chrome window
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        # Delete "Chrome 正受到自动测试软件的控制"
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        driver = webdriver.Chrome(chrome_options=options)
        # driver = driver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])

        # Get url of target website
        driver.get(url)

        # Find the address of search component(input_box)
        if key_word == "name":
            input_box = driver.find_element(by=By.NAME, value=input_box_name)
        else:
            if key_word == "id":
                input_box = driver.find_element(by=By.ID, value=input_box_name)

        # Clear input box
        input_box.clear()
        # Type in company_name
        input_box.send_keys(company_name)
        input_box.send_keys(Keys.ENTER)

        # Screenshot
        time.sleep(1)
        driver.maximize_window()
        time.sleep((random.randint(4,8)))

        # Get multiple open window handles
        windows = driver.window_handles
        # Switch to the newest window
        driver.switch_to.window(windows[-1])

        width = max(1920, driver.execute_script("return document.documentElement.scrollWidth"))
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width + 20, height + 20)

        # Scroll problems
        driver.execute_script(execute_script)
        for i in range(30):
            if 'scroll-done' in driver.title:
                break

        time.sleep(3)
        # Save the screenshot to png format
        # driver.save_screenshot(path_way)
        if os.path.exists(save_path):
            os.remove(save_path)

        driver.get_screenshot_as_file(save_path)
        print("{} {}：截图成功".format(company_name, web_name))
        driver.quit()

    except Exception as e:
        print("{} {}: 截图失败 fail".format(company_name, web_name))