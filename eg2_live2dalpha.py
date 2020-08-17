import argparse
from PIL import Image, ImageChops, ImageOps, ImageFilter, ImageDraw

# 別の手順のため未使用
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("src1")
    parser.add_argument("src2")
    parser.add_argument("dest")
    parser.add_argument("-t", "--threshold", help="Threshold", default='200')
    parser.add_argument("-g", "--gaussianblur", help="GaussianBlur", default='1')
    args = parser.parse_args()

    print("src1:", args.src1)
    print("src2:", args.src2)
    print("dest:", args.dest)
    print("-t:", args.threshold)
    print("-g:", args.gaussianblur)

    offset = 20

    src1 = Image.open(args.src1)
    src2 = Image.open(args.src2)

    # マスク画像作成
    # 差の絶対値
    img_mask = ImageChops.difference(src1, src2)
    # 反転＋グレースケール化
    img_mask = ImageOps.invert(img_mask).convert('L')
    # 引数の閾値に従い指定未満は0
    img_mask = img_mask.point(lambda x: 0 if x < int(args.threshold) else x)
    # 境界にガウシアンぼかし
    img_mask = img_mask.filter(ImageFilter.GaussianBlur(int(args.gaussianblur)))
    # 縁を塗りつぶす
    draw = ImageDraw.Draw(img_mask)
    # top
    draw.rectangle((0,0, img_mask.width,offset+32), fill=(0))
    # right
    draw.rectangle((img_mask.width-offset,0, img_mask.width, img_mask.height), fill=(0))
    # bottom
    draw.rectangle((0,img_mask.height-offset, img_mask.width, img_mask.height), fill=(0))
    # left
    draw.rectangle((0,0, offset,img_mask.height), fill=(0))

    src1.putalpha(img_mask)
    img_out = src1.crop((1, 32, 601, 632))
    crop = img_out.split()[-1].getbbox()
    img_out = img_out.crop(crop)
    img_out.save(args.dest)

if __name__ == '__main__': main()
