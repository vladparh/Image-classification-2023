from fastapi.testclient import TestClient
from fastapi_main import app

# For start tests: pytest --cov-report html --cov .
client = TestClient(app)


def test_help_func():
    """Тестирование метода /help"""
    response = client.get('/help')
    assert response.status_code == 200
    assert response.text == '"Наша модель классифицирует следующие объекты:small vehicle, large vehicle, tennis court, ground track field, ship, harbor, storage tank,swimming pool, plane, bridge, roundabout, baseball diamond, soccer ball field, basketball court, helicopter. На примере Postman, Чтобы получить изображение с классифицией объектов, отправь файл, являющийся изображением в формате .png или .jpg. (Params: Body, type of key: File, параметр: file), пример запроса: http://0.0.0.0:8000/uploadfile/. Доступные команды сервиса: GET: /check/ - проверка статуса работы сервиса; GET: /help/ - справка; POST: /uploadfile/ - отправка изображения и получение его с применённой классификацией; POST: /mode/ - параметр gray - модель будет возвращать чёрно-белые изображения, параметр default - ; обычныеPOST: /"'


def test_get_last_image_no_image():
    """Тестирование метода /last, когда изображение не загружено"""
    response = client.get('/last')
    assert response.status_code == 200
    assert response.text == '"Вы пока не загрузили ни одного изображения. Доступные команды смотрите по /help"'


def test_change_mode_default():
    """Тестирование метода /mode с параметром default"""
    response = client.post('/mode', params={'mode': 'default'})
    assert response.status_code == 200
    assert response.text == '"Модель будет возвращать обычные изображения"'


def test_change_mode_wrong():
    """Тестирование метода /mode с неправильным параметром wrong"""
    response = client.post('/mode', params={'mode': 'wrong'})
    assert response.status_code == 400
    assert response.text == '{"detail":"BAD REQUEST. Возможные параметры запроса: {gray} или {default}"}'


def test_change_mode_gray():
    """Тестирование метода /mode с параметром gray"""
    response = client.post('/mode', params={'mode': 'gray'})
    assert response.status_code == 200
    assert response.text == '"Модель будет возвращать чёрно-белые изображения"'


def test_create_upload_file_image():
    """Тестирование метода /uploadfile загрузкой изображения"""
    response = client.post('/uploadfile', files={'file': open('test_data/test_img.jpg', 'rb')})
    assert response.status_code == 200


def test_get_last_image_with_image():
    """Тестирование метода /last, когда изображение загружено"""
    response = client.get('/last')
    assert response.status_code == 200
    assert response.json() == {'filename': 'test_img.jpg', 'size': [1484,1312]}


def test_create_upload_file_non_image():
    """Тестирование метода /uploadfile загрузкой не изображения"""
    response = client.post('/uploadfile', files={'file': open('test_data/non_image.txt', 'rb')})
    assert response.status_code == 500
    assert response.text == '{"detail":"File must be an image (.png or .jpg)"}'
