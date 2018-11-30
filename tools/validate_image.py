from PIL import Image
import os
import argparse
import math

def validate(file, args):
    try:
        jpgfile = Image.open(file)
        print("Name: {0}, Bits: {1}, Size: {2}, Format:{3}".format(file, jpgfile.bits, jpgfile.size, jpgfile.format))
    except BaseException as e:
        print("Name: {0} has error".format(file))
        print(e)

def scale_to(x, ratio, newsize):
    return max(math.floor(x*ratio), newsize)

def create_dir(file, args):
    if file == args.dir:
        outname = args.newpath
    else:           
        basename = file[len(args.dir)+1:]
        outname = os.path.join(args.newpath, basename)
    #print("F: {0}, D: {1}, O: {2}".format(file, args.dir, outname))
    dirname = os.path.dirname(outname)
    if dirname != "":
        os.makedirs(dirname, exist_ok=True)
    #print("D made")
    return outname

def resize(file, args):
    try:
        im = Image.open(file).convert('RGB')
        outname = create_dir(file, args)
        r, c = im.size
        ratio = args.newsize/min(r,c)
        sz = (scale_to(r, ratio, args.newsize), scale_to(c, ratio, args.newsize))
        im.resize(sz, Image.LINEAR).save(outname)
    except Exception as e:
        print("Encounter error on resize file {0}, exception {1}".format(file, e))

def save(file, args):
    try:
        im = Image.open(file).convert('RGB')
        outname = create_dir(file, args)
        im.save(outname)
    except Exception as e:
        print("Encounter error on save file {0}, exception {1}".format(file, e))

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
    parser.add_argument('--newsize', '-s', action='store', help='the size to resize to')
    parser.add_argument('--newpath', '-n', action='store', help='the new path for saved file')
    args = parser.parse_args()
    if args.newsize is not None:
        args.newsize = int(args.newsize)
    if args.dir.endswith('/'):
        args.dir = args.dir[:-1]
    if os.path.isdir(args.dir):
        for root, dirs, files in os.walk(args.dir):
            for name in files:
                oper(os.path.join(root, name), args)
    elif os.path.isfile(args.dir):
        oper(args.dir, args)
