from .auth import auth_ns
from .genres import genres_ns
from .movies import movies_ns
from .directors import directors_ns
from .user import user_ns

__all__ = [
    "genres_ns",
    "directors_ns",
    "movies_ns",
    "auth_ns",
    "user_ns"
]
