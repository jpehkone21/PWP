import os
from sqlite3 import IntegrityError
from urllib import request
from flask import Flask, jsonify, request
from database import db, Quotes, Creatures, Humans, Animals

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quotes_database.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Get all quotes, prepopulated and added ones
@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    # Fetch all quotes from the database
    quotes = Quotes.query.all()
    
    quotes_list = [
        {
            'quote': quote.quote,
            'mood': quote.mood,
            'owner_name': (
                quote.creature_name if quote.creature_name else
                quote.human_name if quote.human_name else
                quote.animal_name if quote.animal_name else
                'Unknown'
            )
        }
        for quote in quotes
    ]
    
    return jsonify({'quotes': quotes_list})

# Get all quotes from creatures
@app.route('/api/creatures/quotes', methods=['GET'])
def get_characters_quotes():
    quotes = Quotes.query.filter(Quotes.creature_name.isnot(None)).all()
    
    quotes_list = [
        {
            'quote': quote.quote,
            'mood': quote.mood,
            'owner_name': quote.creature_name
        }
        for quote in quotes
    ]
    
    return jsonify({'quotes': quotes_list})

# Get all quotes from humans
@app.route('/api/humans/quotes', methods=['GET'])
def get_humans_quotes():
    quotes = Quotes.query.filter(Quotes.human_name.isnot(None)).all()
    
    quotes_list = [
        {
            'quote': quote.quote,
            'mood': quote.mood,
            'owner_name': quote.human_name
        }
        for quote in quotes
    ]
    
    return jsonify({'quotes': quotes_list})

# Get all quotes from animals
@app.route('/api/animals/quotes', methods=['GET'])
def get_animals_quotes():
    quotes = Quotes.query.filter(Quotes.animal_name.isnot(None)).all()
    
    quotes_list = [
        {
            'quote': quote.quote,
            'mood': quote.mood,
            'owner_name': quote.animal_name
        }
        for quote in quotes
    ]
    
    return jsonify({'quotes': quotes_list})

# Add a quote under an existing character
@app.route('/api/quotes', methods=['POST'])
def add_quote():
    data = request.get_json()
    
    entity_type = data.get('entity_type')
    entity_name = data.get('name')
    quote_text = data.get('quote')
    mood = data.get('mood')

    if entity_type not in ['creature', 'human', 'animal']:
        return jsonify({'message': 'Invalid entity type. Must be "creature", "human", or "animal".'}), 400
    
    if entity_type == 'creature':
        entity = Creatures.query.filter_by(name=entity_name).first()
    elif entity_type == 'human':
        entity = Humans.query.filter_by(name=entity_name).first()
    elif entity_type == 'animal':
        entity = Animals.query.filter_by(name=entity_name).first()
    
    if not entity:
        return jsonify({'message': f'{entity_type.capitalize()} with the name "{entity_name}" does not exist!'}), 404

    # Check if the entity already has a quote
    existing_quote = None
    if entity_type == 'creature':
        existing_quote = Quotes.query.filter_by(creature_name=entity_name).first()
    elif entity_type == 'human':
        existing_quote = Quotes.query.filter_by(human_name=entity_name).first()
    elif entity_type == 'animal':
        existing_quote = Quotes.query.filter_by(animal_name=entity_name).first()

    if existing_quote:
        return jsonify({'message': f"This {entity_type} already has a quote!"}), 400

    new_quote = Quotes(
        quote=quote_text,
        mood=mood
    )

    if entity_type == 'creature':
        new_quote.creature_name = entity_name
    elif entity_type == 'human':
        new_quote.human_name = entity_name
    elif entity_type == 'animal':
        new_quote.animal_name = entity_name

    db.session.add(new_quote)
    db.session.commit()

    return jsonify({'message': f"Quote added to {entity_type.capitalize()} '{entity_name}' successfully!"}), 201

