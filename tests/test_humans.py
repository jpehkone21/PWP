import json
import os
import pytest
import tempfile
import time
from datetime import datetime
from flask.testing import FlaskClient
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError
from werkzeug.datastructures import Headers

from quotesapi import create_app, db
from quotesapi.models import Creatures, Animals, Humans, Quotes  

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
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
        c = Humans(
            name = "human-{}".format(i),
            age = 30 + i
        )
        db.session.add(c)     
    db.session.commit()


class TestHumansCollection(object):
    
    RESOURCE_URL = "/api/humans/"

    def test_get(self, client):
        #print("test get humans")
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        #print(body)
        assert len(body) == 3
        assert body[0]["name"] == "human-1"
        assert body[2]["name"] == "human-3"

    def test_post(self, client):
        valid = {"name": "human-4",
                 "age": 30,
                 "picture": ":)",
                 "relation": "neighbour",
                 "hobby": "collecting stamps"
                 }
        
        # test with wrong content type
        resp = client.post(self.RESOURCE_URL, data="notjson")
        assert resp.status_code in (400, 415)
        
        # test with valid and see that it exists afterward
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
          
        
class TestHumanItem(object):
    
    RESOURCE_URL = "/api/humans/human-1/"
    INVALID_URL = "/api/humans/non-human/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["name"] == "human-1"
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404

    def test_put(self, client):
        valid = {"name": "human-1",
                 "age": 30,
                 "picture": ":)",
                 "relation": "neighbour",
                 "hobby": "collecting rocks"
                 }
        
        # test with wrong content type
        resp = client.put(self.RESOURCE_URL, data="notjson", headers=Headers({"Content-Type": "text"}))
        assert resp.status_code in (400, 415)
        
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        # test with another human's name
        valid["name"] = "human-2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        # test with valid
        valid["name"] = "human-1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        # remove field for 400
        valid.pop("name")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
 