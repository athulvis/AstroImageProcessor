import rawpy
from PIL import Image
import argparse
from pathlib import Path
import numpy as np
import datetime

today = datetime.date.today()

parser = argparse.ArgumentParser()
arg1 = parser.add_argument("-f", "--files", type=list, nargs='+',
                            help="File names")
arg2 = parser.add_argument("-d", "--directory", type=str,
                            help="Directory name")
arg3 = parser.add_argument("-s", "--save", help="Saving file format")
args = parser.parse_args()

if args.directory is not None:
    path = Path(args.directory)
    if path.exists():
        imgs = [i for i in path.glob("**/*") if i.suffix in ['.CR2', '.NEF']]
    else:
        print("Path not found")


if args.files is not None:
    if len(args.files) > 1:
        imgs = args.files
    else:
        raise argparse.ArgumentError(arg1, "Number of files should be greater\
                                    than 1")


def convert_img(filenames):
    rgb_list = []
    for k in filenames:
        img = rawpy.imread(str(k))
        rgb = img.postprocess()
        rgb_list.append(rgb)
        # Image.fromarray(rgb).save(f'{k}.jpg', quality=90,
        # optimize=True)
    return np.array(rgb_list)


def save_img(rgb):
    if args.save == 'JPG':
        Image.fromarray(rgb).save(f'image_{today}.jpg', quality=90,
                                  optimize=True)
        print("Image saved in JPG format")
    elif args.save == 'TIFF':
        Image.fromarray(rgb).save(f'image_{today}.tiff')
        print("Image saved in TIFF format")


def stack_img(rgb_array):
    return np.median(rgb_array, axis=0).astype('uint8')


if __name__ == '__main__':
    clr_Array = convert_img(imgs)
    rgb = stack_img(clr_Array)
    save_img(rgb)