# Get all characters (creatures, humans, and animals)
@app.route('/api/characters', methods=['GET'])
def get_all_characters():
    creatures = Creatures.query.all()
    humans = Humans.query.all()
    animals = Animals.query.all()

    creatures_list = [
        {
            'id': creature.id,
            'name': creature.name,
            'age': creature.age,
            'type': creature.type,
            'special_force': creature.special_force,
            'picture': creature.picture
        }
        for creature in creatures
    ]

    humans_list = [
        {
            'id': human.id,
            'name': human.name,
            'age': human.age,
            'relation': human.relation,
            'hobby': human.hobby,
            'picture': human.picture
        }
        for human in humans
    ]

    animals_list = [
        {
            'id': animal.id,
            'name': animal.name,
            'age': animal.age,
            'species': animal.species,
            'environment': animal.environment,
            'picture': animal.picture
        }
        for animal in animals
    ]

    return jsonify({
        'creatures': creatures_list,
        'humans': humans_list,
        'animals': animals_list
    })

# Get all creatures
@app.route('/api/creatures', methods=['GET'])
def get_creatures():
    # Fetch all creatures from the database
    creatures = Creatures.query.all()
    creatures_list = [
        {
            'id': creature.id,
            'name': creature.name,
            'age': creature.age,
            'type': creature.type,
            'special_force': creature.special_force,
            'picture': creature.picture
        }
        for creature in creatures
    ]
    return jsonify({'creatures': creatures_list})

# Get all humans
@app.route('/api/humans', methods=['GET'])
def get_humans():
    humans = Humans.query.all()
    humans_list = [
        {
            'id': human.id,
            'name': human.name,
            'age': human.age,
            'relation': human.relation,
            'hobby': human.hobby,
            'picture': human.picture
        }
        for human in humans
    ]
    return jsonify({'creatures': humans_list})

# Get all animals
@app.route('/api/animals', methods=['GET'])
def get_animals():
    animals = Animals.query.all()
    animals_list = [
        {
            'id': animal.id,
            'name': animal.name,
            'age': animal.age,
            'species': animal.species,
            'environment': animal.environment,
            'picture': animal.picture
        }
        for animal in animals
    ]
    return jsonify({'creatures': animals_list})

# Post a new creature
@app.route('/api/creatures', methods=['POST'])
def create_creature():
    # Get the JSON data from the request
    data = request.get_json()
    
    if not data.get('name') or not data.get('type'):
        return jsonify({'message': 'Missing required fields (name, type)'}), 400
    
    new_creature = Creatures(
        name=data['name'],
        age=data.get('age'), 
        type=data['type'],
        special_force=data.get('special_force'),  
        picture=data.get('picture') 
    )

    try:
        # Add the new creature to the session and commit it
        db.session.add(new_creature)
        db.session.commit()
        
        return jsonify({
            'message': 'Creature created successfully!',
            'creature': {
                'id': new_creature.id,
                'name': new_creature.name,
                'age': new_creature.age,
                'type': new_creature.type,
                'special_force': new_creature.special_force,
                'picture': new_creature.picture
            }
        }), 201
    except IntegrityError:
        db.session.rollback() 
        return jsonify({'message': 'Creature already exists with that name.'}), 409
    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': str(e)}), 500
    
# Post a new animal
@app.route('/api/animals', methods=['POST'])
def create_animal():
    # Get the JSON data from the request
    data = request.get_json()
    
    if not data.get('name') or not data.get('species'):
        return jsonify({'message': 'Missing required fields (name, species)'}), 400
    
    new_animal = Animals(
        name=data['name'],
        age=data.get('age'), 
        species=data['species'],
        environment=data.get('environment'),
        picture=data.get('picture') 
    )

    try:
        # Add the new animal to the session and commit it
        db.session.add(new_animal)
        db.session.commit()
        
        return jsonify({
            'message': 'Animal created successfully!',
            'animal': {
                'id': new_animal.id,
                'name': new_animal.name,
                'age': new_animal.age,
                'species': new_animal.species,
                'environment': new_animal.environment,
                'picture': new_animal.picture
            }
        }), 201
    except IntegrityError:
        db.session.rollback() 
        return jsonify({'message': 'Animal already exists with that name.'}), 409
    except Exception as e:
        db.session.rollback() 
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
