import pytest
from movies.models import Movie


@pytest.fixture(scope='function')
def add_movie():
    # use the "factory as fixture" pattern to add a few movies
    def _add_movie(title, genre, year):
        movie = Movie.objects.create(title=title, genre=genre, year=year)
        return movie
    return _add_movie
