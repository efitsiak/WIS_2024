# BEGIN CODE HERE
import numpy as np
from flask import Flask, request, jsonify ,render_template, url_for, redirect
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from pymongo import MongoClient

# END CODE HERE

#app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
#CORS(app)
#mongo = PyMongo(app)
#mongo.db.products.create_index([("name", TEXT)])

app = Flask(__name__ ,static_url_path='/static')

client = MongoClient('localhost', 27017)
db = client.db
products= db.products

products.create_index([("name", TEXT)])


@app.route("/")
def index():
    return render_template('products.html')


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get('name')  # Λαμβάνουμε την παράμετρο name από το query string

    found_products = products.find({'name': {'$regex': name, '$options': 'i'}})
    if found_products.count() == 0:
        return jsonify([])

    found_products = sorted(found_products, key=lambda x: x['price'], reverse=True)
    return jsonify(found_products)

    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    
   if request.method == 'POST':
    name = request.form['name']
    production_year = request.form['year']
    price = request.form['price']
    color = request.form['color']
    size = request.form['size']
    products.insert_one({
            "name": name,
            "year": production_year,
            "price": price,
            "color": color,
            "size": size
        })
    return redirect('add-product')
   return render_template('products.html')
 
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    query_features = request.json
    query_vector = np.array([query_features['price'], query_features['production_year'], query_features['color'],
                             query_features['size']])  # μετατροπή χαρακτηριστικών σε διάνυσμα
    collection = products
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
    url = 'https://qa.auth.gr/el/x/studyguide/600000438/current'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    elements = driver.find_elements(f"//table[@id='exam{semester}']//tr[contains(@class, 'odd') or contains(@class, "
                                    f"'even')]//td[1]")
    res = [element.text for element in elements]

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)

    # END CODE HERE
