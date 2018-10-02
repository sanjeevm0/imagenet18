from PIL import Image
import os
import argparse
import math

def validate(file, args):
    jpgfile = Image.open(file)
    try:
        print("Name: {0}, Bits: {1}, Size: {2}, Format:{3}".format(file, jpgfile.bits, jpgfile.size, jpgfile.format))
    except Exception as e:
        print("Name: {0} has error".format(file))
        print(e)

def scale_to(x, ratio, newsize):
    return max(math.floor(x*ratio), newsize)

def resize(file, args):
    try:
        basename = file[len(args.dir)+1:]
        im = Image.open(file).convert('RGB')
        r, c = im.size
        ratio = args.newsize/min(r,c)
        sz = (scale_to(r, ratio, args.newsize), scale_to(c, ratio, args.newsize))
        os.makedirs(args.newpath, exist_ok=True)
        im.resize(sz, Image.LINEAR).save(os.path.join(args.newpath, basename))
    except Exception as e:
        print("Encounter error on resize file {0}".format(file))

def save(file, args):
    try:
        basename = file[len(args.dir)+1]
        im = Image.open(file).convert('RGB')
        os.makedirs(args.newpath, exist_ok=True)
        im.save(os.path.join(args.newpath, basename))
    except:
        print("Encounter error on save file {0}".format(file))

def oper(file, args):
    if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
        if args.oper == "validate":
            validate(file, args)
        elif args.oper == "resize":
            resize(file, args)
        elif args.oper == "save":
            save(file, args)
        else:
            print("Invalid operation {0}".format(args.oper))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image directory')
    parser.add_argument('oper', help='the operation to perform <validate|resize|save>')
    parser.add_argument('--dir', '-d', action='store', help='path to dataset')
    parser.add_argument('--size', '-s', action='store', help='the size to resize to')
    parser.add_argument('--newpath', '-n', action='store', help='the new path for saved file')
    args = parser.parse_args()
    if args.dir.endswith('/'):
        args.dir = args.dir[:-1]
    if os.path.isdir(args.dir):
        for root, dirs, files in os.walk(args.dir):
            for name in files:
                oper(os.path.join(root, name), args)
    elif os.path.isfile(args.dir):
        oper(args.dir, args)
