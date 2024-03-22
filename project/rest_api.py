from flask import Blueprint, request
from flask_restful import Resource, reqparse


rest_api = Blueprint('rest_api_bp', __name__, url_prefix='/api')


@rest_api.route('/hell', methods=['GET', 'POST'])
def api_posts():
    if request.method == 'POST':
        return {'message': f'Hello, World ! POST {request.headers}'}
    elif request.method == 'GET':
        return {'message': f'Hello, World ! GET {request.headers}'}


