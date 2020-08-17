# eg2_unpack_story.py

# $pip install unitypack
# $python eg2_unpack_story.py xxx.asset.unity3d xxx.json

import argparse
import unitypack

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("src")
  parser.add_argument("dest")

  args = parser.parse_args()

  with open(args.src,"rb") as f:
    bundle = unitypack.load(f)

    for asset in bundle.assets:
      for id,object in asset.objects.items():

        if object.type == "StoryScript":
          scenario = object.read()
          with open(args.dest,"wt",encoding="utf-8") as o:
            o.write(scenario['script'])

if __name__ == '__main__': main()
