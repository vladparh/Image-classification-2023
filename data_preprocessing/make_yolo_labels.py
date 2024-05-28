import argparse
import json
import os
import re
import magic

parser = argparse.ArgumentParser()
parser.add_argument("-ca", "--coco_annotations_file")
parser.add_argument("-ld", "--labels_dir")
parser.add_argument("-id", "--images_dir")

args = parser.parse_args()

if not os.path.exists(args.labels_dir):
    os.makedirs(args.labels_dir)


with open(args.coco_annotations_file, "r") as f:
    data = json.load(f)


images = data["images"]
images_dict = {}
for image in images:
    images_dict[image["id"]] = image["file_name"]

annotations = data["annotations"]
for annotation in annotations:
    bbox = annotation["bbox"]
    image_id = annotation["image_id"]
    image_name = images_dict[image_id]
    category_id = annotation["category_id"]

    im = magic.from_file(f"{args.images_dir}/{image_name}")
    w, h = re.search('(\d+) x (\d+)', im).groups()
    w = int(w)
    h = int(h)
    yolo_box = [bbox[0]+bbox[2]/2, bbox[1]+bbox[3]/2, bbox[2], bbox[3]]
    yolo_box = [yolo_box[0]/w, yolo_box[1]/h, yolo_box[2]/w, yolo_box[3]/h]
    yolo_box = [str(round(elem, 6)) for elem in yolo_box]
    yolo_box = [elem+"0"*(8-len(elem)) for elem in yolo_box]
    res_annotation = f"{category_id} {' '.join(yolo_box)}\n"

    with open(f"{args.labels_dir}/{image_name.split('.')[0]}.txt", "a") as f:
        f.write(f"{res_annotation}")

