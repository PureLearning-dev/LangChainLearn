# import os
# from PIL import Image, ImageEnhance, ImageOps


# def transform_to_github_style(img_path):
#     # 1. 加载图片
#     img = Image.open(img_path)
#
#     # 2. 转换为灰度图 (黑白)
#     img = img.convert("L")
#
#     # 3. 压低亮度 (这是实现“低背景”的关键)
#     # 0.6 会让背景显著变暗，保留主体轮廓
#     img = ImageEnhance.Brightness(img).enhance(0.65)
#
#     # 4. 极大增强对比度
#     # 让黑白更分明，避免灰蒙蒙的感觉
#     img = ImageEnhance.Contrast(img).enhance(2.2)
#
#     # 5. 自动色阶优化
#     # 剪掉 2% 的极暗/极亮边缘，让画面色彩更干净
#     img = ImageOps.autocontrast(img, cutoff=2)
#
#     # 6. 保存到桌面，方便查看
#     output_name = "github_style_avatar.png"
#     output_path = os.path.expanduser(f"~/Desktop/{output_name}")
#     img.save(output_path, quality=95)
#
#     print(f"✨ 处理成功！")
#     print(f"你的极客黑白头像已存至桌面: {output_path}")
#
#     # 自动打开图片让你检查效果 (Mac 专用命令)
#     os.system(f"open {output_path}")
#
#
# if __name__ == "__main__":
#     target_file = "/Users/purelearning/Downloads/微信图片_20260208221430_4_119.jpg"
#
#     if os.path.exists(target_file):
#         transform_to_github_style(target_file)
#     else:
#         print("没找到文件，请检查路径是否正确。")