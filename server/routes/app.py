from flask import Flask, request, jsonify

app = Flask("Shopping list")
app = Flask(__name__.split('.')[0])

@app.route('/')
def index():
    return 'Hello World'

@app.route('/json-test', methods=['POST'])
def post_test():
    try:
        json_data = request.get_json()
        return jsonify(json_data)
    except Exception as e:
        error_message = str(e)
        return jsonify({'error': error_message}), 400

@app.route('/add-grocery', methods=['POST'])
def add_grocery():
    return        

@app.route('/recommend', methods=['POST'])
def recommend():
    return 

if __name__ == '__main__':
    app.run(debug=True)