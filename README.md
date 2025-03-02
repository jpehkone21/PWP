# PWP SPRING 2025
# PROJECT NAME
# Group information
* Student 1. Iina Nikkarikoski inikkari21@student.oulu.fi
* Student 2. Iiris Kivelä ikivela21@student.oulu.fi
* Student 3. Johanna Pehkonen jpehkone21@student.oulu.fi


__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint, instructions on how to setup and run the client, instructions on how to setup and run the axiliary service and instructions on how to deploy the api in a production environment__

# Database (for deadline 2)
This project uses a SQLite database. The database is in quotes_database.db file, and all database models are declared in database.py file. A new database can be created and prepopulated by running the prepopulate_database.py file (remove the existing database before trying to create a new one). The requirements.txt includes all project dependencies so far.

First create/activate python virtual environment

Then install dependencies:
```bash
pip install -r requirements.txt
```

You can create and prepopulate the database by running:
```bash
python prepopulate_database.py
```

# Running API (for deadline 3)
Note: Run all commands from PWP folder

Install dependencies:
```bash
pip install -r requirements.txt
```
To start the API in development mode (on Windows), run 
```bash
set FLASK_APP=quotesapi
set FLASK_ENV=development
flask init-db
flask run
```

API starts running on http://127.0.0.1:5000.

For example these urls should work: 
- http://127.0.0.1:5000/api/creatures/
- http://127.0.0.1:5000/api/humans/
- http://127.0.0.1:5000/api/animals/

# Tests
Tests are located in tests folder.

Run tests with:
```bash
pytest tests/
```

Or with test coverage: 
```bash
pytest --cov-report term --cov=quotesapi tests/
```
