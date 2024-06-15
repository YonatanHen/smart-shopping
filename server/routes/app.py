from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ML.fetch import get_products

app = Flask("Shopping list")
app = Flask(__name__.split('.')[0])

@app.route('/')
def index():
    return 'Hello World'

@app.route('/products', methods=['GET'])
def products():
    try:
        product_list = get_products()
        return jsonify(product_list.to_dict(orient="records"))
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500

@app.route('/add-grocery', methods=['POST'])
def add_grocery():
    return        

if __name__ == '__main__':
    app.run(debug=True)