from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
from pymongo import MongoClient


app = Flask(__name__)
app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
client = MongoClient('mongodb://localhost:27017/')
db = client.test_database


@app.route('/')
def index():
    products = db.product.find()
    
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
        message='Welcome to the Dockerized Flask MongoDB app!',
        products=data
    )


# Создать новый товар
@app.route('/create_a_new_product', methods=['POST'])
def create_a_new_product():
    data = request.get_json(force=True)
    item = {
        'product': data['product']
    }
    db.product.insert_one(item)

    return jsonify(
        status=True,
        message='A new product created successfully'
    ), 201


# Получить список названий товаров, с возможностью фильтрации по: a) названию
# @app.route('/get_names')
# def get_names():
#     products = db.product.find()

#     item = {}
#     data = []
#     for product in products:
#         item = {
#             'id': str(product['_id']),
#             'name': product['name']
#         }
#         data.append(item)

#     return jsonify(
#         status=True,
#         data=data
#     )


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


# Получить детали товара по ID
@app.route('/get_product/', methods=['POST'])
def insert_one(productId):
    products = db.product.find_one({"_id": productId})
    
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


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
