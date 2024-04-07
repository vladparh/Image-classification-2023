#!/bin/bash
mkdir cropped_train_data
mkdir cropped_train_data/images
mkdir cropped_train_data/labels
mkdir cropped_train_data/images/train
mkdir cropped_train_data/labels/train
mkdir cropped_train_data/images/val
mkdir cropped_train_data/labels/val

python3 data_preprocessing/split.py \
-idi train_data/images/train \
-ldi train_data/labels/train \
-ido cropped_train_data/images/train \
-ldo cropped_train_data/labels/train \
-fs 1280

python3 data_preprocessing/split.py \
-idi train_data/images/val \
-ldi train_data/labels/val \
-ido cropped_train_data/images/val \
-ldo cropped_train_data/labels/val \
-fs 1280
