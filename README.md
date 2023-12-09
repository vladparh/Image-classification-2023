# Классификация спутниковых изображений 2023
## Описание проекта
В данном проекте производится классификация спутниковых изображений по объектам, изображенным на них.
## Состав команды
1. Блуменау Марк (куратор)
2. Загитов Айнур 
3. Зимницкий Владислав
4. Соборнов Тимофей
5. Пархоменко Владислав

## Описание датасета 
Для выполненении данного проекта было решено использовать [iSAID](https://www.kaggle.com/datasets/usharengaraju/isaid-dataset) датасет -  набор данных для задач сегментации, классификации и обнаружения объектов на фотографиях со спутников. 

Данный датасет содержит 2806 изображений высокого разрешения с 471760 размеченными объектами, относящимся к 15 различным классам: малый и крупный автотранспорт, самолеты, вертолеты, корабли и прочие. Более подробное распределение классов в датасете можно увидеть в таблице ниже. 

| Название класса | Количество изображений | Количество объектов класса на изображении |
|----------|----------|----------|
| small_vehicle    | 1156  | 253077   |
| large_vehicle    |  841   | 39874  |
| tennis_court    | 537  | 11632   |
| ground_track_field    | 536  | 84456   |
| ship    | 480   | 35755  |
| harbor    | 418   | 6492  |
| storage_tank    | 395   | 18549   |
| swimming_pool    | 334   | 2605   |
| plane    | 292  | 8781  |
| bridge    | 289   | 2272  |
| roundabout    | 254   | 3053  |
| baseball_diamond    | 223   | 1207   |
| soccer_ball_field    | 199   | 529   |
| basketball_court    | 191   | 762   |
| helicopter    | 149   | 2716   |

Подробнее ознакомиться с исследование авторов датасета можно на [arxiv](https://arxiv.org/abs/1905.12886)

Ссылка на [датасет](https://captain-whu.github.io/iSAID/dataset.html) от авторов

## Препроцессинг датасета

### Конвертация СOCO в Yolo

```
python3 data_preprocessing/make_yolo_labels.py \
-ca /path_to_coco.json \
-ld /path_to_yolo_labels_dir \
-id /path_to_images_dir
```

### Разбивка изображений на более мелкие
```
python3 data_preprocessing/split.py \
-idi /path_to_images_dir \
-ldi /path_to_labels_dir \
-ido /path_to_output_images_dir \
-ldo /path_to_output_labels_dir \
-fs /split_frame_size
```

#### Скрипты работают на python3.10

## Датасет для обучения

Key ID и ключ в закрепе беседы

```
aws configure
```
```
aws --endpoint-url="https://storage.yandexcloud.net" \
s3 cp --recursive s3://isaiddata/train_data train_data
```