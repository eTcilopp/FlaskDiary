from flask_restful import Resource, reqparse
# from .main import api


@api.route('/api/myresource', methods=['GET', 'POST'])
class MyResource(Resource):
    def get(self):
        # Handle GET request
        return {'message': 'Hello, World!'}

    def post(self):
        # Handle POST request
        # Use reqparse or request.get_json() to parse incoming data
        return {'message': 'Data received'}, 201
