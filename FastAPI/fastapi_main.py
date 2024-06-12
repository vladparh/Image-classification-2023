from fastapi import FastAPI, File, UploadFile, HTTPException
import torch as torch
from PIL import Image
import shutil
from fastapi.responses import FileResponse
import uvicorn
from ultralytics import YOLO

app = FastAPI()

torch.hub._validate_not_a_forked_repo=lambda a,b,c: True  # для корректной загрузки в случае деплоя
model = YOLO(r"last.pt")


class ModelClass:  # класс, для хранения инфы про режим работы и последнее изображение
    def __init__(self, mode='Default', last_im=None, last_im_name=None):
        self.mode = mode
        self.last_im = last_im
        self.last_im_name = last_im_name


model_class = ModelClass()


@app.get('/help')  # вызов справки
def help_func():
    objects = "small vehicle, large vehicle, tennis court, ground track field, ship, harbor, storage tank," \
              "swimming pool, plane, bridge, roundabout, baseball diamond, soccer ball field, basketball court, " \
              "helicopter"

    return f"Наша модель классифицирует следующие объекты:{objects}. На примере Postman, Чтобы получить " \
           f"изображение с классифицией объектов, отправь файл, являющийся изображением в формате .png или .jpg. " \
           f"(Params: Body, type of key: File, параметр: file), пример запроса: http://localhost:8000/uploadfile. " \
           f"Доступные команды сервиса: " \
           f"GET: /check/ - проверка статуса работы сервиса; " \
           f"GET: /help/ - справка; " \
           f"POST: /uploadfile/ - отправка изображения и получение его с применённой классификацией; " \
           f"POST: /mode/ - параметр gray - модель будет возвращать чёрно-белые изображения, параметр default - ; " \
           f"обычныеPOST: /"


@app.get('/last')  # получить информацию о последнем загруженном изображении
async def get_last_image():
    if model_class.last_im is None:
        return "Вы пока не загрузили ни одного изображения. Доступные команды смотрите по /help"
    else:
        return {'filename': model_class.last_im_name, 'size': model_class.last_im.size}


@app.post("/mode") # выбор типа изображения: обычное или черно-белое
async def change_mode(mode: str) -> str:
    if mode == 'gray' or mode == 'Gray':
        model_class.mode = 'L'
        return 'Модель будет возвращать чёрно-белые изображения'
    elif mode == 'default' or mode == 'Default':
        model_class.mode = 'Default'
        return 'Модель будет возвращать обычные изображения'
    else:
        raise HTTPException(status_code=400, detail='BAD REQUEST. Возможные параметры запроса: {gray} или {default}')


@app.post("/uploadfile") # получение предсказаний модели
async def create_upload_file(file: UploadFile = File(...)):
    try:
        shutil.rmtree("runs\detect\predict")  # после отправки удаляем фолдер, чтобы не засорять папку
    except:  # если это первый запуск, удаление не произойдёт и мы идём далее
        pass
    try:
        im = Image.open(file.file)  # проверяем является ли файл изображением
        model_class.last_im_name = file.filename
        model_class.last_im = im
        if model_class.mode == 'L':  # перекрашиваем в черно-белый если юзер менял мод работы
            im = im.convert("L")
        im = im.save(file.filename)

        res = model(file.filename, save=True)
        return FileResponse(rf"runs\detect\predict\{file.filename}")
    except Exception:
        raise HTTPException(status_code=500, detail='Файл должен быть изображением (.png or .jpg)')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
