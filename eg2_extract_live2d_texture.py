# eg2_extract_live2d_texture.py

# $pip install unitypack
# $python eg2_extract_live2d_texture.py xxx.unity3d xxx.png

import argparse
import unitypack
from PIL import ImageOps, Image

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("src")
  parser.add_argument("dest")
  args = parser.parse_args()

  with open(args.src,"rb") as f:
    bundle = unitypack.load(f)

    for asset in bundle.assets:
      for id,object in asset.objects.items():
        if object.type == "Texture2D":
          data = object.read()
          # Format 
          # https://subdiox.github.io/deresute/resource/unity3d-texture2d.html
          # 13 RGBA4444 -> RGBA8888
          size = (data.width,data.height)
          img = Image.frombytes('RGBA', size, data.image_data, 'raw', 'RGBA;4B', 0, -1)
          img = Image.merge('RGBA', img.split()[::-1])

          img.save(args.dest) # PNGのみ

if __name__ == '__main__': main()
