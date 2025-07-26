
from selenium import webdriver
from selenium.webdriver.common.by import By
'''
wd = webdriver.Chrome() # 指定 Chrome 浏览器，会自动下载驱动

#用例网站
wd.get('http://mv.cqccms.com.cn/incoc/GSViewEbike!viewCocEbike.action?vinCode=220922507205752')
#需要补全的代码：要求能够通过OCR 识别对应文件的四位验证码数字
#网页上对应的图片元素为 <img alt="" src="/incoc/servlet/verifyCode">


#这是验证码输入文本框
element = wd.find_element(By.ID, "engineNo")
yanzhengma = "4568"
element.send_keys(yanzhengma)
#这是验证码提交框
#element = wd.find_element(By.NAME, "doView")
#element.click()
#wd.get_screenshot_as_file(By.CLASS_NAME, "biaotifontblue")
input('按回车退出')'''
