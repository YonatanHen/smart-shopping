from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.product_service import get_all_products, delete_product, get_products_by_list_id, update_product
from services.list_service import add_list, get_lists, delete_list, add_products_to_list
from services.utils.calculate_list import calculate_new_list

app = Flask("Shopping list")
app = Flask(__name__.split('.')[0])
CORS(app)

@app.route('/')
def index_api():
    return 'Smart Shopping App'


@app.route('/product', methods=['GET'])
def products_api():
    if request.method == 'GET':
        try:
            product_list = get_all_products()
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500


@app.route('/product/<int:id>', methods=['GET'])
def products_list_api(id):
    if request.method == 'GET':
        try:
            product_list = get_products_by_list_id(id)
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500


@app.route('/list/<int:list_id>/product/<string:product_name>', methods=['DELETE', 'PUT'])
def list_id_product_name_api(list_id, product_name):
    if request.method == 'DELETE':
        try:
            deleted_product = delete_product(product_name, list_id)
            
            if deleted_product is None:
                raise ValueError('Product not found')
            
            return jsonify(deleted_product)
        
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    elif request.method == 'PUT':
        try:
            product_data = request.get_json()
            updated_product = update_product(product_name, list_id, product_data)
            
            if updated_product is None:
                raise ValueError('Product not found')
            
            return jsonify(updated_product)
        
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


@app.route('/list/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def list_id_api(id):
    if request.method == 'PATCH':
        try:
            product_list_json = request.get_json()
            updated_list = add_products_to_list(id,product_list_json)
            return jsonify(updated_list)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

    elif request.method == 'DELETE':
        try:
            deleted_list = delete_list(id)
            return jsonify(deleted_list)
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500
    
    
@app.route('/list/suggest/', methods=['GET'])
def suggest_list_api():
    try:
        return calculate_new_list()
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500       


if __name__ == '__main__':
    app.run(debug=True)
