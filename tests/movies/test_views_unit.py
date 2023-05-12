import pytest
from django.http import Http404

from movies.views import MovieSerializer, MovieDetail, Movie


def test_add_movie(client, monkeypatch):
    payload = {"title": "The Big Lebowski", "genre": "comedy", "year": "1998"}

    def mock_create():
        return "The Big Lebowski"

    monkeypatch.setattr(MovieSerializer, "create", mock_create)
    monkeypatch.setattr(MovieSerializer, "data", payload)

    res = client.post("/api/movies/", payload, content_type="application/json")
    assert res.status_code == 201
    assert res.data["title"] == "The Big Lebowski"


def test_add_movie_invalid_json(client):
    res = client.post("/api/movies/", {}, content_type="application/json")
    assert res.status_code == 400


def test_add_movie_invalid_json_keys(client):
    res = client.post(
        "/api/movies/",
        {"title": "The Big Lebowski", "genre": "comedy"},
        content_type="application/json",
    )
    assert res.status_code == 400


def test_get_single_movie(client, monkeypatch):
    payload = {"title": "The Big Lebowski", "genre": "comedy", "year": "1998"}


def test_get_single_movie_incorrect_id(client):
    pass


def test_get_all_movies(client, monkeypatch):
    pass


def test_remove_movie(client, monkeypatch):
    pass


def test_remove_movie_incorrect_id(client, monkeypatch):
    pass


def test_update_movie(client, monkeypatch):
    pass


def test_update_movie_incorrect_id(client, monkeypatch):
    pass


@pytest.mark.parametrize(
    "payload",
    [
        [{}],
        [{"title": "The Big Lebowski", "genre": "comedy"}]
    ]
)
def test_update_movie_invalid_json(client, monkeypatch, payload):
    pass