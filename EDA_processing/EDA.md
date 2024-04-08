# Разведочный анализ данных
## Общий анализ изображений
Проведём общий анализ изображений. Всего в тренировочной выборке находится 1411 спутниковых снимков. Посмотрим сколько категорий объектов может встречаться на каждом изображении:

![Количество категорий на снимках](eda_images/plots/cat_on_imgs.png)

На гистаграмме видно, что на снимках встречаются от 1 до 10 категорий объектов. Также посмотрим на разрешение спутниковых снимков:

![Разрешение спутниковых снимков](eda_images/plots/imges_res.png)

Тренировочная выборка представлена спутниковыми снимками в разном разрешении, с разным соотношением сторон и разной ориентацией.

## Анализ изображений по категориям
Рассмотрим теперь каждую категорию в отдельности. Маски объектов каждой категории: https://disk.yandex.ru/d/VG-VBLbyK7aOPQ

### Категория 'storage_tank'
С данной категорией есть 245 спутниковых снимков. Рассмотрим расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/storage_tank_1.png)

На первом графике точками отмечены центры объектов, координаты берутся относительно ширины и высоты изображений. Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/storage_tank_2.png)

### Категория 'Large_Vehicle'
С данной категорией есть 770 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/large_vehicle_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/large_vehicle_2.png)

### Категория 'Small_Vehicle'
С данной категорией есть 1099 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/small_vehicle_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/small_vehicle_2.png)

### Категория 'plane'
С данной категорией есть 198 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/plane_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/plane_2.png)

### Категория 'ship'
С данной категорией есть 434 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/ship_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/ship_2.png)

### Категория 'Swimming_pool'
С данной категорией есть 259 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/swimming_pool_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/swimming_pool_2.png)

### Категория 'Harbor'
С данной категорией есть 339 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/harbor_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/harbor_2.png)

### Категория 'tennis_court'
С данной категорией есть 310 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/tennis_court_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/tennis_court_2.png)

### Категория 'Ground_Track_Field'
С данной категорией есть 197 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/ground_track_field_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/ground_track_field_2.png)

### Категория 'Soccer_ball_field'
С данной категорией есть 184 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/soccer_ball_field_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/soccer_ball_field_2.png)

### Категория 'baseball_diamond'
С данной категорией есть 146 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/baseball_diamond_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/baseball_diamond_2.png)

### Категория 'Bridge'
С данной категорией есть 225 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/bridge_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/bridge_2.png)

### Категория 'basketball_court'
С данной категорией есть 119 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/basketball_court_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/basketball_court_2.png)

### Категория 'Roundabout'
С данной категорией есть 182 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/roundabout_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/roundabout_2.png)

### Категория 'Helicopter'
С данной категорией есть 38 спутниковых снимков. Расположение обектов и их количество на снимках:

![Расположение объектов и их кол-во на снимках](eda_images/plots/helicopter_1.png)

Размер изображений с объектами данного класса:

![Размеры изображений](eda_images/plots/helicopter_2.png)

## Тепловая карты распределления отдельных категорий на изображений

![Общая тепловая карта](eda_images/heatmaps/Total_heat_map.png)
Выполнена нормализация координат объектов с приведением к относительным значениям.

Посмотреть детальнее на каждую тепловую карту можно в [папке](eda_images/heatmaps). 


## Выводы
В датасете ISAID все категории объектов представлены большим количеством разноплановых изображений. Снимки имеют широкий спектор размеров, объекты на них имеют разную ориентацию, расположение объектов на снимках также совершенно разное. Всё это говорит о качественной подготовке данного датасета.