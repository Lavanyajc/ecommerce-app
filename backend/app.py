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
            {
                "name": "T-shirt",
                "category": "Men",
                "description": "100% cotton casual wear",
                "price": 499
            },
            {
                "name": "Saree",
                "category": "Women",
                "description": "Elegant traditional silk saree",
                "price": 1499
            },
            {
                "name": "Laptop",
                "category": "Electronics",
                "description": "i7, 16GB RAM, 512GB SSD",
                "price": 55999
            },
            {
                "name": "Sofa",
                "category": "Home",
                "description": "Luxury 3-seater sofa",
                "price": 23999
            },
            {
                "name": "Cricket Bat",
                "category": "Sports",
                "description": "Professional grade willow bat",
                "price": 1999
            },
            {
                "name": "Novel",
                "category": "Books",
                "description": "Fictional thriller bestseller",
                "price": 299
            }
        ])
        print("🔹 Seeded products collection with sample data.")

# Seed on startup
seed_db()

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the E-commerce API"})

@app.route('/products')
def get_products():
    products = db.products.find()
    return jsonify([
        {
            "name": p.get("name", "Unnamed Product"),
            "description": p.get("description", "No description available."),
            "price": p.get("price", "N/A")
        } for p in products
    ])

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
