# eg2_extract_text.py

# $python eg2_extract_text.py xxx.json xxx.txt

import argparse
import json
import os

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("src")
  parser.add_argument("dest")

  args = parser.parse_args()

  with open(args.src,"r",encoding="utf-8") as f:
    json_dict = json.load(f)

    filename = os.path.splitext(os.path.basename(args.src))[0]
    with open(args.dest,"wt",encoding="utf-8") as o:

      for obj in json_dict:
        line = ""

        if "speaker" in obj:
          line = line + '"' + obj['speaker'] + '"'

        if "text" in obj:
          line = line + '\t"' + obj['text'] + '"'
      
        if len(line) > 0:
          o.write(line + "\n")

if __name__ == '__main__': main()
