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


@app.route('/', methods=['GET'])
def collection_view():
    products = db.product.find()

    # # ---The first version of the collection view---
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

    # ---The second version of the collection view---
    data = []
    for product in products:
        product['_id'] = str(product['_id'])
        data.append(product)

    return jsonify(
        message='This is a collection of MongoDB',
        products=data
    )


@app.route('/add_collection', methods=['POST'])
def create_a_collection():
    collection = []
    collection = [{"name": "product0", "description": "123", "options": [{"a": "yes", "b": "no"}]},
                  {"name": "product1", "description": "1234",
                      "options": [{"a": "yess", "b": "noo"}]},
                  {"name": "product1", "description": "12345",
                   "options": [{"a": "yesss", "b": "nooo"}]},
                  {"name": "product2", "description": "123456",
                   "options": [{"a": "yessss", "b": "noooo"}]},
                  {"name": "product3", "description": "123456", "options": [{"a": "yesssss", "b": "nooooo"}]}]
    db.product.insert_many(collection)

    return jsonify(
        message='A collection created successfully',
    ), 201


@app.route('/add_product', methods=['POST'])
def create_a_new_product():
    data = request.get_json(force=True)
    pr = db.product.insert_one(data)

    return jsonify(
        message='A new product created successfully',
        id=str(pr.inserted_id),
    ), 201


# If you want to output the product IDs as well, you need to remove '"_id": 0' from lines 79 and 82 and uncomment line 86
@app.route('/by_name/<product_name>', methods=['GET'])
def get_product_by_name(product_name):
    if product_name == '_':
        products = db.product.find({}, {"name": 1, "_id": 0})
    else:
        products = db.product.find(
            {"name": product_name}, {"name": 1, "_id": 0})

    data = []
    for product in products:
        # product['_id'] = str(product['_id'])
        data.append(product)

    return jsonify(
        data=data
    )


@app.route('/by_parameter/<parameter>/<value>', methods=['GET'])
def get_product_by_parameter(parameter, value):
    if parameter == '_id':
        products = db.product.find(
            {"_id": ObjectId(value)}, {"name": 1, "_id": 0})
    elif parameter == 'a' or parameter == 'b':
        products = db.product.find(
            {'options': {'$elemMatch': {parameter: value}}}, {"name": 1, "_id": 0})
    else:
        products = db.product.find({parameter: value}, {"name": 1, "_id": 0})

    data = []
    for product in products:
        data.append(product)

    return jsonify(
        data=data
    )


@app.route('/product/<product_id>', methods=['GET'])
def get_product_details_by_id(product_id):
    products = db.product.find({"_id": ObjectId(product_id)})

    data = []
    for product in products:
        product['_id'] = str(product['_id'])
        data.append(product)

    return jsonify(
        data=data
    )


@app.route('/delete_one/<product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    item = {
        '_id': ObjectId(product_id)
    }
    db.product.delete_one(item)
    # db.products.delete_many(item)

    return jsonify(
        message='A product deleted successfully',
    ), 200


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
