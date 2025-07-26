import webbrowser
from pyzbar import pyzbar
from PIL import Image
import cv2
import requests
import os
import time


class QRCodeProcessor:
    """
    二维码处理器，支持从图像文件、摄像头扫描二维码，并处理其中的URL
    """

    def __init__(self, open_browser=True, log_file="qr_log.txt"):
        """
        初始化二维码处理器
        :param open_browser: 是否自动打开浏览器
        :param log_file: 日志文件路径2
        """
        self.open_browser = open_browser
        self.log_file = log_file
        self._init_log()

    def _init_log(self):
        """初始化日志文件"""
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("QR Code Processing Log\n")
                f.write("=" * 40 + "\n")

    def _log(self, message):
        """记录日志"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry, end="")
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def _open_url(self, url):
        """打开URL"""
        try:
            # 验证URL是否有效
            if not url.startswith(("http://", "https://")):
                url = "http://" + url

            self._log(f"尝试打开URL: {url}")

            if self.open_browser:
                webbrowser.open(url)
                self._log("已打开浏览器访问该URL")

            return url
        except Exception as e:
            self._log(f"打开URL时出错: {str(e)}")
            return None

    def process_qr_from_image(self, image_path):
        """
        从图像文件处理二维码
        :param image_path: 图像文件路径
        :return: 二维码内容或None
        """
        try:
            self._log(f"处理图像文件: {image_path}")

            # 使用PIL打开图像
            img = Image.open(image_path)

            # 解码二维码
            decoded_objects = pyzbar.decode(img)

            if not decoded_objects:
                self._log("未在图像中发现二维码")
                return None

            # 获取第一个二维码的内容
            qr_data = decoded_objects[0].data.decode("utf-8")
            self._log(f"解码成功: {qr_data}")

            return qr_data
        except Exception as e:
            self._log(f"处理图像时出错: {str(e)}")
            return None

    def process_qr_from_camera(self, timeout=30):
        """
        从摄像头扫描二维码
        :param timeout: 超时时间（秒）
        :return: 二维码内容或None
        """
        self._log(f"启动摄像头扫描，超时时间: {timeout}秒")

        # 初始化摄像头
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self._log("无法打开摄像头")
            return None

        start_time = time.time()
        qr_data = None

        try:
            while time.time() - start_time < timeout:
                # 读取摄像头帧
                ret, frame = cap.read()
                if not ret:
                    self._log("无法从摄像头获取帧")
                    continue

                # 转换为灰度图像（提高识别效率）
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 解码二维码
                decoded_objects = pyzbar.decode(gray)

                # 显示摄像头画面
                cv2.imshow('QR Code Scanner', frame)

                # 检测到二维码
                if decoded_objects:
                    qr_data = decoded_objects[0].data.decode("utf-8")
                    self._log(f"解码成功: {qr_data}")
                    break

                # 检查退出键
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self._log("用户手动退出扫描")
                    break
        finally:
            # 释放资源
            cap.release()
            cv2.destroyAllWindows()
        return qr_data

    def process_qr_from_url(self, image_url):
        """
        从网络图片URL处理二维码
        :param image_url: 图片URL
        :return: 二维码内容或None
        """
        try:
            self._log(f"处理网络图片: {image_url}")

            # 下载图片
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            # 保存临时文件
            temp_file = "temp_qr_image.jpg"
            with open(temp_file, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            # 处理图片
            result = self.process_qr_from_image(temp_file)

            # 删除临时文件
            os.remove(temp_file)

            return result
        except Exception as e:
            self._log(f"处理网络图片时出错: {str(e)}")
            return None

def return_result():
    processor = QRCodeProcessor(open_browser=True)

    # 使用场景选择
    print("请选择二维码处理方式:")
    print("1. 从图像文件处理")
    print("2. 从摄像头扫描")
    print("3. 从网络图片处理")

    choice = input("请输入选项 (1/2/3): ")

    if choice == "1":
        # 从图像文件处理
        image_path = input("请输入图像文件路径: ").strip()
        result = processor.process_qr_from_image(image_path)
    elif choice == "2":
        # 从摄像头扫描
        result = processor.process_qr_from_camera()
    elif choice == "3":
        # 从网络图片处理
        image_url = input("请输入图片URL: ").strip()
        result = processor.process_qr_from_url(image_url)
    else:
        print("无效选项")
        result = None

    # 输出结果
    if result:
        print(f"\n成功处理二维码: {result}")
    else:
        print("\n未能处理二维码")

    # 显示日志文件路径
    print(f"\n详细日志已保存至: {os.path.abspath(processor.log_file)}")
    print(result)
    print(type(result))
    return result

# 使用示例
if __name__ == "__main__":
    # 创建二维码处理器
    processor = QRCodeProcessor(open_browser=True)
    # 使用场景选择
    print("请选择二维码处理方式:")
    print("1. 从图像文件处理")
    print("2. 从摄像头扫描")
    print("3. 从网络图片处理")

    choice = input("请输入选项 (1/2/3): ")

    if choice == "1":
        # 从图像文件处理
        image_path = input("请输入图像文件路径: ").strip()
        result = processor.process_qr_from_image(image_path)
    elif choice == "2":
        # 从摄像头扫描
        result = processor.process_qr_from_camera()
    elif choice == "3":
        # 从网络图片处理
        image_url = input("请输入图片URL: ").strip()
        result = processor.process_qr_from_url(image_url)
    else:
        print("无效选项")
        result = None

    # 输出结果
    if result:
        print(f"\n成功处理二维码: {result}")
    else:
        print("\n未能处理二维码")
    print(result)
    print(type(result))
    # 显示日志文件路径
    print(f"\n详细日志已保存至: {os.path.abspath(processor.log_file)}")