import json

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
                if item["@id"] == key:
                    current_data = item
        elif key in current_data:
            current_data = current_data[key]
        else:
            print(f"Key '{key}' not found.")

    # Update value of the entry
    last_key = keys[-1]
    current_data[last_key] = new_value

    return data