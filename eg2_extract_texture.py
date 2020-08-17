# eg2_extract_texture.py

# $pip install unitypack
# $python eg2_extract_texture.py [-i] xxx.unity3d xxx.png

import argparse
import unitypack
from PIL import ImageOps, ImageChops

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("src")
  parser.add_argument("dest")
  parser.add_argument("-i","--invert",help="image invert",action="store_true")
  args = parser.parse_args()

  with open(args.src,"rb") as f:
    bundle = unitypack.load(f)

    for asset in bundle.assets:
      for id,object in asset.objects.items():
        if object.type == "Texture2D":
          data = object.read()
          img = data.image
          img = ImageOps.flip(img)       # 上下反転
          if args.invert:
            img = ImageChops.invert(img) # ネガポジ反転(基本未使用)

          img.save(args.dest)            # PNGのみ

if __name__ == '__main__': main()
