from flask import Blueprint, jsonify, request

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def index():
    return "Server is up ..."
