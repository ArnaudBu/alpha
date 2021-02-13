from flask import Blueprint

blueprint = Blueprint(
    'back_blueprint',
    __name__,
    url_prefix='/api'
)
