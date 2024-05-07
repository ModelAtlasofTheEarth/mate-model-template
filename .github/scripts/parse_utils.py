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
