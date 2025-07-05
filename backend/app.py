from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongo:27017/ecommerce'))
db = client['ecommerce']

# Seed the database on startup if empty
def seed_db():
    if db.products.count_documents({}) == 0:
        db.products.insert_many([
    {"name": "T-shirt", "category": "Men"},
    {"name": "Saree", "category": "Women"},
    {"name": "Laptop", "category": "Electronics"},
    {"name": "Sofa", "category": "Home"},
    {"name": "CricketBat", "category": "Sports"},
    {"name": "Novel", "category": "Books"}
])

        print("🔹 Seeded products collection with sample data.")

# Seed immediately on startup
seed_db()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the E-commerce API"})

@app.route('/products')
def get_products():
    products = db.products.find()
    return jsonify([{"name": p["name"]} for p in products])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

