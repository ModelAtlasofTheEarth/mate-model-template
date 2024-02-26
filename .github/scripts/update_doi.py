import os
import io
import re
import json
from ruamel.yaml import YAML
from github import Github, Auth
from request_utils import check_uri
from yaml_utils import *
from json_utils import *

# Environment variables
token = os.environ.get("GITHUB_TOKEN")
repo_name = os.environ.get("REPO_NAME")
issue_number = int(os.environ.get("ISSUE_NUMBER"))

# Get issue
auth = Auth.Token(token)
g = Github(auth=auth)
repo = g.get_repo(repo_name)
issue = repo.get_issue(number = issue_number)

# Parse issue
regex = r"### *(?P<key>.*?)\s*[\r\n]+(?P<value>[\s\S]*?)(?=###|$)"
data = dict(re.findall(regex, issue.body))

doi = data["-> doi"].strip()

# Verify doi is valid
response = check_uri(doi)
if response == "OK":
    # Insert DOI into metadata
    
    # JSON
    json_file_path = "ro-crate-metadata.json"
    key_path = "@graph../.identifier"

    json_data = create_or_update_json_entry(json_file_path, key_path, doi)
    metadata_out = json.dumps(json_data, indent=4)

    file_content = repo.get_contents(json_file_path)
    commit_message = "Update ro-crate with DOI"
    repo.update_file(json_file_path, commit_message, metadata_out, file_content.sha)


    # YAML
    yaml = YAML(typ=['rt', 'string'])
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    # Read existing file
    yaml_file_path = "website_material/index.md"
    web_yaml_dict = read_yaml_with_header(yaml_file_path)

    # Path to key to update
    key_path = "dataset.doi"
    # Update value
    navigate_and_assign(web_yaml_dict, key_path, doi)

    # Use an in-memory text stream to hold the YAML content
    stream = io.StringIO()
    stream.write("---\n")
    yaml.dump(web_yaml_dict, stream)
    stream.write("---\n")
    yaml_content_with_frontmatter = stream.getvalue()

    file_content = repo.get_contents(yaml_file_path)
    commit_message = "Update YAML file with DOI"
    repo.update_file(yaml_file_path, commit_message, yaml_content_with_frontmatter, file_content.sha)

    # Print True to indicate success so that files may be copied to website repo
    print(True)
else:
    issue.create_comment(f"An error was encountered trying to access the DOI provided. Please check that it was entered correctly.\n{response}")
    issue.remove_from_labels("published")
    # Print False to indicate failure so that files are not copied to website repo
    print(False)