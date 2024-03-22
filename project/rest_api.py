from flask import Blueprint
from flask_restful import Resource, reqparse


rest_api = Blueprint('rest_api_bp', __name__, url_prefix='/api')


@rest_api.route('/hell', methods=['GET', 'POST'])
def api_posts():
    # Handle GET request
    print('I was here')
    return {'message': 'Hello, World!'}

