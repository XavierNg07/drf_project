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


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    res = client.post(
        '/api/movies/',
        {},
        content_type='application/json'
    )
    assert res.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    res = client.post(
        '/api/movies/',
        {
            'title': 'Someday or One Day',
            'genre': 'drama',
        },
        content_type='application/json'
    )
    assert res.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title='Along with the Gods: The Two Worlds', genre='action', year='2017')
    res = client.get(f'/api/movies/{movie.id}/')
    assert res.status_code == 200
    assert res.data['title'] == 'Along with the Gods: The Two Worlds'


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title='The Big Lebowski', genre='comedy', year='1998')
    movie_two = add_movie('No Country for Old Men', 'thriller', '2007')
    res = client.get(f'/api/movies/')
    assert res.status_code == 200
    assert res.data[0]['title'] == movie_one.title
    assert res.data[1]['title'] == movie_two.title
