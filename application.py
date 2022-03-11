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


# Просмотреть содержимое коллекции
@app.route('/')
def index():
    products = db.product.find()
    
    # item = {}
    # data = []
    # for product in products:
    #     item = {
    #         'id': str(product['_id']),
    #         'name': product['name'],
    #         'description': product['description'],
    #         'options': product['options']
    #     }
    #     data.append(item)

    data = []
    for product in products:
        product['_id'] = str(product['_id'])  
        data.append(product)

    return jsonify(
        status=True,
        message='This is a "product" collection of MongoDB',
        products=data
    )


# work!
# curl -X POST http://localhost:5000/add_product -d '{"name": "product0", "description": "123", "options": {"english": "yes", "german": "no"}}'
# Создать новый товар
@app.route('/add_product', methods=['POST'])
def create_a_new_product():
    data = request.get_json(force=True)
    pr = db.product.insert_one(data)

    return jsonify(
        status=True,
        message='A new product created successfully',
        id=str(pr.inserted_id),
    ), 201


# Получить список названий товаров, с возможностью фильтрации по: a) названию
@app.route('/get_names')
def get_names():
    products = db.product.find()

    item = {}
    data = []
    for product in products:
        item = {
            'id': str(product['_id']),
            'name': product['name']
        }
        data.append(item)

    return jsonify(
        status=True,
        data=data
    )


# # b) выбранному параметру и его значению
# @app.route('/sorty', methods=['GET','POST'])
# def sorty(parameter, value):
#     products = db.product.find({parameter: value})

#     item = {}
#     data = []
#     for product in products:
#         item = {
#             'id': str(product['_id']),
#             'name': product['name'],
#             'description': product['description'],
#             'options': product['options']
#         }
#         data.append(item)

#     return jsonify(
#         status=True,
#         data=data
#     )


# curl -X GET http://localhost:5000/products/123123123
# Получить детали товара по ID
@app.route('/products/<product_id>', methods=['GET'])
def insert_one(product_id):
    products = db.product.find_one({"_id": product_id})
    
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

    return jsonify(
        status=True,
        data=data
    )


# work!
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
        status=True,
        message='A product deleted successfully',
        # data_before=data_before,
        # data_after=data_after
    ), 200


# work!
# curl -X DELETE http://localhost:5000/delete_all
# Очистить коллекцию
@app.route('/delete_all', methods=['DELETE'])
def delete_all():
    db.product.drop()

    return jsonify(
        status=True,
        message='All docs in collection deleted successfully'
    ), 200


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
