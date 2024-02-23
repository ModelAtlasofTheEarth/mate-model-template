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
