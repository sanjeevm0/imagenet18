import sys
import subprocess

if __name__ == '__main__':
    args = ["python", "validate_image.py"]+sys.argv[1:]
    print("Args:{0}".format(args))
    subprocess.call(args, stderr=sys.stdout.fileno())
