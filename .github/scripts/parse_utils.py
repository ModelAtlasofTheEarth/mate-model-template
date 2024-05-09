import re


def extract_doi_parts(doi_string):
    # Regular expression to match a DOI within a string or URL
    # It looks for a string starting with '10.' followed by any non-whitespace characters
    # and optionally includes common URL prefixes
    # the DOI
    doi_pattern = re.compile(r'(10\.[0-9]+/[^ \s]+)')

    # Search for DOI pattern in the input string
    match = doi_pattern.search(doi_string)

    # If a DOI is found in the string
    if match:
        # Extract the DOI
        doi = match.group(1)

        # Clean up the DOI by removing any trailing characters that are not part of a standard DOI
        # This includes common punctuation and whitespace that might be accidentally included
        #doi = re.sub(r'[\s,.:;]+$', '', doi)
        doi = re.sub(r'[\s,.:;|\/\?:@&=+\$,]+$', '', doi)

        # Split the DOI into prefix and suffix at the first "/"
        #prefix, suffix = doi.split('/', 1)

        return doi
    else:
        # Return an error message if no DOI is found
        return "No valid DOI found in the input string."


def format_citation(ro_crate):
    # Find the root entity (main dataset)
    root_entity = next((item for item in ro_crate['@graph'] if item['@id'] == './'), None)
    if not root_entity:
        return "Error: Root data entity not found."

    # Extract essential data: title, DOI, publication year, publisher
    title = root_entity.get('name', 'No title available')
    doi = root_entity.get('identifier', ['No DOI available'])[0]
    date_published = root_entity.get('datePublished', '')[:4]  # Extract the first four characters, which represent the year
    publisher_entity = next((item for item in ro_crate['@graph'] if item['@id'] == root_entity.get('publisher', {}).get('@id')), None)
    publisher_name = publisher_entity.get('name') if publisher_entity else "No publisher available"

    # Extract and format author names
    authors = root_entity.get('creator', [])
    author_names = []
    for author_id in authors:
        author_entity = next((item for item in ro_crate['@graph'] if item['@id'] == author_id['@id']), None)
        if author_entity:
            surname = author_entity.get('familyName', '')
            given_name_initial = author_entity.get('givenName', '')[0] if author_entity.get('givenName', '') else ''
            author_names.append(f"{surname}, {given_name_initial}.")

    # Join author names with commas, and use '&' before the last author if multiple
    if len(author_names) > 1:
        authors_formatted = ', '.join(author_names[:-1]) + f", & {author_names[-1]}"
    else:
        authors_formatted = ''.join(author_names)

    # Create formatted citation string
    citation = f"{authors_formatted} ({date_published}). {title} [Data set]. {publisher_name}. https://doi.org/{doi.split('/')[-1]}"
    return citation
