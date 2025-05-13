import requests
import random

BASE_URL = "http://127.0.0.1:5000/api" 


"""
Add new quote for a specific character
"""
def add_quote():
    print("\n--- Add Quote ---")
    print("Who is the quote for?")
    print("1: Human")
    print("2: Creature")
    print("3: Animal")

    choice = input("Enter the number: ").strip()
    endpoints = {
        "1": "humans",
        "2": "creatures",
        "3": "animals"
    }

    if choice not in endpoints:
        print("Invalid selection.")
        return

    character_type = endpoints[choice]
    name = input(f"Enter the name of the {character_type[:-1]}: ").strip()
    quote = input("Enter the quote: ").strip()
    mood = input("Enter the mood score (number): ").strip()

    try:
        mood_val = float(mood)
    except ValueError:
        print("Mood must be a number.")
        return

    data = {
        "quote": quote,
        "mood": mood_val
    }

    try:
        response = requests.post(f"{BASE_URL}/{character_type}/{name}/quotes", json=data)
        if response.status_code == 201:
            print("Quote added successfully!")
        elif response.status_code == 409:
            print("Quote already exists.")
        else:
            print(f"Failed to add quote: {response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")


"""
Get all quotes from a specific character
"""
def get_quotes():
    print("\n--- View Quotes ---")
    print("For which character type do you want to see quotes?")
    print("1: Human")
    print("2: Creature")
    print("3: Animal")

    choice = input("Enter the number: ").strip()
    endpoints = {
        "1": "humans",
        "2": "creatures",
        "3": "animals"
    }

    if choice not in endpoints:
        print("Invalid selection.")
        return

    character_type = endpoints[choice]
    name = input(f"Enter the name of the {character_type[:-1]}: ").strip()

    try:
        response = requests.get(f"{BASE_URL}/{character_type}/{name}/quotes")
        if response.status_code == 200:
            quotes = response.json()
            if not quotes:
                print(f"No quotes found for {name}.")
                return
            print(f"\nQuotes for {name}:")
            for i, quote in enumerate(quotes, 1):
                print(f"{i}. \"{quote['quote']}\" (Mood: {quote.get('mood', 'N/A')})")
        else:
            print(f"Failed to retrieve quotes: {response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")


"""
Get all quotes from all characters
"""
def get_all_quotes():
    print("\n--- All Quotes from All Characters ---")

    character_types = {
        "humans": "Human",
        "creatures": "Creature",
        "animals": "Animal"
    }

    for endpoint, label in character_types.items():
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}/")
            response.raise_for_status()
            characters = response.json()

            for character in characters:
                name = character.get("name")
                quote_response = requests.get(f"{BASE_URL}/{endpoint}/{name}/quotes")
                if quote_response.status_code == 200:
                    quotes = quote_response.json()
                    if quotes:
                        print(f"\nQuotes from {label} '{name}':")
                        for i, quote in enumerate(quotes, 1):
                            print(f"  {i}. \"{quote['quote']}\" (Mood: {quote.get('mood', 'N/A')})")
                else:
                    print(f"Failed to get quotes for {name} in {endpoint}: {quote_response.text}")
        except requests.RequestException as e:
            print(f"Error retrieving data from {endpoint}: {e}")

