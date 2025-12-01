import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import random
import json
import logging
import datetime
import tempfile
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def print_html_time(save_path, save_file_name, company_name, web_name, input_box_name, url, key_word):
    driver = None
    try:
        # 创建保存目录（如果不存在）
        os.makedirs(save_path, exist_ok=True)
        
        judge = os.path.join(save_path, save_file_name)
        if os.path.exists(judge):
            logger.info(f"文件已存在，跳过: {save_file_name}")
            return
            
        # 检查必要参数
        if not url or not input_box_name or key_word not in ['name', 'id']:
            logger.error(f"无效参数: url={url}, input_box_name={input_box_name}, key_word={key_word}")
            print(f"{company_name} {web_name}: 保存失败 (参数错误)")
            return
        
        chrome_options = webdriver.ChromeOptions()
        settings = {
            "recentDestinations": [{
                "id": "Save as PDF",
                "origin": "local"
            }],
            "selectedDestinationId": "Save as PDF",
            "version": 2,
            "displayHeaderFooter": True,
            "mediaSize": {
                "height_microns": 297000,
                "name": "ISO_A4",
                "width_microns": 210000,
                "custom_display_name": "A4"
            },
        }

        # 添加必要的Chrome选项
        chrome_options.add_argument('--enable-print-browser')
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_argument('--no-sandbox')  # 避免权限问题
        chrome_options.add_argument('--disable-dev-shm-usage')  # 解决资源限制问题
        chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
        chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
        
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(settings),
            'savefile.default_directory': save_path
        }
        chrome_options.add_argument('--kiosk-printing')
        chrome_options.add_experimental_option('prefs', prefs)

        # 降级方案：使用headless模式并添加更多的Chrome选项
        # 这种模式更稳定，且不需要可视化界面
        chrome_options.add_argument('--headless')  # 使用无头模式
        chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
        chrome_options.add_argument('--window-size=1920x1080')  # 设置窗口大小
        chrome_options.add_argument('--disable-extensions')  # 禁用扩展
        chrome_options.add_argument('--disable-popup-blocking')  # 禁用弹窗阻止
        chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
        chrome_options.add_argument('--no-sandbox')  # 禁用沙盒
        chrome_options.add_argument('--disable-dev-shm-usage')  # 解决资源限制
        chrome_options.add_argument('--remote-debugging-port=9222')  # 启用远程调试
        chrome_options.add_argument('--disable-features=site-per-process')  # 禁用站点隔离
        
        # 使用本地下载的ChromeDriver
        try:
            # 指定本地ChromeDriver路径
            chromedriver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chromedriver', 'chromedriver-win32', 'chromedriver.exe')
            logger.info(f"使用本地ChromeDriver: {chromedriver_path}")
            
            # 配置WebDriver超时设置
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            # 设置隐式等待时间
            driver.implicitly_wait(30)
            # 设置页面加载超时
            driver.set_page_load_timeout(60)
            # 设置脚本执行超时
            driver.set_script_timeout(45)
        except Exception as e:
            logger.error(f"ChromeDriver初始化失败: {str(e)}")
            # 提供错误提示
            print(f"ChromeDriver初始化失败: {str(e)}")
            print(f"请确认ChromeDriver路径是否正确: {chromedriver_path}")
            print(f"当前Chrome版本: 142.0.7444.176")
            # 在这里我们不会抛出异常，而是让程序继续执行，但可能会在后续步骤中失败
        
        # 业务逻辑代码移到except代码块外部
        logger.info(f"正在处理: {company_name} - {web_name}")
        # 检查driver是否成功创建
        if driver is None:
            logger.error("WebDriver初始化失败，跳过当前任务")
            print(f"{company_name} {web_name}: 保存失败 (WebDriver初始化失败)")
            return
        
        # 获取目标网站URL
        if url == "https://www.baidu.com/":
            company_name = company_name + " 处罚"
        
        # 尝试加载页面，带有重试机制
        max_retries = 3
        for retry in range(max_retries):
            try:
                driver.get(url)
                logger.info(f"成功加载页面: {url}")
                break
            except TimeoutException:
                logger.warning(f"页面加载超时，第 {retry+1} 次重试...")
                if retry == max_retries - 1:
                    raise
                time.sleep(2)

        # 使用显式等待查找搜索框
        wait = WebDriverWait(driver, 20)  # 20秒超时
        try:
            if key_word == "name":
                input_box = wait.until(EC.element_to_be_clickable((By.NAME, input_box_name)))
            elif key_word == "id":
                input_box = wait.until(EC.element_to_be_clickable((By.ID, input_box_name)))
            else:
                raise ValueError(f"不支持的key_word类型: {key_word}")
            
            # 清除输入框并输入公司名称
            input_box.clear()
            input_box.send_keys(company_name)
            input_box.send_keys(Keys.ENTER)
            logger.info(f"成功提交搜索: {company_name}")
            
            # 等待搜索结果加载
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # 截图前的准备
            driver.maximize_window()
            # 随机等待一段时间，但使用更合理的范围
            time.sleep(random.uniform(2, 5))

            # 处理多窗口情况
            windows = driver.window_handles
            if len(windows) > 1:
                driver.switch_to.window(windows[-1])
                logger.info("已切换到新窗口")
            
            # 调整窗口大小以适应内容
            width = max(1920, driver.execute_script("return document.documentElement.scrollWidth"))
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width + 20, height + 20)
            
            # 获取当前时间作为时间戳
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_url = driver.current_url
            
            # 添加时间戳和网址到页面底部
            timestamp_html = f"""
            <div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #f0f0f0; 
                    padding: 10px; text-align: center; font-size: 12px; border-top: 1px solid #ccc;">
                <p style="margin: 2px 0;">时间戳: {current_time}</p>
                <p style="margin: 2px 0;">来源网址: {current_url}</p>
            </div>
            """
            
            try:
                # 注入时间戳和网址到页面
                driver.execute_script(f"document.body.insertAdjacentHTML('beforeend', arguments[0]);", timestamp_html)
                time.sleep(1)  # 等待DOM更新
                
                # 使用Chrome的打印功能保存为PDF
                # 确保保存路径存在
                os.makedirs(save_path, exist_ok=True)
                full_save_path = os.path.join(save_path, save_file_name)
                
                # 使用Chrome DevTools Protocol的Page.printToPDF命令
                pdf_options = {
                    'printBackground': True,
                    'landscape': False,
                    'displayHeaderFooter': False,
                    'preferCSSPageSize': True,
                    'paperWidth': 8.27,
                    'paperHeight': 11.69
                }
                
                # 获取PDF数据
                pdf_data = driver.execute_cdp_cmd('Page.printToPDF', pdf_options)
                
                # 将PDF数据保存到文件
                with open(full_save_path, 'wb') as f:
                    import base64
                    f.write(base64.b64decode(pdf_data['data']))
                
                logger.info(f"成功保存PDF到: {full_save_path}")
                print(f"{company_name} {web_name}: 成功保存PDF到 {full_save_path}")
                
            except Exception as e:
                logger.error(f"保存PDF失败: {str(e)}")
                
                # 备用方案：截取完整页面截图
                try:
                    # 计算完整页面高度
                    full_height = driver.execute_script("return document.body.scrollHeight")
                    driver.set_window_size(width, full_height)
                    
                    # 保存截图
                    screenshot_path = os.path.join(save_path, save_file_name.replace('.pdf', '.png'))
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"备用方案: 成功保存截图到: {screenshot_path}")
                    print(f"{company_name} {web_name}: 成功保存截图到 {screenshot_path}")
                except Exception as screenshot_error:
                    logger.error(f"保存截图也失败: {str(screenshot_error)}")
                    raise
            
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"元素查找或操作超时: {str(e)}")
            raise

    except WebDriverException as e:
        logger.error(f"WebDriver错误: {str(e)}")
        print(f"{company_name} {web_name}: 保存失败 (WebDriver错误)")
    except TimeoutException as e:
        logger.error(f"操作超时: {str(e)}")
        print(f"{company_name} {web_name}: 保存失败 (超时)")
    except Exception as e:
        logger.error(f"未知错误: {str(e)}")
        print(f"{company_name} {web_name}: 保存失败 (错误: {str(e)})")
    finally:
        # 确保在任何情况下都关闭浏览器
        if driver is not None:
            try:
                driver.quit()
                logger.info("浏览器已关闭")
            except:
                logger.warning("关闭浏览器时发生错误")