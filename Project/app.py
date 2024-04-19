# BEGIN CODE HERE
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from flask import Flask, jsonify
from flask import Flask, request
from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get('name')
    collection = mongo.db.products
    products = list(collection.find({'name': {'$regex': name, '$options': 'i'}}).sort('price', -1))
    return jsonify(products)

    # return ""
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    data = request.json
    collection = mongo.db.products
    existing_product = collection.find_one({'name': data['name']})
    if existing_product:
        collection.update_one({'_id': existing_product['_id']}, {'$set': data})
        return jsonify({'message': 'Product updated successfully'})
    else:
        inserted_data = collection.insert_one(data)
        return jsonify(str(inserted_data.inserted_id))
    # return ""
    # END CODE HERE


def calculate_similarity(query_vector, product_vectors):
    pass


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    query_vector = np.array(request.json['features'])
    collection = mongo.db.products
    product_vectors = [np.array([product['price'], product['production_year'], product['color'], product['size']]) for product in collection.find()]
    similarities = calculate_similarity(query_vector, product_vectors)
    similar_products = [product for product, similarity in zip(collection.find(), similarities) if similarity > 0.7]
    return jsonify([product['name'] for product in similar_products])
    # return ""
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    semester = request.args.get('semester')
    url = f"https://qa.auth.gr/el/x/studyguide/{semester}/current"
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    courses = [course.text.strip() for course in soup.find_all('a', class_='more')]
    driver.quit()
    return jsonify(courses)
    # return ""
    # END CODE HERE
