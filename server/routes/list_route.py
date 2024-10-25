from flask import Blueprint, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.list_service import add_list, get_lists, get_products_by_list_id, delete_list, add_products_to_list
from services.utils.calculate_list import calculate_new_list

list_bp = Blueprint('list',__name__,url_prefix='/list')

@list_bp.route('/', methods=['GET', 'POST'])
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


@list_bp.route('/<int:id>/product', methods=['GET'])
def products_list_api(id):
    if request.method == 'GET':
        try:
            product_list = get_products_by_list_id(id)
            return jsonify(product_list.to_dict(orient="records"))
        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message}), 500


@list_bp.route('/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
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
    
    
@list_bp.route('/suggest', methods=['GET'])
def suggest_list_api():
    try:
        return calculate_new_list()
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 500       
