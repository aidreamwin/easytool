# coding: utf-8

from PIL import Image, ImageDraw, ImageFilter
import argparse

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

def process(args, dst_w=1280, dst_h=720):
    # 打开原始图像
    dst_img = resize_image(args.input, dst_w, dst_h) # bImage.open(args.input)
    # 对左侧图像进行高斯模糊
    left_img = dst_img.crop((0, 0, int(dst_w/2), dst_h))
    blurred_img = left_img.filter(ImageFilter.GaussianBlur(radius=args.radius))
    dst_img.paste(blurred_img, (0, 0))

    # 在拼接处画一条黑色的线
    draw = ImageDraw.Draw(dst_img)
    draw.line((int(dst_w/2), 0, int(dst_w/2), dst_h), fill=(0, 0, 0), width=1)

    # 保存结果
    save_file = f"{args.input}.out.jpg"
    dst_img.save(save_file)
    return save_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='图像高斯对比')
    parser.add_argument('--input','-i', type=str, default='demo.jpg', help="输入文件名")
    parser.add_argument('--radius','-r', type=int, default=5, help='高斯模糊半径，越大越模糊')
    args = parser.parse_args()
    process(args)