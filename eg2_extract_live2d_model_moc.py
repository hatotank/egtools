# eg2_extract_live2d_model_moc.py

# $python eg2_extract_live2d_model_moc.py [--moc] xxx.asset.unity3d xxx

import argparse
import unitypack

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("src")
  parser.add_argument("dest")
  parser.add_argument("--moc",help="image invert",action="store_true")
  args = parser.parse_args()

  with open(args.src,"rb") as f:
    bundle = unitypack.load(f)

    for asset in bundle.assets:
      for id,object in asset.objects.items():

        #print(object.type)
        if object.type == "TextAsset":
          data = object.read()
          #print("Asset name:", data.name)
          #print("Contents:", repr(data.script))
          if args.moc:
            with open(args.dest,"wb") as o:
              o.write(data.script)
          else:
            with open(args.dest,"wt",encoding="utf-8") as o:
              o.write(data.script)

if __name__ == '__main__': main()
