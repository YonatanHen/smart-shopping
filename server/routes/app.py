from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.product_service import get_products, add_products

app = Flask("Shopping list")
app = Flask(__name__.split('.')[0])

@app.route('/')
def index_api():
    return 'Smart Shopping App'

@app.route('/products', methods=['GET', 'POST'])
def products_api():
    if request.method == 'GET':
        try:
            product_list = get_products()
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500
    elif request.method == 'POST':
        try:
            product_list_json = request.get_json()
            add_products(product_list_json['product_list'])
            return jsonify(product_list_json)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

# @app.route('/add-list', methods=['POST'])
# def add_list():
#     return        

if __name__ == '__main__':
    app.run(debug=True)