from flask import current_app

from project.dao.movie import MovieDAO
from project.exceptions import ItemNotFound
from project.schemas.movie import MovieSchema
from project.services.base import BaseService


class MoviesService(BaseService):
    def get_item_by_id(self, pk):
        movie = MovieDAO(self._db_session).get_by_id(pk)
        if not movie:
            raise ItemNotFound
        return MovieSchema().dump(movie)

    def get_all_movies(self):
        movies = MovieDAO(self._db_session).get_all()
        return MovieSchema(many=True).dump(movies)

    def get_filter_movies(self, filter_args):
        limit = 0
        offset = 0
        if filter_args.get("page"):
            limit = current_app.config["ITEMS_PER_PAGE"]
            offset = (filter_args.get("page") - 1) * limit
        status = filter_args.get("status")
        movies = MovieDAO(self._db_session).get_filter(limit=limit, offset=offset, status=status)
        return MovieSchema(many=True).dump(movies)
