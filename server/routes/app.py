from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.product_service import get_all_products
from services.list_service import add_list, edit_list

app = Flask("Shopping list")
app = Flask(__name__.split('.')[0])

@app.route('/')
def index_api():
    return 'Smart Shopping App'

@app.route('/products', methods=['GET', 'POST', 'UPDATE'])
def products_api():
    if request.method == 'GET':
        try:
            product_list = get_all_products()
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

@app.route('/list', methods=['GET', 'POST', 'UPDATE'])
def lists_api():
    if request.method == 'POST':
        try:
            product_list_json = request.get_json()
            add_list(product_list_json['product_list'])
            return jsonify(product_list_json)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500
    elif request.method == 'UPDATE':
        try:
            product_list_json = request.get_json()
            edit_list(product_list_json['product_list'])
            return jsonify(product_list_json)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run(debug=True)