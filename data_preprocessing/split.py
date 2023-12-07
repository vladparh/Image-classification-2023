import argparse
import cv2
from splitter import Splitter
import os

parser = argparse.ArgumentParser()
parser.add_argument("-idi", "--images_dir_input")
parser.add_argument("-ldi", "--labels_dir_input")
parser.add_argument("-ido", "--images_dir_output")
parser.add_argument("-ldo", "--labels_dir_output")
parser.add_argument("-fs", "--frame_size")
args = parser.parse_args()

images_dir_input = args.images_dir_input
labels_dir_input = args.labels_dir_input

images_dir_output = args.images_dir_output
labels_dir_output = args.labels_dir_output
if not os.path.exists(images_dir_output):
    os.makedirs(images_dir_output)
if not os.path.exists(labels_dir_output):
    os.makedirs(labels_dir_output)

split_frame = int(args.frame_size)

images = os.listdir(images_dir_input)
for image in images:
    labels_file = f"{labels_dir_input}/{image.split('.')[0]}.txt"
    image_file = f"{images_dir_input}/{image}"

    splitter = Splitter(
        image_file,
        labels_file,
        split_frame
    )

    res = splitter.crop()

    for key, value in res.items():
        if value["labels"]:
            cv2.imwrite(f"{images_dir_output}/{image.split('.')[0]}_{key}.png", value["image"])
            with open(f"{labels_dir_output}/{image.split('.')[0]}_{key}.txt", "w") as f:
                f.write(value["labels"])