"""
Adds a new creature, human or animal

"""
def add_character():
    character_type = input("What kind of character do you want to add \n " \
    "1: creature, 2: human, 3:animal \n" \
    "Enter the number: ").strip().lower()
    if character_type == '1':
        print("\n--- Add New Creature ---")
        name = input("Enter name: ").strip()
        age = input("Enter age: ").strip()
        picture = input("Enter ASCII picture: ").strip()
        type = input("Enter type (e.g. alien, unicorn): ").strip()
        special_force = input("Enter special force: ").strip()

        data = {
            "name": name,
            "age": int(age),
            "picture": picture,
            "type": type,
            "special_force": special_force
        }

        try:
            response = requests.post(f"{BASE_URL}/creatures/", json=data)
            if response.status_code == 201:
                print("Creature added successfully!")
            elif response.status_code == 409:
                print("Creature already exists.")
            else:
                print(f"Failed to add creature: {response.text}")
        except requests.RequestException as e:
            print(f"Error: {e}")
    if character_type == '2':
        print("\n--- Add New Human ---")
        name = input("Enter name: ").strip()
        age = input("Enter age: ").strip()
        picture = input("Enter ASCII picture: ").strip()
        relation = input("Enter relation (e.g. brother, friend): ").strip()
        hobby = input("Enter hobby: ").strip()

        data = {
            "name": name,
            "age": int(age),
            "picture": picture,
            "relation": relation,
            "hobby": hobby
        }

        try:
            response = requests.post(f"{BASE_URL}/humans/", json=data)
            if response.status_code == 201:
                print("Human added successfully!")
            elif response.status_code == 409:
                print("Human already exists.")
            else:
                print(f"Failed to add human: {response.text}")
        except requests.RequestException as e:
            print(f"Error: {e}")

    if character_type == '3':
        print("\n--- Add New Animal ---")
        name = input("Enter name: ").strip()
        age = input("Enter age: ").strip()
        picture = input("Enter ASCII picture: ").strip()
        species = input("Enter species: ").strip()
        environment = input("Enter environment: ").strip()

        data = {
            "name": name,
            "age": int(age),
            "picture": picture,
            "species": species,
            "environment": environment
        }

        try:
            response = requests.post(f"{BASE_URL}/animals/", json=data)
            if response.status_code == 201:
                print("Animal added successfully!")
            elif response.status_code == 409:
                print("Animal already exists.")
            else:
                print(f"Failed to add animal: {response.text}")
        except requests.RequestException as e:
            print(f"Error: {e}")
    else: 
        print("invalid number")

"""
Get all creatures/humans/animals

"""
def get_all_characters():
    print("\nWhat do you want to view?")
    print("1: All Humans")
    print("2: All Creatures")
    print("3: All Animals")
    print("4: Everything")

    choice = input("Enter the number: ").strip()

    endpoints = {
        "1": ("Humans", "humans"),
        "2": ("Creatures", "creatures"),
        "3": ("Animals", "animals"),
        "4": [
            ("Humans", "humans"),
            ("Creatures", "creatures"),
            ("Animals", "animals")
        ]
    }

    if choice not in endpoints:
        print("Invalid selection.")
        return

    categories = endpoints[choice] if choice == "4" else [endpoints[choice]]

    for category, endpoint in categories:
        print(f"\n--- {category} ---")
        try:
            response = requests.get(f"{BASE_URL}/{endpoint}/")
            response.raise_for_status()
            characters = response.json()
            if not characters:
                print(f"No {category.lower()} found.")
                continue
            for i, char in enumerate(characters, 1):
                if category == "Humans":
                    print(f"{i}. {char['name']} (Age: {char['age']}, Hobby: {char['hobby']})")
                elif category == "Creatures":
                    print(f"{i}. {char['name']} (Age: {char['age']}, Type: {char['type']}, Force: {char['special_force']})")
                elif category == "Animals":
                    print(f"{i}. {char['name']} (Age: {char['age']}, Species: {char['species']}, Environment: {char['environment']})")
        except requests.RequestException as e:
            print(f"Error retrieving {category.lower()}: {e}")


"""
Get a specific character by name
"""
def get_single_character():
    print("\nWhat kind of character do you want to retrieve?")
    print("1: Human")
    print("2: Creature")
    print("3: Animal")

    choice = input("Enter the number: ").strip()
    endpoints = {
        "1": ("Human", "humans"),
        "2": ("Creature", "creatures"),
        "3": ("Animal", "animals")
    }

    if choice not in endpoints:
        print("Invalid selection.")
        return

    category_name, endpoint = endpoints[choice]
    print(f"\n--- Get Specific {category_name} ---")
    name = input(f"Enter the name of the {category_name.lower()}: ").strip()

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}/{name}")
        if response.status_code == 200:
            character = response.json()
            print(f"\nName: {character.get('name', 'N/A')}")
            print(f"Age: {character.get('age', 'N/A')}")
            print(f"Picture: {character.get('picture', 'N/A')}")

            if choice == "1":  # Human
                print(f"Relation: {character.get('relation', 'N/A')}")
                print(f"Hobby: {character.get('hobby', 'N/A')}")
            elif choice == "2":  # Creature
                print(f"Type: {character.get('type', 'N/A')}")
                print(f"Special Force: {character.get('special_force', 'N/A')}")
            elif choice == "3":  # Animal
                print(f"Species: {character.get('species', 'N/A')}")
                print(f"Environment: {character.get('environment', 'N/A')}")
        else:
            print(f"{category_name} '{name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")


