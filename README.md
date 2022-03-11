# Микросервис для электронного магазина
Веб-приложение написано на Python с помощью web framework Flask. Реализованы REST-API функции. Сущности хранятся в MongoDB.

Модель/cущности: Товар - отвечает за товар на складе, например - телефон такой-то марки от такого-то производителя.

Поля: идентификатор (ID), название, описание, параметры: массив пар ключ/значение.

## ЗАДАНИЕ. REST API методы, которые необходимо создать:
- Создать новый товар
- Получить список названий товаров, с возможностью фильтрации по:
a) названию
b) выбранному параметру и его значению
- Получить детали товара по ID

## Необходимые шаги для инсталляции:
pip install -r requirements.txt

## Запуск:
docker run -d -p 27017:27017 mongo

python run.py

## curl команды с нужными параметрами для прохождения тестового сценария:
* создать товар: curl.exe -d "@insert.json" -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/create_a_new_product/
* найти товар:
** по названию: ---
** по параметру: ---
* получить детали найденного товара: curl.exe -d "621f4d1d2fb1e13c2d5ac82a" -X POST http://127.0.0.1:5000/get_product/

# Что можно делать внутри микросервиса:

- Заполнить коллекцию данными для тестирования (def create_a_collection()): curl -X POST http://localhost:5000/add_collection
- Просмотреть полное содержимое коллекции (def collection_view()): curl -X GET http://localhost:5000/
- Удалить товар по ID (def delete_one_product(product_id)): curl -X DELETE http://localhost:5000/delete_one/6229cc70ad7f7f4a53ce9803 (где 6229cc70ad7f7f4a53ce9803 - это ID товара)
- Очистить коллекцию (def delete_all()): curl -X DELETE http://localhost:5000/delete_all

## А также (по заданию):

- Создать новый товар (def create_a_new_product()): curl -X POST http://localhost:5000/add_product -d '{"name": "product4", "description": "123444", "options": [{"a": "yes0", "b": "no0"}]}'
- Получить список названий товаров, с возможностью фильтрации по названию (def get_product_by_name(product_name))
    * Если надо вывести названия всех товаров коллекции, то вам нужен запрос: curl -X GET http://localhost:5000/by_name/_ (где product_name == "_")
    * Если надо проверить наличие конкретного товара, то вам нужен запрос: curl -X GET http://localhost:5000/by_name/product1 (где product1 - название вашего товара)
        * Если надо вывести еще и ID товаров, то из строк 69 и 71 нужно убрать '"_id":0' и раскомментировать строку 75 в файле application.py
- Получить список названий товаров, с возможностью фильтрации по выбранному параметру и его значению (def get_product_by_parameter(parameter, value))
    * Фильтрация по названию: curl -X GET http://localhost:5000/by_parameter/name/product1 (где product1 - название вашего товара)
    * Фильтрация по ID: curl -X GET http://localhost:5000/by_parameter/_id/622b5087d143ec233eae2bd5 (где 622b5087d143ec233eae2bd5 - ID вашего товара)
    * Фильтрация по описанию: curl -X GET http://localhost:5000/by_parameter/description/123456 (где 1234 - описание товара)
    * Фильтрация по параметрам (в данном случае a или b): curl -X GET http://localhost:5000/by_parameter/a/yesss  
- Получить детали товара по ID (def get_product_details_by_id(product_id)): curl -X GET http://localhost:5000/products/622b5087d143ec233eae2bd5 (где 622b5087d143ec233eae2bd5 - ID вашего товара)

