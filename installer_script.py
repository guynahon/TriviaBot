import json
from pymongo import MongoClient
import os


def import_json_to_mongodb():
    # Connection to MongoDB
    client = MongoClient()

    # Access or create a database
    db = client['Trivia2']

    # Access or create a collection
    collection = db['Questions']

    user_home = os.path.expanduser('~')
    project_folder_path = input("Please paste the project folder path: ")
    file_path = os.path.join(project_folder_path, 'DB', 'data')

    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Insert data into the collection
    collection.insert_many(data)

    print("Data imported successfully.")


if __name__ == "__main__":
    try:
        # Try to import pymongo; if not installed, install it
        import pymongo
    except ImportError:
        print("pymongo not found. Installing...")
        import subprocess

        subprocess.run(["pip", "install", "pymongo"])

    import_json_to_mongodb()
