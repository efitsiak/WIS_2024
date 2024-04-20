# BEGIN CODE HERE
import numpy as np
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get('name')  # λαμβάνει όνομα
    products = list(mongo.db.products.find({'name': {'$regex': name, '$options': 'i'}}).sort('price', -1))  #
    # βρίσκουμε τα προϊόντα στη βάση με το ίδιο όνομα και τα ταξινομούμε κατά φθίνουσα σειρά
    return jsonify(products)

    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    data = request.json  # λαμβάνουμε δεδομένα από το body του post request
    existing_product = mongo.db.products.find_one({'name': data['name']})
    if existing_product:
        mongo.db.products.update_one(
            {'name': data['name']},
            {'$set': {
                'price': data['price'],
                'production_year': data['production_year'],
                'color': data['color'],
                'size': data['size']
            }})
    else:
        mongo.db.products.insert_one(data)

    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    query_features = request.json
    query_vector = np.array([query_features['price'], query_features['production_year'], query_features['color'],
                             query_features['size']])  # μετατροπή χαρακτηριστικών σε διάνυσμα
    collection = mongo.db.products
    product_vectors = [np.array([product['price'], product['production_year'], product['color'], product['size']])
                       for product in collection.find()]

    # Υπολογίζουμε την ομοιότητα cosine similarity μεταξύ του query και κάθε προϊόντος

    similarities = []
    for product_vector in product_vectors:
        dot_product = np.dot(query_vector, product_vector)
        query_vector_norm = np.linalg.norm(query_vector)
        product_vector_norm = np.linalg.norm(product_vector)
        similarity = dot_product / (query_vector_norm * product_vector_norm)
        similarities.append(similarity)

    # Επιλέγουμε τα προϊόντα που έχουν ομοιότητα πάνω από 70%
    similar_products = [product for product, similarity in zip(collection.find(), similarities) if similarity > 0.7]

    # Επιστρέφουμε τα ονόματα των παρόμοιων προϊόντων
    return jsonify([product['name'] for product in similar_products])
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


# Συνδέεστε στο MongoDB server
client = MongoClient('localhost', 27017)

# Δημιουργείτε ή επιλέγετε τη βάση δεδομένων
db = client['pspi']
