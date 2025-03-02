"""
Tests for the Animals Resource
"""

import json
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event
from werkzeug.datastructures import Headers

from quotesapi import create_app, db
from quotesapi.models import Animals

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    ''' Connect database '''
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def client():
    """Set up a test client for Flask. This client code is generated with chatgpt."""
    app = create_app()  # Create Flask app
    app.config["TESTING"] = True  # Enable testing mode
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use an in-memory DB
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()  # Create fresh tables before each test
        _populate_db()
        yield app.test_client()  # Return test client
        db.drop_all()  # Clean up database after tests

def _populate_db():
    for i in range(1, 4):
        c = Animals(
            name = f"animal-{i}",
            age = 30 + i
        )
        db.session.add(c)
    db.session.commit()


class TestAnimalsCollection:
    ''' Tests for AnimalsCollection resource '''

    RESOURCE_URL = "/api/animals/"

    def test_get(self, client):
        ''' Test GET method '''

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        #print(body)
        assert len(body) == 3
        assert body[0]["name"] == "animal-1"
        assert body[2]["name"] == "animal-3"

    def test_post(self, client):
        ''' Test POST method '''
        valid = {"name": "animal-4",
                 "age": 5,
                 "picture": ":)",
                 "species": "cat",
                 "environment": "home"
                 }

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data="notjson")
        assert resp.status_code in (400, 415)

        # test with age not being number
        valid["age"] = "twenty"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # test with valid and see that it exists afterward
        valid["age"] = 999
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
        resp = client.get(resp.headers["Location"])
        assert resp.status_code == 200

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove name field for 400
        valid.pop("name")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

class TestAnimalItem():
    ''' Tests for AnimalItem resource '''

    RESOURCE_URL = "/api/animals/animal-1/"
    INVALID_URL = "/api/animals/non-animal/"

    def test_get(self, client):
        ''' Test GET method '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["name"] == "animal-1"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        ''' Test PUT method '''
        valid = {"name": "animal-1",
                 "age": 5,
                 "picture": ":)",
                 "species": "dog",
                 "environment": "garden"
                 }

        # test with wrong content type
        resp = client.put(
            self.RESOURCE_URL,
            data="notjson",
            headers=Headers({"Content-Type": "text"})
            )
        assert resp.status_code in (400, 415)

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with another creature's name
        valid["name"] = "animal-2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # test with valid (only change special force)
        valid["name"] = "animal-1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

    def test_delete(self, client):
        ''' Test DELETE method '''
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
