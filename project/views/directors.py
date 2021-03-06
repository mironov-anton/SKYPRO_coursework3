from flask_restx import Namespace, Resource, abort

from project.exceptions import ItemNotFound
from project.services import DirectorsService
from project.setup_db import db
from project.tools.auth import auth_required

directors_ns = Namespace("directors")


@directors_ns.route("/")
class DirectorsView(Resource):
    @auth_required
    @directors_ns.response(200, "OK")
    def get(self, token_data):
        return DirectorsService(db.session).get_all_directors()


@directors_ns.route("/<int:director_id>")
class DirectorView(Resource):
    @auth_required
    @directors_ns.response(200, "OK")
    @directors_ns.response(404, "Director not found")
    def get(self, director_id: int, token_data):
        try:
            return DirectorsService(db.session).get_item_by_id(director_id)
        except ItemNotFound:
            abort(404, message="Director not found")
