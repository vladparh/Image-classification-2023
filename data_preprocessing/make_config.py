import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-ca", "--coco_annotations_file")
parser.add_argument("-d", "--data_path")
args = parser.parse_args()

with open(args.coco_annotations_file, "r") as f:
    data = json.load(f)


categories = data["categories"]
categories_dict = {}
for category in categories:
    categories_dict[category["id"]] = category["name"]


config_template = f"""path: {args.data_path}
train: images/train
val: images/val

names:
"""

for key, value in categories_dict.items():
    config_template += f"  {key}: {value}\n"

with open("config.yaml", "w") as f:
    f.write(config_template)
