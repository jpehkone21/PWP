import requests
import random

BASE_URL = "http://127.0.0.1:5000/api" 

def get_all_quotes():
    url = f"{BASE_URL}/quotes/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        quotes = response.json()
        for id, quote in enumerate(quotes, 1):
            print(f"{id}. {quote['quote']} (Mood: {quote['mood']})")
    except requests.RequestException as e:
        print(f"Error fetching all quotes: {e}")
        
def get_human_quote():
    url = f"{BASE_URL}/humans/<human>/quotes/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        quotes = response.json()
        for name, age, picture, relation, hobby, quote in enumerate(quotes, 1):
            print(f"name: {name}")
            print(f"age: {age}")
            print(f"relation: {relation}")
            print(f"hobby: {hobby}")
            print(f"{picture}")
            print(f"quote: {quote}")
    except requests.RequestException as e:
        print(f"Error fetching all quotes: {e}")
        
def add_human():
    print("\n--- Add New Human ---")
    name = input("Enter name: ").strip()
    age = input("Enter age: ").strip()
    picture = input("Enter ASCII picture: ").strip()
    relation = input("Enter relation (e.g., brother, friend): ").strip()
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

def get_all_humans():
    print("\n--- List of All Humans ---")
    try:
        response = requests.get(f"{BASE_URL}/humans/")
        response.raise_for_status()
        humans = response.json()
        if not humans:
            print("No humans found.")
            return
        for id, human in enumerate(humans, 1):
            print(f"{id}. {human['name']} (Age: {human['age']}, Hobby: {human['hobby']})")
    except requests.RequestException as e:
        print(f"Error: {e}")

def get_single_human():
    print("\n--- Get Specific Human ---")
    name = input("Enter the name of the human: ").strip()
    try:
        response = requests.get(f"{BASE_URL}/humans/{name}")
        if response.status_code == 200:
            human = response.json()
            print(f"Name: {human['name']}")
            print(f"Age: {human.get('age', 'N/A')}")
            print(f"Picture: {human.get('picture', 'N/A')}")
            print(f"Relation: {human.get('relation', 'N/A')}")
            print(f"Hobby: {human.get('hobby', 'N/A')}")
        else:
            print(f"Human '{name}' not found.")
    except requests.RequestException as e:
        print(f"Error: {e}")

def edit_human():
    print("\n--- Edit Human ---")
    name = input("Enter the name of the human to edit: ").strip()

    try:
        # Fetch current data first
        response = requests.get(f"{BASE_URL}/humans/{name}")
        if response.status_code != 200:
            print(f"⚠️ Human '{name}' not found.")
            return
        current = response.json()
        
        print("Leave fields empty to keep current values.")
        age = input(f"Enter new age (current: {current.get('age', '')}): ").strip()
        picture = input(f"Enter new picture (current: {current.get('picture', '')}): ").strip()
        relation = input(f"Enter new relation (current: {current.get('relation', '')}): ").strip()
        hobby = input(f"Enter new hobby (current: {current.get('hobby', '')}): ").strip()

        updated = {
            "name": name,  # name cannot change
            "age": int(age) if age else current.get("age"),
            "picture": picture or current.get("picture"),
            "relation": relation or current.get("relation"),
            "hobby": hobby or current.get("hobby")
        }

        put_response = requests.put(f"{BASE_URL}/humans/{name}", json=updated)
        if put_response.status_code == 204:
            print("Human updated successfully!")
        else:
            print(f"Failed to update: {put_response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")

def delete_human():
    print("\n--- Delete Human ---")
    name = input("Enter the name of the human to delete: ").strip()
    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/humans/{name}")
        if response.status_code == 204:
            print("Human deleted successfully!")
        else:
            print(f"Failed to delete human: {response.text}")
    except requests.RequestException as e:
        print(f"Error: {e}")
                
def main():
    print("Welcome to the Quotes Generator!\n")
    print("You are welcome to choose from options below what you would like to do.\n")
    print("Available options: \n")
    print("----------------------\n")
    print("1: Get all quotes")
    print("2: Get quote from human")
    print("3: Get quote from creature")
    print("4: Get quote from animal \n")
    print("----------------------\n")
    print("5: Add new human and quote")
    print("6: Add new creature and quote")
    print("7: Add new animal and quote \n")
    print("----------------------\n")
    print("8: Edit specific human")
    print("9: Edit specific creature")
    print("10: Edit specific animal \n")
    print("----------------------\n")
    print("11: Delete specific human")
    print("12: Delete specific creature")
    print("13: Delete specific animal \n")
    print("----------------------\n")
    print("14: Exit the program \n")
    
    while True:
        cmd = input("Give a number of the action you want to do: ").strip().lower()
        
        if cmd == '1':
            get_all_quotes()
            
        elif cmd == '2':
            break
        elif cmd == '3':
            break
        elif cmd == '4':
            break
        elif cmd == '5':
            add_human()
            
        elif cmd == '6':
            break
        elif cmd == '7':
            break
        elif cmd == '8':
            edit_human()
            
        elif cmd == '9':
            break
        elif cmd == '10':
            break
        elif cmd == '11':
            delete_human()
            
        elif cmd == '12':
            break
        elif cmd == '13':
            break
        elif cmd == '13':
            break
        elif cmd == '14':
            print("Closing the program...")
            break
        else:
            print("The number was not valid. Try again.")
            break

            
            
if __name__ == "__main__":
    main()