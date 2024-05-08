import json
from ruamel.yaml import YAML
import csv
import os

def create_or_update_json_entry(file_path, keys_path, new_value):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Traverse the nested structure using the keys path
    keys = keys_path.split('.')
    prefix = ""
    current_data = data

    for key in keys[:-1]:
        # Hack to deal with potential of key being "./"
        key = prefix + key
        if key == "":
            prefix = "."
            continue
        else:
            prefix = ""

        if type(current_data) == list:
            # Find the item with @id as the key
            for item in current_data:
                if item.get("@id") == key:
                    current_data = item
        elif key in current_data:
            current_data = current_data[key]
        else:
            print(f"Key '{key}' not found.")
            return None

    # Update value of the entry
    last_key = keys[-1]
    if last_key in current_data:
        if isinstance(current_data[last_key], list):
            current_data[last_key].insert(0, new_value)
        else:
            current_data[last_key] = [new_value, current_data[last_key]]
    else:
        current_data[last_key] = [new_value]

    return data

from ruamel.yaml import YAML

def navigate_and_assign(source, path, value):
    """Navigate through a nested dictionary and assign a value to the specified path."""
    keys = path.split('.')
    for i, key in enumerate(keys[:-1]):
        if key.isdigit():  # If the key is a digit, it's an index for a list
            key = int(key)
            while len(source) <= key:  # Extend the list if necessary
                source.append({})
            source = source[key]
        else:
            if i < len(keys) - 2 and keys[i + 1].isdigit():  # Next key is a digit, so ensure this key leads to a list
                source = source.setdefault(key, [])
            else:  # Otherwise, it leads to a dictionary
                source = source.setdefault(key, {})
    # Assign the value to the final key
    if keys[-1].isdigit():  # If the final key is a digit, it's an index for a list
        key = int(keys[-1])
        while len(source) <= key:  # Extend the list if necessary
            source.append(None)
        source[key] = value
    else:
        source[keys[-1]] = value


def read_yaml_with_header(file_path):
    """
    Read YAML content inside YAML header delimiters '---'
    """

    with open(file_path,'r') as file:
        data = file.read()

    yaml = YAML()
    yaml_content = yaml.load(data.strip('---\n'))

    return yaml_content

def update_csv_content(file_path, field, value):
    # Read the CSV file and update the field value
    updated_rows = []
    field_exists = False
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == field:
                row[1] = value
                field_exists = True
            updated_rows.append(row)

    # If the field does not exist, add a new line
    if not field_exists:
        updated_rows.append([field, value])

    return updated_rows
