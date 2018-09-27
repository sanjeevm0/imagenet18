from PIL import Image
import os
import argparse

def validate(file):
    if file.lower().endswith(".jpeg") or file.lower().endswith(".jpg"):
        jpgfile = Image.open(file)
        print("Name: {0}, Bits: {1}, Size: {2}, Format:{3}".format(file, jpgfile.bits, jpgfile.size, jpgfile.format))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image directory')
    parser.add_argument('dir', metavar='DIR', help='path to dataset')
    args = parser.parse_args()
    for root, dirs, files in os.walk(args.dir):
        for name in files:
            validate(os.path.join(root, name))
