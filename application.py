from email import message
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
from pymongo import MongoClient
import json
from bson import ObjectId, json_util
from bson.json_util import dumps


app = Flask(__name__)
app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database

# done!
# Просмотреть содержимое коллекции
@app.route('/')
def index():
    products = db.product.find()
    
    # ---The first version of the collection view---
    item = {}
    data = []
    for product in products:
        item = {
            'id': str(product['_id']),
            'name': product['name'],
            'description': product['description'],
            'options': product['options']
        }
        data.append(item)

    # ---The second version of the collection view---
    # data = []
    # for product in products:
    #     product['_id'] = str(product['_id'])  
    #     data.append(product)

    return jsonify(
        message='This is a "product" collection of MongoDB',
        products=data
    )


# done!
# curl -X POST http://localhost:5000/add_product -d '{"name": "product4", "description": "123444", "options": [{"english": "yesss", "german": "nooo"}]}'
# Создать новый товар
@app.route('/add_product', methods=['POST'])
def create_a_new_product():
    data = request.get_json(force=True)
    pr = db.product.insert_one(data)

    return jsonify(
        message='A new product created successfully',
        id=str(pr.inserted_id),
    ), 201


# done!
# a) Получить список названий товаров, с возможностью фильтрации по названию
    # Если надо вывести названия всех товаров коллекции, то вам нужен запрос: curl -X GET http://localhost:5000/by_name/_ (где product_name == "_")
    # Если надо проверить наличие конкретного товара, то вам нужен запрос: curl -X GET http://localhost:5000/by_name/product0 (где product0 - название вашего товара)
        # Если надо вывести еще и ID товаров, то из строк 69 и 71 нужно убрать '"_id":0' и раскомментировать строку 75
@app.route('/by_name/<product_name>', methods=['GET'])
def get_product_by_name(product_name):
    if product_name=='_':
        products = db.product.find({},{"name":1,"_id":0})
    else:
        products = db.product.find({"name": product_name},{"name":1,"_id":0})
    
    data = []
    for product in products:
        # product['_id'] = str(product['_id'])  
        data.append(product)

    return jsonify(
        data=data
    )

# done!
# curl -X GET http://localhost:5000/by_parameter/name/product0 
# curl -X GET http://localhost:5000/by_parameter/_id/622b3d98f8140baa6b613cf1 
# curl -X GET http://localhost:5000/by_parameter/description/1234 
# curl -X GET http://localhost:5000/by_parameter/english/yesss
# b) Получить список названий товаров, с возможностью фильтрации по выбранному параметру и его значению
@app.route('/by_parameter/<parameter>/<value>', methods=['GET'])
def get_product_by_parameter(parameter, value):
    if parameter=='_id':
        products = db.product.find({"_id": ObjectId(value)}, {"name":1,"_id":0})
    elif parameter=='english' or parameter=='german':
        products = db.product.find({'options': {'$elemMatch': {parameter: value}}}, {"name":1,"_id":0})
    else:
        products = db.product.find({parameter: value}, {"name":1,"_id":0})

    data = []
    for product in products:
        data.append(product)

    return jsonify(
        data=data
    )


# done!
# curl -X GET http://localhost:5000/products/6229cc91ad7f7f4a53ce9804
# Получить детали товара по ID
@app.route('/product/<product_id>', methods=['GET'])
def insert_one(product_id):
    products = db.product.find({"_id": ObjectId(product_id)})

    data = []
    for product in products:
        product['_id'] = str(product['_id'])  
        data.append(product)

    return jsonify(
        data=data
    )


# done!
# curl -X DELETE http://localhost:5000/delete_one/6229cc70ad7f7f4a53ce9803
# Удалить товар по ID
@app.route('/delete_one/<product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    # products = db.product.find()
    # data_before = []
    # for product in products:
    #     product['_id'] = str(product['_id'])  
    #     data_before.append(product)
    
    item = {
        '_id': ObjectId(product_id)
    }
    db.product.delete_one(item)
    # db.products.delete_many(item)

    # products = db.product.find()
    # data_after = []
    # for product in products:
    #     product['_id'] = str(product['_id'])  
    #     data_after.append(product)

    return jsonify(
        message='A product deleted successfully',
        # data_before=data_before,
        # data_after=data_after
    ), 200


# done!
# curl -X DELETE http://localhost:5000/delete_all
# Очистить коллекцию
@app.route('/delete_all', methods=['DELETE'])
def delete_all():
    db.product.drop()

    return jsonify(
        message='All docs in collection deleted successfully'
    ), 200


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
