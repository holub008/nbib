import re

from nbib.exceptions import MalformedLine, MalformedSequentialData
from nbib._tags import get_tag_parsers

_LINE_REGEX = r'^([ A-Z]{4})(-| ) (.*)$'


def read_file(path):
    pass


def read(content):
    tag_parsers = get_tag_parsers()
    fp_obj = _first_pass_parse(content, tag_parsers)

    return fp_obj


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
                        ref_write_location.push({})

                # to navigate the list, we simply pick the last (most recent) element
                ref_write_location = ref_write_location[-1]
            # to navigate the dict, we pick out the correct key (attribute)
            elif parent_category.attribute_appendable():
                cat_attribute = cat.get_attribute()
                if cat_attribute not in ref_write_location:
                    if cat.list_appendable():
                        ref_write_location[cat_attribute] = []
                    elif cat.attribute_appendable():
                        ref_write_location[cat_attribute] = {}

                ref_write_location = ref_write_location[cat_attribute]
            else:
                raise ValueError('Categories must be either list or attribute appendable!')
            parent_category = cat

    ##############
    # perform the write
    ##############
    if category.list_appendable():
        ref_write_location.push(parsed_content)
    elif category.attribute_appendable():
        ref_write_location[attribute_name] = parsed_content
    else:
        raise ValueError('Categories must be either list or attribute appendable!')


def _parse_line(line) -> tuple:
    """
        returns tag and tag content, in order
        if the line is a continuation, tag will be None
    """
    match = re.match(_LINE_REGEX, line)
    if match:
        groups = match.groups()
        if groups[1] == '-':
            return groups[0], groups[2]
        else:
            return None, groups[2]

    raise MalformedLine()


def _first_pass_parse(content: str, tag_parsers: dict) -> list:
    """
        in first pass parsing, every tag is mapped to a single attribute of a ref
    """
    lines = content.split('\n')

    refs = []

    current_ref = {}
    # tags are parsed only when the next tag (or end of record) is encountered (to account for multi-line tags)
    # so we keep a running collection of all lines in the tag
    current_tag = None
    current_tag_content = []

    for line in lines:
        if line == '':  # end of record
            _parse_and_place_tag(current_tag, current_tag_content, current_ref, tag_parsers)
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


def _second_pass_parse(refs):
    pass
    # for mesh, we should use a follow up approach. first pass, just dump to string. second pass, structure
    # for authors, use a follow up approach to get first + last names
