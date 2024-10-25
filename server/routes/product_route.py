from flask import Blueprint, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.product_service import get_all_products, delete_product, update_product


product_bp = Blueprint('product',__name__,url_prefix='product')

@product_bp.route('/', methods=['GET'])
def products_api():
    if request.method == 'GET':
        try:
            product_list = get_all_products()
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500

@product_bp.route('<string:product_name>/list/<int:list_id>', methods=['DELETE', 'PUT'])
def list_id_product_name_api(product_name,list_id):
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