# coding: utf-8

from PIL import Image, ImageDraw, ImageFilter
import argparse
parser = argparse.ArgumentParser(description='图像高斯对比')
parser.add_argument('--input','-i', type=str, default='demo.jpg', help="输入文件名")
parser.add_argument('--radius','-r', type=int, default=5, help='高斯模糊半径，越大越模糊')
args = parser.parse_args()
# 打开原始图像
img = Image.open(args.input)

# 计算需要截取的区域
w, h = img.size
left = (w - 1280) // 2
top = (h - 720) // 2
right = left + 1280
bottom = top + 720

# 截取图像并调整大小
crop_img = img.crop((left, top, right, bottom))
dst_img = crop_img.resize((1280, 720))

# 对左侧图像进行高斯模糊
left_img = dst_img.crop((0, 0, 640, 720))
blurred_img = left_img.filter(ImageFilter.GaussianBlur(radius=args.radius))
dst_img.paste(blurred_img, (0, 0))

# 在拼接处画一条黑色的线
draw = ImageDraw.Draw(dst_img)
draw.line((640, 0, 640, 720), fill=(0, 0, 0), width=1)

# 保存结果
dst_img.save(f"{args.input}.out.jpg")