"""
Update character details
"""
def edit_character():
    print("\nWhat kind of character do you want to edit?")
    print("1: Human")
    print("2: Creature")
    print("3: Animal")

    choice = input("Enter the number: ").strip()
    endpoints = {
        "1": ("Human", "humans"),
        "2": ("Creature", "creatures"),
        "3": ("Animal", "animals")
    }

    if choice not in endpoints:
        print("Invalid selection.")
        return

    category_name, endpoint = endpoints[choice]
    print(f"\n--- Edit {category_name} ---")
    name = input(f"Enter the name of the {category_name.lower()} to edit: ").strip()

    try:
        # Fetch current data
        response = requests.get(f"{BASE_URL}/{endpoint}/{name}")
        if response.status_code != 200:
            print(f"{category_name} '{name}' not found.")
            return
        current = response.json()

        print("Leave fields empty to keep current values.")
        age = input(f"Enter new age (current: {current.get('age', '')}): ").strip()
        picture = input(f"Enter new picture (current: {current.get('picture', '')}): ").strip()

        updated = {
            "name": name,
            "age": int(age) if age else current.get("age"),
            "picture": picture or current.get("picture"),
        }

        if choice == "1":  # Human
            relation = input(f"Enter new relation (current: {current.get('relation', '')}): ").strip()
            hobby = input(f"Enter new hobby (current: {current.get('hobby', '')}): ").strip()
            updated["relation"] = relation or current.get("relation")
            updated["hobby"] = hobby or current.get("hobby")

        elif choice == "2":  # Creature
            type_ = input(f"Enter new type (current: {current.get('type', '')}): ").strip()
            force = input(f"Enter new special force (current: {current.get('special_force', '')}): ").strip()
            updated["type"] = type_ or current.get("type")
            updated["special_force"] = force or current.get("special_force")

        elif choice == "3":  # Animal
            species = input(f"Enter new species (current: {current.get('species', '')}): ").strip()
            environment = input(f"Enter new environment (current: {current.get('environment', '')}): ").strip()
            updated["species"] = species or current.get("species")
            updated["environment"] = environment or current.get("environment")

        # Send PUT request
        put_response = requests.put(f"{BASE_URL}/{endpoint}/{name}", json=updated)
        if put_response.status_code == 204:
            print(f"{category_name} updated successfully!")
        else:
            print(f"Failed to update: {put_response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")

 
"""
Delete specific character by name
"""
def delete_character():
    print("\nWhat kind of character do you want to delete?")
    print("1: Human")
    print("2: Creature")
    print("3: Animal")

    choice = input("Enter the number: ").strip()
    endpoints = {
        "1": ("Human", "humans"),
        "2": ("Creature", "creatures"),
        "3": ("Animal", "animals")
    }

    if choice not in endpoints:
        print("Invalid selection.")
        return

    category_name, endpoint = endpoints[choice]
    print(f"\n--- Delete {category_name} ---")
    name = input(f"Enter the name of the {category_name.lower()} to delete: ").strip()
    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/{endpoint}/{name}")
        if response.status_code == 204:
            print(f"{category_name} deleted successfully!")
        else:
            print(f"Failed to delete {category_name.lower()}: {response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")



def main():
    print("Welcome to the Quotes Generator!\n")
    print("You are welcome to choose from options below what you would like to do.\n")
    print("Available options: \n")
    print("----------------------\n")
    print("1: Get all quotes from all characters")
    print("2: Get quotes from one character")
    print("3: Add a quote for character")
    print("----------------------\n")
    print("4: Add new character")
    print("5: View all characters")
    print("6: View specific character")    
    print("----------------------\n")
    print("7: Edit specific character")
    print("8: Delete specific character")
    print("----------------------\n")
    print("x: Exit the program \n")
    
    while True:
        cmd = input("Give a number of the action you want to do: ").strip().lower()
        
        if cmd == '1':
            get_all_quotes()
        elif cmd == '2':
            get_quotes()
        elif cmd == '3':
            add_quote()


        elif cmd == '4':
            add_character()
        elif cmd == '5':
            get_all_characters()
        elif cmd == '6':
            get_single_character()

        elif cmd == '7':
            edit_character()
        elif cmd == '8':
            delete_character()

        elif cmd == 'x':
            print("Closing the program...")
            break
        else:
            print("The number was not valid. Try again.")
            break

            
            
if __name__ == "__main__":
    main()