import json
import pytest
from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    res = client.post(
        '/api/movies/',
        {
            'title': 'Now You See Me 2',
            'genre': 'action',
            'year': '2016',
        },
        content_type='application/json'
    )
    assert res.status_code == 201
    assert res.data['title'] == 'Now You See Me 2'

    movies = Movie.objects.all()
    assert len(movies) == 1
