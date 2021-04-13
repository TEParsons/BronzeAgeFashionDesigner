import re
from pathlib import Path

# List all valid entry types
VALID_ENTRY_TYPES = [
    "article",
    "book",
    "booklet",
    "conference",
    "inbook",
    "incollection",
    "inproceedings",
    "manual",
    "masterthesis",
    "misc",
    "phdthesis",
    "proceedings",
    "techreport",
    "unpublished",
]
# List all valid fields
VALID_FIELDS = [
    "address",
    "annote",
    "author",
    "booktitle",
    "chapter",
    "doi",
    "edition",
    "author",
    "howpublished",
    "institution",
    "issn",
    "isbn",
    "journal",
    "month",
    "note",
    "number",
    "organization",
    "pages",
    "publisher",
    "school",
    "type",
    "series",
    "title",
    "url",
    "volume",
    "year",
]

# Regex to find entries in .bib file
entry_re = (
    r"(?<!%)" # exclude comments
    r"\@(VALID_ENTRY_TYPES)" # entry type
    r"\{"
    r"[a-zA-Z\d]*" # tag
    r",[\n\s]*"
    r"("
    r"(VALID_FIELDS)" # field name
    r"="
    r"(\{.*\}|\".*\")" # field value
    r",?[\n\s]*)*" # repeat as necessary
    r"[\n\s]*"
    r"\}" # close
)
entry_re = entry_re.replace("VALID_ENTRY_TYPES", "|".join(VALID_ENTRY_TYPES))
entry_re = entry_re.replace("VALID_FIELDS", "|".join(VALID_FIELDS))
entry_re = re.compile(entry_re)

# Regex to find fields/values in entry
values_re = (
    r"(VALID_FIELDS)" # field name
    r"\s*\=\s*"
    r"(\{.*\}|\".*\")" # field value
)
values_re = values_re.replace("VALID_FIELDS", "|".join(VALID_FIELDS))
values_re = re.compile(values_re)

# Regex to find entry type / tag in entry
tags_re = (
    r"(?<=" # positive lookbehind
        r"\@"
    r")"
    r"(VALID_ENTRY_TYPES)" # entry type
    r"\s*\{\s*"
    r"([a-zA-Z\d]*)" # tag
    r"(?="  # positive lookahead
    r",[\n\s]*"
    r")"
)
tags_re = tags_re.replace("VALID_ENTRY_TYPES", "|".join(VALID_ENTRY_TYPES))
tags_re = re.compile(tags_re)


def entry_from_string(string):
    assert isinstance(string, str) and entry_re.fullmatch(string)
    # Get tags
    tags = tags_re.findall(string)
    # Get values as dict
    values = dict(values_re.findall(string))
    # Reformat values
    for key in values:
        # Remove redundant quotation marks
        if re.fullmatch("[\"\'].*[\"\']", values[key]):
            values[key] = values[key][1:-1]
        # Expand bibtex lists
        if re.fullmatch("\{.*\}", values[key]):
            values[key] = values[key].split(",")
        # Expand redundant lists
        if isinstance(values[key], list) and len(values[key]) == 1:
            values[key] = values[key][0]
    # Make object
    obj = BibtexEntry(type=tags[0][0], tag=tags[0][1], values=values)

    return obj


def parse_file(file):
    assert isinstance(file, str) or isinstance(file, Path)
    file = Path(file)
    # Read file
    with open(file) as f:
        content = f.read()
    # Find entries
    entries_iter = entry_re.finditer(content)
    # Convert to string
    entries_str = [e.group(0) for e in entries_iter]
    # Convert to object
    entries_obj = [entry_from_string(e) for e in entries_str]
    # Convert to dict
    entries_dict = {e.tag: e for e in entries_obj}

    return entries_dict


class BibtexEntry:
    def __init__(self, type, tag="", values={}):
        assert isinstance(values, dict)

        # Store input params
        self.type = type
        self.tag = tag
        # Make blank dict of values
        self.values = {key: None for key in VALID_FIELDS}
        # Apply values supplied
        for key in values:
            self[key] = values[key]

    def __getitem__(self, key):
        assert key in self.values

        return self.values[key]

    def __setitem__(self, key, val):
        assert key in VALID_FIELDS

        self.values[key] = val

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        assert val in VALID_ENTRY_TYPES

        self._type = val

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val):
        self._tag = val