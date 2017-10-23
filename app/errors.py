
from flask import make_response, jsonify
from app import app


# ============================   Error handlers   ===========================

@app.errorhandler(404)
def not_found(error):
    """
    RESTful 404 error
    """

    return make_response(jsonify({'error': 'Not found', 'code': 404})), 404
