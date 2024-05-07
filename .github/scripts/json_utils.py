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
