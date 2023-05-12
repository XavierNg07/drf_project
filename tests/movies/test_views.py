import pytest

from movies.models import Movie


@pytest.mark.django_db
def test_add_movie(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    res = client.post(
        "/api/movies/",
        {
            "title": "Now You See Me 2",
            "genre": "action",
            "year": "2016",
        },
        content_type="application/json",
    )
    assert res.status_code == 201
    assert res.data["title"] == "Now You See Me 2"

    movies = Movie.objects.all()
    assert len(movies) == 1


@pytest.mark.django_db
def test_add_movie_invalid_json(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    res = client.post(
        "/api/movies/",
        {},
        content_type="application/json",
    )
    assert res.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_add_movie_invalid_json_keys(client):
    movies = Movie.objects.all()
    assert len(movies) == 0

    res = client.post(
        "/api/movies/",
        {
            "title": "Someday or One Day",
            "genre": "drama",
        },
        content_type="application/json",
    )
    assert res.status_code == 400

    movies = Movie.objects.all()
    assert len(movies) == 0


@pytest.mark.django_db
def test_get_single_movie(client, add_movie):
    movie = add_movie(title="Along with the Gods: The Two Worlds", genre="action", year="2017")
    res = client.get(f"/api/movies/{movie.id}/")
    assert res.status_code == 200
    assert res.data["title"] == "Along with the Gods: The Two Worlds"


@pytest.mark.django_db
def test_get_all_movies(client, add_movie):
    movie_one = add_movie(title="The Big Lebowski", genre="comedy", year="1998")
    movie_two = add_movie(title="No Country for Old Men", genre="thriller", year="2007")
    res = client.get("/api/movies/")
    assert res.status_code == 200
    assert res.data[0]["title"] == movie_one.title
    assert res.data[1]["title"] == movie_two.title


@pytest.mark.django_db
def test_remove_movie(client, add_movie):
    movie = add_movie(title="Along with the Gods: The Two Worlds", genre="action", year="2017")

    res = client.get(f"/api/movies/{movie.id}/")
    assert res.status_code == 200
    assert res.data["title"] == "Along with the Gods: The Two Worlds"

    res_two = client.delete(f"/api/movies/{movie.id}/")
    assert res_two.status_code == 204

    res_three = client.get("/api/movies/")
    assert res_three.status_code == 200
    assert len(res_three.data) == 0


@pytest.mark.django_db
def test_remove_movie_incorrect_id(client):
    res = client.delete(f"/api/movies/99/")
    assert res.status_code == 404


@pytest.mark.django_db
def test_update_movie(client, add_movie):
    movie = add_movie(title="Along with the Gods: The Two Worlds", genre="action", year="2017")

    res = client.put(
        f"/api/movies/{movie.id}/",
        {
            "title": "Along with the Gods: The Two Worlds",
            "genre": "action",
            "year": "2018"
        },
        content_type="application/json",
    )
    assert res.status_code == 200
    assert res.data["title"] == "Along with the Gods: The Two Worlds"
    assert res.data["year"] == "2018"

    res_two = client.get(f"/api/movies/{movie.id}/")
    assert res_two.status_code == 200
    assert res_two.data["title"] == "Along with the Gods: The Two Worlds"
    assert res_two.data["year"] == "2018"


@pytest.mark.django_db
def test_update_movie_incorrect_id(client):
    res = client.put(f"/api/movies/99/")
    assert res.status_code == 404


@pytest.mark.django_db
def test_update_movie_invalid_json(client, add_movie):
    movie = add_movie(title="Along with the Gods: The Two Worlds", genre="action", year="2017")
    res = client.put(
        f"/api/movies/{movie.id}/",
        {},
        content_type="application/json",
    )
    assert res.status_code == 400


@pytest.mark.django_db
def test_update_movie_invalid_json_keys(client, add_movie):
    movie = add_movie(title="Along with the Gods: The Two Worlds", genre="action", year="2017")

    res = client.put(
        f"/api/movies/{movie.id}/",
        {"title": "Along with the Gods: The Two Worlds"},
        content_type="application/json",
    )
    assert res.status_code == 400