"""
Test for the Quotes resource
"""

import json
import pytest
from sqlalchemy.engine import Engine
from sqlalchemy import event
from werkzeug.datastructures import Headers

from quotesapi import create_app, db
from quotesapi.models import Creatures, Animals, Humans, Quotes

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    ''' Connect database'''
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
    a = Animals(
        name = "animal-1",
        age = 10
    )

    h = Humans(
        name = "human-2",
        age = 20
    )

    c = Creatures(
        name = "creature-3",
        age = 30
    )
    db.session.add(a)
    db.session.add(h)
    db.session.add(c)

    q1 = Quotes(
        quote = "testing1",
        mood = 5,
        creatures = c
    )
    q2 = Quotes(
        quote = "testing2",
        mood = 5,
        creatures = c
    )
    db.session.add(q1)
    db.session.add(q2)
    db.session.commit()


class TestQuotesCollection():
    ''' Tests for the QuotesCollection resource'''

    RESOURCE_URL = "/api/creatures/creature-3/quotes/"
    INVALID_URL = "/api/creatures/non-creature/quotes/"
    ANIMAL_URL = "/api/animals/animal-1/quotes/"
    HUMAN_URL = "/api/humans/human-2/quotes/"

    def test_get(self, client):
        ''' Test GET method '''

        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        #print(body)
        assert len(body) == 2

    def test_post(self, client):
        ''' Test POST method '''
        valid = {"quote": "Life is good!",
                 "mood": 8}

        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data="notjson")
        assert resp.status_code in (400, 415)

        # test with mood not being number
        valid["mood"] = "great"
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # test with valid and see that it exists afterward
        valid["mood"] = 8
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        assert len(json.loads(resp.data)) == 3

        # try to add same quote for animal
        resp = client.post(self.ANIMAL_URL, json=valid)
        assert resp.status_code == 409

        #test adding different quote for animal
        valid["quote"] = "animals are great!"
        resp = client.post(self.ANIMAL_URL, json=valid)
        assert resp.status_code == 201
        resp = client.get(self.ANIMAL_URL)
        assert resp.status_code == 200
        assert len(json.loads(resp.data)) == 1

        # test same for human
        valid["quote"] = "humans are great!"
        resp = client.post(self.HUMAN_URL, json=valid)
        assert resp.status_code == 201
        resp = client.get(self.HUMAN_URL)
        assert resp.status_code == 200
        assert len(json.loads(resp.data)) == 1

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        # remove name field for 400
        valid.pop("quote")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestQuoteItem(object):
    ''' Test for WuoteItem resource '''

    RESOURCE_URL = "/api/creatures/creature-3/quotes/1/"
    INVALID_URL = "/api/creatures/creature-3/quotes/non/"

    def test_get(self, client):
        ''' Test GET method '''
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["quote"] == "testing1"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        ''' Test PUT method'''
        valid = {"quote": "different testing",
                 "mood": 2}

        # test with wrong content type
        resp = client.put(
            self.RESOURCE_URL,
            data="notjson",
            headers=Headers({"Content-Type": "text"})
            )
        assert resp.status_code in (400, 415)

        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404

        # test with existing quote
        valid["quote"] = "testing2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        # test with valid
        valid["quote"] = "something different"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204

        # remove field for 400
        valid.pop("quote")
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

        #test to delete creature with quotes (quotes should also be deleted)
        resp = client.delete("/api/creatures/creature-3/")
        assert resp.status_code == 204
        resp = client.get("/api/creatures/creature-3/quotes/2/")
        assert resp.status_code == 404
