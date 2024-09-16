from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.product_service import get_all_products, delete_product, get_products_by_list_id
from services.list_service import add_list, get_lists, delete_list, add_products_to_list
from services.utils.calculate_list import calculate_new_list

app = Flask("Shopping list")
app = Flask(__name__.split('.')[0])


@app.route('/')
def index_api():
    return 'Smart Shopping App'


@app.route('/products', methods=['GET'])
def products_api():
    if request.method == 'GET':
        try:
            product_list = get_all_products()
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

@app.route('/products/<int:id>', methods=['GET'])
def products_list_api(id):
    if request.method == 'GET':
        try:
            product_list = get_products_by_list_id(id)
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

@app.route('/products/<string:product_name>/<int:id>', methods=['DELETE'])
def products_name_id_api(product_name, id):
    if request.method == 'DELETE':
        try:
            updated_list = delete_product(product_name, id)
            if updated_list is None:
                raise ValueError('Product not found')
            return jsonify(updated_list.to_dict(orient='records'))
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/list', methods=['GET', 'POST'])
def lists_api():
    if request.method == 'GET':
        try:
            lists = get_lists()
            return jsonify(lists.to_dict(orient='records'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            product_list_json = request.get_json()
            add_list(product_list_json)
            return jsonify(product_list_json)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500


@app.route('/list/<int:id>', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def list_id_api(id):
    if request.method == 'PATCH':
        try:
            product_list_json = request.get_json()
            updated_list = add_products_to_list(id,product_list_json)
            return jsonify(updated_list)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

    if request.method == 'PUT':
        return 'update list'

    elif request.method == 'DELETE':
        try:
            deleted_list = delete_list(id)
            return jsonify(deleted_list)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500
    
@app.route('/list/suggest/<int:precision>', methods=['GET'])
def suggest_list_api(precision):
    try:
        return calculate_new_list(precision)
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500       

if __name__ == '__main__':
    app.run(debug=True)
