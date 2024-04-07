# Данный файл представляет собой инструкцию по использованию docker-контейнера с работающим веб-сервисом.

## Запуск Docker-контейнера

Ссылка на Docker-образ:
```
https://hub.docker.com/r/forch2002/detection-service-image
```

После скачивания Docker-образа, для запуска контейнера нам понадобится ID этого образа. Посмотреть его можно с помощью команды:
```
docker images --no-trunc
```

![image](https://github.com/vladparh/Image-classification-2023/assets/136927535/2d6c3cb6-d72e-4e28-abf2-4ee2cfaa4083)


ID образа также можно посмотреть через Docker Desktop:

![image](https://github.com/vladparh/Image-classification-2023/assets/136927535/546ca1bb-7b85-4291-9c32-af1eb350563f)

Чтобы запустить Docker-контейнер, выполните команду ниже, вставив после "-p 8000:8000" ID образа, полученный ранее:

```
docker run -p 8000:8000 902c212f6b095b60bb212c00fbd7804f6f6628b1ff309af0f3213b7cd852cf36
```

После чего веб-сервис заработает локально и буден доступен по следующему адресу: 
```
http://localhost:8000/
```

Если что-то не заработает, можете проверить актуальный адрес в Docker Desktop:

![image](https://github.com/vladparh/Image-classification-2023/assets/136927535/175ffd17-9aff-44d6-955d-6c662a6371ef)

## Использование веб-сервиса

