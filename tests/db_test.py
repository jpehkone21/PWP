import json
import os
import pytest
import random
import tempfile
import time
from datetime import datetime
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from quotesapi import create_app, db
from quotesapi.models import Creatures, Humans, Animals, Quotes


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()

    yield app

    # Ensure db session is removed before trying to unlink the file
    with app.app_context():
        db.session.remove()  # Make sure to remove the session first
        os.close(db_fd)  # Close the file descriptor
        
    # Delay the unlink to ensure session is completely removed
    time.sleep(0.1)  # Introduce a slight delay to ensure cleanup before file unlink
    try:
        os.unlink(db_fname)  # Delete the temp file
    except PermissionError:
        print(f"Unable to delete file: {db_fname}. It might still be locked.")
'''
def test_quote_one_to_one_relationship(app):
    """
    Tests that a quote can only belong to one entity: either an animal, human, or creature.
    """

    with app.app_context():
        # Create an Animal, Human, and Creature
        animal = Animals(name="Lion", age=5, picture="lion.png", species="Panthera leo", environment="Savanna")
        human = Humans(name="John", age=30, picture="john.png", relation="Engineer", hobby="Reading")
        creature = Creatures(name="Dragon", age=100, picture="dragon.png", type="Fire", special_force="Breath Fire")
        
        db.session.add(animal)
        db.session.add(human)
        db.session.add(creature)
        db.session.commit()  # Commit the entities to the database
        
        # Create a Quote and assign it to the Animal
        quote = Quotes(quote="The Lion roars", mood=0.8, animal_name="Lion")
        db.session.add(quote)
        db.session.commit()  # Commit the Quote

        # Now try to assign the same Quote to both an Animal and a Human (this should raise an IntegrityError)
        quote2 = Quotes(quote="The Lion roars again", mood=0.9, animal_name="Lion", human_name="John")
        db.session.add(quote2)
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()  # Rollback to keep the session clean for further tests
        
        # Test if the Quote can only be associated with a single entity (Creature)
        quote3 = Quotes(quote="The Dragon speaks", mood=0.9, creature_name="Dragon")
        db.session.add(quote3)
        db.session.commit()  # Commit the Quote

        # Verify that the Quote is correctly linked to the Creature
        assert quote3.creature_name == "Dragon"
        assert quote3.human_name is None
        assert quote3.animal_name is None

        db.session.rollback()  # Rollback after test
'''
def _get_creature():
    return Creatures(
        name="Dragon",
        age=500,
        picture="dragon.png",
        type="Fire",
        special_force="Flame Breath"
    )
    
def _get_human():
    return Humans(
        name="John Doe",
        age=30,
        picture="john_doe.png",
        relation="Friend",
        hobby="Reading"
    )
    
def _get_animal():
    return Animals(
        name="Lion",
        age=8,
        picture="lion.png",
        species="Panthera leo",
        environment="Savanna"
    )
    
