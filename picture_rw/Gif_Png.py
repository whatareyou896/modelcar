from PIL import Image
from loguru  import logger
import os
def convert_static_gif_to_image(gif_path, output_path=None, output_format='PNG', delete_original=False):
    """
    将静态 GIF 图片转换为其他图片格式
    :param gif_path: 输入 GIF 文件路径
    :param output_path: 输出文件路径（可选）
    :param output_format: 输出格式（如 PNG, JPEG）
    :param delete_original: 是否删除原始 GIF 文件
    :return: 转换后的文件路径
    """
    # 设置日志

    try:
        # 检查文件是否存在
        if not os.path.exists(gif_path):
            raise FileNotFoundError(f"文件不存在: {gif_path}")

        # 检查文件是否为 GIF
        if not gif_path.lower().endswith('.gif'):
            raise ValueError("输入文件必须是 GIF 格式")

        # 打开 GIF 文件
        with Image.open(gif_path) as img:
            # 检查是否为静态 GIF（只有一帧）
            try:
                # 尝试读取第二帧
                img.seek(1)
                # 如果成功读取第二帧，说明不是静态 GIF
                logger.warning(f"警告: GIF 文件包含多帧 ({gif_path})，但将被视为静态图片处理")
                img.seek(0)  # 回到第一帧
            except EOFError:
                # 只有一帧
                logger.info(f"检测到静态 GIF: {gif_path}")

            # 获取图像信息
            width, height = img.size
            mode = img.mode
            logger.info(f"图像信息: {width}x{height} 像素, 模式: {mode}")

            # 确定输出路径
            if output_path is None:
                # 如果没有提供输出路径，创建基于输入文件名的路径
                base_name = os.path.splitext(os.path.basename(gif_path))[0]
                output_dir = os.path.dirname(gif_path)
                output_path = os.path.join(output_dir, f"{base_name}.{output_format.lower()}")

            # 转换并保存图像
            if output_format.upper() == 'JPEG' and img.mode in ['RGBA', 'LA', 'P']:
                # 对于 JPEG 格式，需要移除透明度
                if img.mode == 'RGBA':
                    # 创建一个白色背景
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    # 将 GIF 粘贴到背景上
                    background.paste(img, mask=img.split()[3])  # 使用 alpha 通道作为掩码
                    img = background
                elif img.mode == 'P' and 'transparency' in img.info:
                    # 处理调色板模式的透明度
                    img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    # 转换为 RGB
                    img = img.convert('RGB')
            # 保存图像
            img.save(output_path, output_format)
            logger.info(f"已将 GIF 转换为 {output_format}: {output_path}")
            # 如果需要，删除原始文件
            if delete_original:
                os.remove(gif_path)
                logger.info(f"已删除原始文件: {gif_path}")
            return output_path

    except Exception as e:
        logger.error(f"转换失败: {str(e)}")
        return None