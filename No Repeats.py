import hashlib
import os
from concurrent.futures import ThreadPoolExecutor
import json
import logging
import sys

cwd = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(cwd, 'logs.txt')
duplicates_file = os.path.join(cwd, 'duplicates.txt')
try:
    try:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='w', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logging.info("Logging setup complete.")
        logging.info(f"Logs will be written to: {log_file}")
    except Exception as e:
        print(f"Exception occurred while setting up logging: {e}")
        exit(1)

    settings_path = os.path.join(cwd, 'settings.json')

    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            directory_path = settings.get('directory', '')
    except FileNotFoundError:
        logging.error("settings.json not found.")
        exit(1)
    except json.JSONDecodeError:
        logging.error("Error decoding settings.json.")
        exit(1)

    database_path = os.path.join(cwd, 'database.json')

    if os.path.exists(database_path):
        try:
            with open(database_path, 'r') as f:
                hash_database = json.load(f)
        except json.JSONDecodeError:
            logging.error("Error decoding database.json")
            hash_database = {}
    else:
        hash_database = {}

    if not directory_path:
        logging.error("No directory path found in settings.json.")
    else:
        logging.info(f"Directory to scan: {directory_path}")

        def hash_file(filename):
            """Generate SHA-256 hash of a file."""
            h = hashlib.sha256()
            with open(filename, 'rb') as file:
                while chunk := file.read(8192):
                    h.update(chunk)
            return h.hexdigest()

        def compare_files(directory):
            """Compare files by their hashes."""
            duplicates = []

            def process_file(file):
                logging.info(f"Processing file: {file}")
                file_hash = hash_file(file)
                file_entry = {
                    "dir": os.path.dirname(file),
                    "name": os.path.basename(file)
                }
                unique_key = file_hash

                if unique_key in hash_database:
                    existing_file = hash_database[unique_key]
                    if existing_file['dir'] != file_entry['dir'] or existing_file['name'] != file_entry['name']:
                        logging.info(f"Duplicate found: {file} is a duplicate of {os.path.join(existing_file['dir'], existing_file['name'])}")
                        with open(duplicates_file, 'a') as f:
                            f.write(f"Duplicate found: {file} is a duplicate of {os.path.join(existing_file['dir'], existing_file['name'])}\n")
                        duplicates.append((file, os.path.join(existing_file['dir'], existing_file['name'])))
                else:
                    hash_database[unique_key] = file_entry
                    logging.info(f"Finished processing file: {file}")

            with ThreadPoolExecutor() as executor:
                for root, _, files in os.walk(directory):
                    file_paths = [os.path.join(root, file) for file in files]
                    executor.map(process_file, file_paths)

            return duplicates

        duplicates = compare_files(directory_path)

        if duplicates:
            logging.info("\nDuplicate files found:")
            for duplicate, original in duplicates:
                logging.info(f"{duplicate} is a duplicate of {original}")
        else:
            logging.info("\nNo duplicate files found.")

        try:
            with open(database_path, 'w') as f:
                json.dump(hash_database, f, indent=4)
        except IOError as e:
            logging.error(f"IOError: Unable to write to {database_path}. {e}")

except KeyboardInterrupt:
    logging.warning("Emergency stop triggered. Exiting the program...")
    sys.exit(0)
