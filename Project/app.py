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

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/")
def index():
    return render_template('homepage.html')

@app.route("/products")
def products():
    try:
        return render_template('products.html')
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while trying to load the products page."



@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get('name')  
    
    found_products = mongo.db.products.find({'name': {'$regex': name, '$options': 'i'}})
    found_products_list = list(found_products)  # Μετατροπή του Cursor σε λίστα
    
    if len(found_products_list) == 0:
        return jsonify([])

    # Ταξινόμηση των προϊόντων κατά φθίνουσα σειρά τιμής
    found_products_sorted = sorted(found_products_list, key=lambda x: x['price'], reverse=True)
    
    # Μετατροπή των αποτελεσμάτων σε λίστα JSON objects
    results = []
    for product in found_products_sorted:
        result = {
            "id": str(product['_id']),  # Μετατροπή ObjectId σε string
            "name": product['name'],
            "production_year": product['year'],
            "price": product['price'],
            "color": product['color'],
            "size": product['size']
        }
        results.append(result)
    
    return jsonify(results)

    # END CODE HERE


@app.route("/add-product", methods=['POST'])
def add_product():
    # BEGIN CODE HERE
        data = request.get_json()  # Get the JSON data from the request
        name = data.get('name')
        production_year = data.get('year')
        price = data.get('price')
        color = data.get('color')
        size = data.get('size')
        print(f"Received data: {data}")  # Debug print statement
        
        
         # Μετατρέπουμε το χρώμα από το κείμενο στον αντίστοιχο κωδικό
        colors_mapping = {
         'red': 1,
          'yellow': 2,
         'blue': 3
         }
        color_code = colors_mapping.get(data.get('color').lower())  # Χρησιμοποιούμε lower() για να αντιστοιχίσουμε ανεξαρτήτως πεζών-κεφαλαίων

    # Μετατρέπουμε το μέγεθος από το κείμενο στον αντίστοιχο κωδικό
        sizes_mapping = {
        'small': 1,
        'medium': 2,
        'large': 3,
        'extra large': 4
        }
        size_code = sizes_mapping.get(data.get('size').lower()) 
        mongo.db.products.insert_one({
            "name": name,
            "year": production_year,
            "price": price,
            "color": color_code,
            "size": size_code
        })
        return jsonify({"status": "success"}), 201  # Return success response
  
       
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