def test_create_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all relationships have been
    saved correctly.
    """
    with app.app_context():
        # Create everything
        creature = _get_creature()
        human = _get_human()
        animal = _get_animal()
        db.session.add(creature)
        db.session.add(human)
        db.session.add(animal)
        db.session.commit()
        
        # Check that everything exists
        assert Creatures.query.count() == 1
        assert Humans.query.count() == 1
        assert Animals.query.count() == 1
        db_creature = Creatures.query.first()
        db_human = Humans.query.first()
        db_animal = Animals.query.first()
        
'''import os
import pytest
import tempfile
import time
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from sensorhub import create_app, db
from sensorhub.models import Location, Sensor, Deployment, Measurement

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# based on http://flask.pocoo.org/docs/1.0/testing/
# we don't need a client for database testing, just the db handle
@pytest.fixture
def app():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }
    
    app = create_app(config)
    
    with app.app_context():
        db.create_all()
        
    yield app
    
    os.close(db_fd)
    os.unlink(db_fname)

def _get_location(sitename="alpha"):
    return Location(
        name="site-{}".format(sitename),
        latitude=63.3,
        longitude=22.6,
        altitude=24.5,
        description="test site {}".format(sitename)
    )

def _get_sensor(number=1):
    return Sensor(
        name="donkeysensor-{}".format(number),
        model="donkeysensor2000",
    )
    
def _get_measurement():
    return Measurement(
        value=44.51,
        time=datetime.now()
    )
    
def _get_deployment():
    return Deployment(
        start=datetime(2019, 1, 1, 0, 0, 1),
        end=datetime(2020, 1, 1, 0, 0, 0),
        name="test deployment"
    )
    
def test_create_instances(app):
    """
    Tests that we can create one instance of each model and save them to the
    database using valid values for all columns. After creation, test that 
    everything can be found from database, and that all relationships have been
    saved correctly.
    """
    
    with app.app_context():
        # Create everything
        location = _get_location()
        sensor = _get_sensor()
        measurement = _get_measurement()
        deployment = _get_deployment()
        sensor.location = location
        measurement.sensor = sensor
        deployment.sensors.append(sensor)
        db.session.add(location)
        db.session.add(sensor)
        db.session.add(measurement)
        db.session.add(deployment)
        db.session.commit()
        
        # Check that everything exists
        assert Location.query.count() == 1
        assert Sensor.query.count() == 1
        assert Measurement.query.count() == 1
        assert Deployment.query.count() == 1
        db_sensor = Sensor.query.first()
        db_measurement = Measurement.query.first()
        db_location = Location.query.first()
        db_deployment = Deployment.query.first()
        
        # Check all relationships (both sides)
        assert db_measurement.sensor == db_sensor
        assert db_location.sensor == db_sensor
        assert db_sensor.location == db_location
        assert db_sensor in db_deployment.sensors
        assert db_deployment in db_sensor.deployments
        assert db_measurement in db_sensor.measurements    
    
def test_location_sensor_one_to_one(app):
    """
    Tests that the relationship between sensor and location is one-to-one.
    i.e. that we cannot assign the same location for two sensors.
    """
    
    with app.app_context():
        location = _get_location()
        sensor_1 = _get_sensor(1)
        sensor_2 = _get_sensor(2)
        sensor_1.location = location
        sensor_2.location = location
        db.session.add(location)
        db.session.add(sensor_1)
        db.session.add(sensor_2)    
        with pytest.raises(IntegrityError):
            db.session.commit()
        
def test_measurement_ondelete_sensor(app):
    """
    Tests that measurement's sensor foreign key is set to null when the sensor
    is deleted.
    """
    
    with app.app_context():
        measurement = _get_measurement()
        sensor = _get_sensor()
        measurement.sensor = sensor
        db.session.add(measurement)
        db.session.commit()
        db.session.delete(sensor)
        db.session.commit()
        assert measurement.sensor is None
        
def test_location_columns(app):
    """
    Tests the types and restrictions of location columns. Checks that numerical
    values only accepts numbers, name must be present and is unique, and that
    all of the columns are optional. 
    """
    
    with app.app_context():
        location = _get_location()
        location.latitude = str(location.latitude) + "°"
        db.session.add(location)
        with pytest.raises(StatementError):
            db.session.commit()
            
        db.session.rollback()
            
        location = _get_location()
        location.longitude = str(location.longitude) + "°"
        db.session.add(location)
        with pytest.raises(StatementError):
            db.session.commit()
        
        db.session.rollback()

        location = _get_location()
        location.altitude = str(location.altitude) + "m"
        db.session.add(location)
        with pytest.raises(StatementError):
            db.session.commit()
        
        db.session.rollback()
        
        location = _get_location()
        location.name = None
        db.session.add(location)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        location_1 = _get_location()
        location_2 = _get_location()
        db.session.add(location_1)
        db.session.add(location_2)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        location = Location(name="site-test")
        db.session.add(location)
        db.session.commit()
    
def test_sensor_columns(app):
    """
    Tests sensor columns' restrictions. Name must be unique, and name and model
    must be mandatory.
    """

    with app.app_context():
        sensor_1 = _get_sensor()
        sensor_2 = _get_sensor()
        db.session.add(sensor_1)
        db.session.add(sensor_2)    
        with pytest.raises(IntegrityError):
            db.session.commit()

        db.session.rollback()
        
        sensor = _get_sensor()
        sensor.name = None
        db.session.add(sensor)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
        
        sensor = _get_sensor()
        sensor.model = None
        db.session.add(sensor)
        with pytest.raises(IntegrityError):
            db.session.commit()    
    
def test_measurement_columns(app):
    """
    Tests that a measurement value only accepts floating point values and that
    time only accepts datetime values.
    """
    
    with app.app_context():
        measurement = _get_measurement()
        measurement.value = str(measurement.value) + "kg"
        db.session.add(measurement)
        with pytest.raises(StatementError):
            db.session.commit()
            
        db.session.rollback()
        
        measurement = _get_measurement()
        measurement.time = time.time()
        db.session.add(measurement)
        with pytest.raises(StatementError):
            db.session.commit()
    
def test_deployment_columns(app):
    """
    Tests that all columns in the deployment table are mandatory. Also tests
    that start and end only accept datetime values.
    """
    
    with app.app_context():
        # Tests for nullable
        deployment = _get_deployment()
        deployment.start = None
        db.session.add(deployment)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        deployment = _get_deployment()
        deployment.end = None
        db.session.add(deployment)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()

        deployment = _get_deployment()
        deployment.name = None
        db.session.add(deployment)
        with pytest.raises(IntegrityError):
            db.session.commit()
        
        db.session.rollback()
            
        # Tests for column type
        deployment = _get_deployment()
        deployment.start = time.time()
        db.session.add(deployment)
        with pytest.raises(StatementError):
            db.session.commit()
        
        db.session.rollback()
        
        deployment = _get_deployment()
        deployment.end = time.time()
        db.session.add(deployment)
        with pytest.raises(StatementError):
            db.session.commit()
    
        db.session.rollback()'''
