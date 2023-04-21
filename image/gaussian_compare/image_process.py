# coding: utf-8

from PIL import Image, ImageDraw, ImageFilter
import argparse
parser = argparse.ArgumentParser(description='图像高斯对比')
parser.add_argument('--input','-i', type=str, default='demo.jpg', help="输入文件名")
parser.add_argument('--radius','-r', type=int, default=5, help='高斯模糊半径，越大越模糊')
args = parser.parse_args()


from PIL import Image

def resize_image(image_path, dst_w=1280, dst_h=720):
    with Image.open(image_path) as image:
        # 获取原始图像的尺寸
        width, height = image.size

        # 如果图像已经符合尺寸要求，则直接返回
        if width == dst_w and height == dst_h:
            return image

        # 计算等比例缩放后的尺寸
        scale = max(dst_w/width, dst_h/height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        # 进行缩放
        resized_image = image.resize((new_width, new_height))

        # 裁剪缩放后的图像，使其恰好符合尺寸要求
        left = (new_width - dst_w) / 2
        top = (new_height - dst_h) / 2
        right = left + dst_w
        bottom = top + dst_h
        cropped_image = resized_image.crop((left, top, right, bottom))

        # 返回缩放并裁剪后的图像
        return cropped_image


# 打开原始图像
img = resize_image(args.input) # bImage.open(args.input)

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
