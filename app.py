from flask import Flask
from flask_cors import CORS
from routes.list_route import list_bp
from routes.product_route import product_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(list_bp)
app.register_blueprint(product_bp)

if __name__ == '__main__':
    app.run(debug=True)
