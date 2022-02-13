from flask_restx import Namespace, reqparse, Resource, abort

from project.exceptions import ItemNotFound
from project.services import MoviesService
from project.setup_db import db

movies_ns = Namespace("movies")
parser = reqparse.RequestParser()  # Enables adding and parsing of multiple arguments in the context of a single request.
parser.add_argument("page", type=int)  # Adds an argument to be parsed.
parser.add_argument("status", type=str)


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.expect(parser)  # A decorator to Specify the expected input model
    # @auth_required
    @movies_ns.response(200, "OK")  # A decorator to specify one of the expected responses
    def get(self):
        req_args = parser.parse_args()
        if any(req_args.values()):
            return MoviesService(db.session).get_filter_movies(req_args)
        else:
            return MoviesService(db.session).get_all_movies()


@movies_ns.route("/<int:movie_id>")
class MovieView(Resource):
    # @auth_required
    @movies_ns.response(200, "OK")
    @movies_ns.response(404, "Movie not found")
    def get(self, movie_id: int):
        try:
            return MoviesService(db.session).get_item_by_id(movie_id)
        except ItemNotFound:
            abort(404, message="Movie not found")
