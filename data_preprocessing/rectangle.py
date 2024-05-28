from box_formate import yolo_box_to_cv2
import argparse
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image_file")
parser.add_argument("-l", "--labels_file")
args = parser.parse_args()

image_file = args.image_file
labels_file = args.labels_file

im = cv2.imread(image_file)
(h, w) = im.shape[:2]

with open(labels_file, "r") as f:
    for row in f:
        yolo_box = [float(coord) for coord in row.strip()[1:].strip().split(" ")]
        left, right = yolo_box_to_cv2(yolo_box, w, h)
        cv2.rectangle(im, left, right, (0, 0, 225), 1)

cv2.imwrite(f"../rectangle.png", im)

