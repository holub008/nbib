import re
from typing import Dict, List

from nbib.exceptions import MalformedLine
from nbib._tags import get_tag_parsers

_LINE_REGEX = r'^([ A-Z]{4})(-| ) (.*)$'


def read_file(path: str):
    """
        Read nbib formated references from a file

        :param path: an nbib formatted file
        :return: a list of parsed references. references contain a variety of attributes structured according to the _tags and _structure submodules

        :raises MalformedLine: when a line does match required structure
        :raises UnknownTagFormat: when a tag value with structured data doesn't follow expected format
    """
    with open(path, mode='r') as f:
        return read(f.read())


def read(content: str) -> List[Dict]:
    """
        Read nbib formated references from a string

        :param content: an nbib formatted string
        :return: a list of parsed references. references contain a variety of attributes structured according to the _tags and _structure submodules

        :raises MalformedLine: when a line does match required structure
        :raises UnknownTagFormat: when a tag value with structured data doesn't follow expected format
    """
    tag_parsers = get_tag_parsers()
    fp_refs = _first_pass_parse(content, tag_parsers)
    sp_refs = _second_pass_parse(fp_refs)

    return sp_refs


def _parse_and_place_tag(current_tag: str, current_tag_content: list, current_ref: dict, tag_parsers: dict):
    parser = tag_parsers.get(current_tag, None)
    # an exception may be right in some cases, but our tag mapping currently isn't broad enough to except
    if not parser:
        return

    ##############
    # parse the incoming tag
    ##############

    parsed_content = parser.parse(current_tag_content)
    attribute_name = parser.get_attribute()

    category = parser.get_category()

    ##############
    # advance in the ref to the desired write location, creating objects along the way as needed
    ##############
    ref_write_location = current_ref
    category_path = category.get_category_path()
    if len(category_path) > 0:
        parent_category = category_path[0]
        if len(category_path) > 1:
            navigation = category_path[1:] + (category, )
        else:
            navigation = (category, )

        for ix, cat in enumerate(navigation):
            if parent_category.list_appendable():
                # case: the leaf category is for sequential tags (i.e. attribute appendable rooted beneath list
                # appendable) and we've reached a new start tag. create a new entry
                if ix == len(navigation) - 1:
                    if cat.attribute_appendable() and cat.get_start_tag() == current_tag:
                        ref_write_location.append({})

                # to navigate the list, we simply pick the last (most recent) element
                # if the list is empty, a tag is unexpectedly located. this can happen (e.g. affiliation being used for
                # an entire study & for individual authors). we can either throw or drop it :/
                if len(ref_write_location) == 0:
                    return
                ref_write_location = ref_write_location[-1]
            # to navigate the dict, we pick out the correct key (attribute)
            elif parent_category.attribute_appendable():
                cat_attribute = cat.get_attribute_name()
                if cat_attribute not in ref_write_location:
                    if cat.list_appendable():
                        ref_write_location[cat_attribute] = []
                    elif cat.attribute_appendable():
                        ref_write_location[cat_attribute] = {}
                    else:
                        raise ValueError('Categories must be either list or attribute appendable!')

                ref_write_location = ref_write_location[cat_attribute]
            else:
                raise ValueError('Categories must be either list or attribute appendable!')
            parent_category = cat

    ##############
    # perform the write
    ##############
    if category.list_appendable():
        ref_write_location.append(parsed_content)
    elif category.attribute_appendable():
        ref_write_location[attribute_name] = parsed_content
    else:
        raise ValueError('Categories must be either list or attribute appendable!')


def _parse_line(line: str) -> tuple:
    """
        returns tag and tag content, in order
        if the line is a continuation, tag will be None
    """
    match = re.match(_LINE_REGEX, line)
    if match:
        groups = match.groups()
        if groups[1] == '-':
            return groups[0].rstrip(), groups[2]
        else:
            return None, groups[2]

    raise MalformedLine(f'For line: "{line}"')


def _first_pass_parse(content: str, tag_parsers: dict) -> list:
    """
        in first pass parsing, every tag is mapped to a single attribute of a ref
    """
    # handle both LF and CRLF terminated files
    # there is probably a better way to do this, but splitlines() is off the table since CR may be embedded in tag
    # content (in several examples I found)
    lines = [x.rstrip('\r') for x in content.split('\n')]

    refs = []

    current_ref = {}
    # tags are parsed only when the next tag (or end of record) is encountered (to account for multi-line tags)
    # so we keep a running collection of all lines in the tag
    current_tag = None
    current_tag_content = []

    for line in lines:
        if line == '':  # end of record
            _parse_and_place_tag(current_tag, current_tag_content, current_ref, tag_parsers)
            # filter end of file (which technically starts a new entry with two newlines) and otherwise empty refs
            if not current_ref == {}:
                refs.append(current_ref)
                current_ref = {}
            current_tag_content = []
            current_tag = None
        else:
            next_tag, next_tag_content = _parse_line(line)

            if next_tag:
                _parse_and_place_tag(current_tag, current_tag_content, current_ref, tag_parsers)
                current_tag = next_tag
                current_tag_content = [next_tag_content]
            else:
                current_tag_content.append(next_tag_content)

    return refs


def _second_pass_parse(refs: list) -> list:
    """
        in second pass parsing, parsed attributes are exploded to new attributes
        these are currently hardcodes that depend on some characteristics of the structure module
    """
    for ref in refs:
        # expand MeSH heading strings into descriptor, qualifier (optional) pairs
        if 'descriptors' in ref:
            new_descriptors = []
            for raw_descriptor in ref['descriptors']:
                headings = [h for h in raw_descriptor.split('/')]
                descriptor = headings[0]
                if len(headings) > 1:
                    for qualifier in headings[1:]:
                        new_descriptors.append({
                            'descriptor': descriptor.lstrip('*'),
                            'qualifier': qualifier.lstrip('*'),
                            'major': qualifier.startswith('*') or descriptor.startswith('*')
                        })
                else:
                    new_descriptors.append({'descriptor': descriptor.lstrip('*'), 'major': descriptor.startswith('*')})
            ref['descriptors'] = new_descriptors

        if 'authors' in ref:
            for auth in ref['authors']:
                name = auth['author']
                name_parts = [n.strip() for n in name.split(',')]
                # it looks like PubMed almost always spits out a last, first pair.
                # if that structure is violated, just skip it
                if len(name_parts) == 2:
                    # leave the rest of the name attributes in :/
                    auth['first_name'] = name_parts[1]
                    auth['last_name'] = name_parts[0]

    return refs
