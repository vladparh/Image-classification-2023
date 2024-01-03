import json
import numpy as np
from PIL import Image
from tqdm import tqdm
import pandas as pd

mode = 'train' #'val'/'train'
annotations_path =f'../Isaid_dataset/{mode}/iSAID_{mode}.json'
img_path_input = f'../Isaid_dataset/{mode}/images/'
label_output_path = f'../isaid_yolov5/{mode}/labels/'
img_output_path = f'../isaid_yolov5/{mode}/images/'
csv_path_output = f'../isaid_yolov5/{mode}/{mode}.csv'
frame_size = 600 #минимальный размер изображений на выходе
min_area = 12 #минимальная площадь объекта (в пикс.)

def mini_labels(labels, box, min_area=12):
    '''Создает bbox для объектов, находящихся внутри части изображения, ограниченного рамками box'''
    new_boxs=[]
    for item in labels:
        cat_name, label = item[0], item[1]
        if not (
            (box[2]<label['bbox'][0]) or
            (label['bbox'][2]<box[0]) or
            (box[3]<label['bbox'][1]) or
            (label['bbox'][3]<box[1])
           ):
            seg = []
            for it in label['seg']:
                seg += it
            seg = np.array(seg)
            new_seg = np.zeros(seg.shape)
            x_seg = seg[::2]
            y_seg = seg[1::2]
            x_seg[x_seg < box[0]] = box[0]
            x_seg[x_seg > box[2]] = box[2]
            y_seg[y_seg < box[1]] = box[1]
            y_seg[y_seg > box[3]] = box[3]
            new_seg[::2] = x_seg
            new_seg[1::2] = y_seg
            if (np.max(new_seg[::2])-np.min(new_seg[::2]))*(np.max(new_seg[1::2])-np.min(new_seg[1::2])) > min_area:
                new_boxs.append([cat_name, [np.min(new_seg[::2]) - box[0],
                                          np.min(new_seg[1::2]) - box[1],
                                          np.max(new_seg[::2]) - box[0],
                                          np.max(new_seg[1::2]) - box[1]]])
    return new_boxs

with open(annotations_path, 'r', encoding='Utf-8') as json_data:
    annotations = json.load(json_data)

name2id={'storage_tank': 0,
 'Large_Vehicle': 1,
 'Small_Vehicle': 2,
 'plane': 3,
 'ship': 4,
 'Swimming_pool': 5,
 'Harbor': 6,
 'tennis_court': 7,
 'Ground_Track_Field': 8,
 'Soccer_ball_field': 9,
 'baseball_diamond': 10,
 'Bridge': 11,
 'basketball_court': 12,
 'Roundabout': 13,
 'Helicopter': 14}

img_ann = {}
for img in annotations['images']:
    img_ann[img['id']] = []
for obj in annotations['annotations']:
    img_ann[obj['image_id']].append([obj['category_name'], {'bbox': [obj['bbox'][0],obj['bbox'][1],obj['bbox'][0]+obj['bbox'][2]-1,obj['bbox'][1]+obj['bbox'][3]-1], 'seg': obj['segmentation']}])

df = pd.DataFrame(columns=['img','label'])
for img in tqdm(annotations['images']):
    im = Image.open(img_path_input+img['file_name'])
    im = im.convert('RGB')
    img_name = img['file_name'][:5]
    width, height = im.size
    m=width//frame_size
    n=height//frame_size
    if n==0:
        n=1
    if m==0:
        m=1
    mini_width = width // m
    mini_height = height // n
    for i in range(n):
        for j in range(m):
            if (i==n-1) and (j==m-1):
                box = (j*mini_width, i*mini_height, width, height)
            elif i==n-1:
                box = (j*mini_width, i*mini_height, j*mini_width + mini_width, height)
            elif j==m-1:
                box = (j*mini_width, i*mini_height, width, i*mini_height + mini_height)
            elif (i < n-1) and (j < m-1):
                box = (j*mini_width, i*mini_height, j*mini_width + mini_width, i*mini_height + mini_height)
            labels = mini_labels(img_ann[img['id']], box, min_area)
            if len(labels)!=0:
                for label in labels:
                    cat_name, bbox = label[0], label[1]
                    if ((((bbox[0]+bbox[2])/2.0)/mini_width >= 1.0) or
                        (((bbox[1]+bbox[3])/2.0)/mini_height >= 1.0)):
                        continue
                    obj_width = (bbox[2]-bbox[0])/mini_width
                    obj_height = (bbox[3]-bbox[1])/mini_height
                    if obj_width >= 1.0:
                        obj_width = 1.0 - 1e-6
                    if obj_height >= 1.0:
                        obj_height = 1.0 - 1e-6
                    line = ' '.join([
                                   str(name2id[cat_name]),
                                   str(((bbox[0]+bbox[2])/2.0)/mini_width),
                                   str(((bbox[1]+bbox[3])/2.0)/mini_height),
                                   str(obj_width),
                                   str(obj_height)
                                  ])
                    with open(label_output_path + f'{img_name}_{i}_{j}.txt','a') as file:
                        file.write(line + '\n')
                im.crop(box).save(img_output_path + f'{img_name}_{i}_{j}.jpg')
                df.loc[len(df.index )] = [f'{img_name}_{i}_{j}.jpg', f'{img_name}_{i}_{j}.txt']
df.to_csv(csv_path_output, index=False)
