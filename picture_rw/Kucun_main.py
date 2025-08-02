from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import erweima
import ShuJuTiQu
from  ..mysql.Che_insert  import *
from loguru import logger
import time
import Yan_Download
def main(url):
    """
    获取 二维码的连接
    获取对应html
    解析html 得出数据字典进行数据 插入
    Main function
    :param url:
    :return:
    """
    # 初始化验证码处理器
    # 配置浏览器选项
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # 初始化浏览器
    wd = webdriver.Chrome(options=options)
    wd.get(url)
    try:
        logger.info("自动尝试失败，转为手动模式")
        # 等待结果
        WebDriverWait(wd, 30).until(
            lambda
            #此处传入的网页连接
                driver: driver.current_url != url
        )

        time.sleep(5)
        logger.info("手动输入验证码提交成功！")
    # 获取页面内容
        page_content = wd.page_source
        with open('result.html', 'w', encoding='utf-8') as f:
            f.write(page_content)
        logger.info("页面内容已保存到 result.html")

    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        # 保存错误截图
        wd.save_screenshot('error.png')
        logger.info("错误截图已保存到 error.png")
    finally:
        time.sleep(5)
        wd.quit()
if __name__ == "__main__":
    """
    二维码录取主程序运行处
    """
    #获取 二维码的连接
    url = erweima.return_result()
    # 获取对应html
    main(url)
    #解析html 得出数据字典
    a = ShuJuTiQu.ShuJutiTiQu_main()
    logger.info(f"转化的字典数据为:{a}")
    #进行数据 插入
    Che_insert_main(a)