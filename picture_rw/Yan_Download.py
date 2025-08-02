from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import requests
from urllib.parse import urljoin
from api_doc_demo import api_doc_demo_main
from loguru  import logger
import os
import shutil
from Gif_Png import convert_static_gif_to_image

def setup_driver(download_dir=None):
    """设置 Chrome 驱动选项"""
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')

    # 添加 User-Agent
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    # 设置下载目录
    if download_dir:
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

    # 初始化 WebDriver
    driver = webdriver.Chrome(
        options=chrome_options
    )

    # 隐藏 WebDriver 特征
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    return driver


def capture_verify_code(driver,url, verify_code_path="/incoc/servlet/verifyCode"):
    """
    捕获验证码 GIF 文件
    :param driver: WebDriver 实例
    :param url: 目标 URL
    :param verify_code_path: 验证码路径
    :return: 验证码文件路径
    """
    # 访问目标页面
    t = time.time()
    driver.get(url)

    # 等待页面加载
    time.sleep(2)

    # 获取完整的验证码 URL
    verify_code_url = urljoin(url, verify_code_path)

    # 获取页面 cookies
    cookies = driver.get_cookies()

    # 创建会话并设置 cookies
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # 设置请求头
    headers = {
        'User-Agent': driver.execute_script("return navigator.userAgent;"),
        'Referer': url
    }

    # 下载验证码文件
    response = session.get(verify_code_url, headers=headers)

    # 保存验证码文件
    if response.status_code == 200:
        # 确保目录存在
        os.makedirs('captchas', exist_ok=True)

        # 生成文件名
        timestamp = int(time.time())
        file_path = os.path.join('captchas', f'verifyCode_{timestamp}.gif')

        # 保存文件
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"验证码已保存到: {file_path}")
        print(time.time() - t)
        return file_path
    else:
        print(f"下载验证码失败，状态码: {response.status_code}")
        return None


def download_verify_code_via_browser(driver, url, verify_code_path="/incoc/servlet/verifyCode"):
    """
    通过浏览器下载验证码文件（使用浏览器内置下载功能）
    :param driver: WebDriver 实例
    :param url: 目标 URL
    :param verify_code_path: 验证码路径
    :return: 验证码文件路径
    """
    # 访问目标页面
    t = time.time()
    driver.get(url)

    # 等待页面加载
    time.sleep(2)

    # 获取完整的验证码 URL
    verify_code_url = urljoin(url, verify_code_path)

    # 使用 JavaScript 触发下载
    driver.execute_script(f"window.location.href = '{verify_code_url}';")

    # 等待下载完成
    time.sleep(2)

    # 查找最新下载的文件
    download_dir = driver.capabilities["chrome"]["userDataDir"] + "/Download"
    files = os.listdir(download_dir)

    # 查找 verifyCode 文件
    verify_files = [f for f in files if f.startswith("verifyCode") and f.endswith(".gif")]

    if verify_files:
        # 按修改时间排序，获取最新的文件
        verify_files.sort(key=lambda x: os.path.getmtime(os.path.join(download_dir, x)), reverse=True)
        latest_file = verify_files[0]

        # 创建保存目录
        os.makedirs('captchas', exist_ok=True)

        # 移动文件到指定目录
        src_path = os.path.join(download_dir, latest_file)
        dest_path = os.path.join('captchas', latest_file)
        shutil.move(src_path, dest_path)

        print(f"验证码已保存到: {dest_path}")
        print(time.time() - t)
        return dest_path
    else:
        print("未找到下载的验证码文件")
        return None


def recognize_captcha(image_path):
    """识别验证码（示例函数，实际需要根据验证码类型实现）"""
    # 这里只是一个示例，实际验证码识别需要专门的库或服务
    print(f"识别验证码: {image_path}")
    api_doc_demo_main(image_path)
    with open(
            # r'd:\software\python\envs\py38\script\download\[OCR]_dzfp_25442000000412019647_李春莲_20250709105155.jsonl',
            image_path,
            'r', encoding='utf-8') as f:
        obj = json.loads(f.read())
    print(obj)
    # 实际应用中，您可能需要使用 OCR 库（如 Tesseract）或第三方 API
    return "1234"  # 返回示例验证码


def Yan_Download_main():
    # 目标 URL
    url = "http://mv.cqccms.com.cn/incoc/GSViewEbike!viewCocEbike.action?vinCode=220922507205752"
    verify_code_path = "/incoc/servlet/verifyCode"

    # 设置下载目录
    download_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_dir, exist_ok=True)

    # 初始化浏览器
    driver = setup_driver(download_dir)

    try:
        # 方法1：直接通过请求下载验证码
        #print("方法1：通过请求下载验证码")
        #captcha_path = capture_verify_code(driver,url, verify_code_path)
        #time.sleep(20)
        #if captcha_path:
        #    logger.info(f"验证码路径：{captcha_path}")
        #else:
        #    logger.error("获取失败")
        # 方法2：通过浏览器下载验证码（备选方法）
        captcha_path = r"D:\software\python\envs\py38\script\pythonProject\picture_rw\captchas\verifyCode_1753599733.gif"
        #captcha_path = download_verify_code_via_browser(driver, url, verify_code_path)
        out_path = convert_static_gif_to_image(captcha_path)
        print(out_path)
        recognize_captcha(out_path)
        time.sleep(20)


        verify_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "engineNo"))
        )
        #verify_input.clear()

        verify_input.send_keys()

        # 定位提交按钮并点击
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "doView"))
        )
        submit_btn.click()
    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        # 保存错误截图
        driver.save_screenshot('error.png')
        print("错误截图已保存到 error.png")
    finally:
        driver.quit()



if __name__ == "__main__":
    logger.info("这里是获取验证码的地方")
    Yan_Download_main()

