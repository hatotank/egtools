import re
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-m","--mode", required=True, choices=['moc','model','png'], help="exec mode moc=moc file, model=model file, png=hd file")
  parser.add_argument("src", help="input file name")
  parser.add_argument("dest", help="output file name")
  parser.add_argument("-p","--python3", action="store_true", help="insert python3 at the beginning of the command")
  args = parser.parse_args()
  
  if args.mode == "moc":
    prog = re.compile('[A-z-]+\.moc')
    pycmd = "eg2_extract_live2d_model_moc.py --moc"
  if args.mode == "model": 
    prog = re.compile('model.json')
    pycmd = "eg2_extract_live2d_model_moc.py"
  if args.mode == "png":
    prog = re.compile('texture.+png')
    pycmd = "eg2_extract_live2d_texture.py"

  if args.python3:
    pycmd = "python3 " + pycmd

  with open(args.dest, "w") as o:
    with open(args.src) as f:
      for line in f:
        result1 = prog.search(line)
        if not result1:
          continue

        result2 = prog.split(line)
        if args.mode == "png":
          if result2[1][-3:].strip() == "sd":
            continue

        o.writelines(pycmd + " " + line.strip() + " " + result2[0] + result1.group() + "\n")

if __name__ == '__main__': main()
