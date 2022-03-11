# Микросервис для электронного магазина
Веб-приложение написано на Python с помощью web framework Flask. Реализованы REST-API функции. Сущности хранятся в MongoDB.

Модель/cущности: Товар - отвечает за товар на складе, например - телефон такой-то марки от такого-то производителя.

Поля: идентификатор (ID), название, описание, параметры: массив пар ключ/значение.

## ЗАДАНИЕ. REST API методы, которые необходимо создать:
- Создать новый товар
- Получить список названий товаров, с возможностью фильтрации по:
   * a) названию
   * b) выбранному параметру и его значению
- Получить детали товара по ID


# Инструкция использования микросервиса
### Необходимые шаги для инсталляции:
`pip install -r requirements.txt`

### Запуск:
`docker run -d -p 27017:27017 mongo`

`python run.py`

### Что можно делать внутри микросервиса (описание методов REST-API):

- __Заполнить коллекцию данными для тестирования__ (def create_a_collection()): `curl -X POST http://localhost:5000/add_collection`
- __Просмотреть полное содержимое коллекции__ (def collection_view()): `curl -X GET http://localhost:5000/`
- __Удалить товар по ID__ (def delete_one_product(product_id)): `curl -X DELETE http://localhost:5000/delete_one/6229cc70ad7f7f4a53ce9803`, где `6229cc70ad7f7f4a53ce9803` - это ID товара
- __Очистить коллекцию__ (def delete_all()): `curl -X DELETE http://localhost:5000/delete_all`

#### А также (по заданию):

* __Создать новый товар__ (def create_a_new_product()): `curl -X POST http://localhost:5000/add_product -d '{"name": "product4", "description": "123444", "options": [{"a": "yes0", "b": "no0"}]}'`
* __Получить список названий товаров, с возможностью фильтрации по названию__ (def get_product_by_name(product_name)):
    * Если надо __*вывести названия всех товаров коллекции*__, то вам нужен запрос: `curl -X GET http://localhost:5000/by_name/_`, где product_name == "_"
    * Если надо __*проверить наличие конкретного товара*__, то вам нужен запрос: `curl -X GET http://localhost:5000/by_name/product1`, где product1 - название вашего товара
- __Получить список названий товаров, с возможностью фильтрации по выбранному параметру и его значению__ (def get_product_by_parameter(parameter, value)):
    * Фильтрация __*по названию*__: `curl -X GET http://localhost:5000/by_parameter/name/product1`, где product1 - название вашего товара
    * Фильтрация __*по ID*__: `curl -X GET http://localhost:5000/by_parameter/_id/622b5087d143ec233eae2bd5`, где 622b5087d143ec233eae2bd5 - ID вашего товара
    * Фильтрация __*по описанию*__: `curl -X GET http://localhost:5000/by_parameter/description/123456`, где 123456 - описание товара
    * Фильтрация __*по параметрам*__ (в данном случае a или b): `curl -X GET http://localhost:5000/by_parameter/a/yesss`  
- __Получить детали товара по ID__ (def get_product_details_by_id(product_id)): `curl -X GET http://localhost:5000/product/622b5087d143ec233eae2bd5`, где 622b5087d143ec233eae2bd5 - ID вашего товара

