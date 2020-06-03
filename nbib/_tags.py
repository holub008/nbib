from nbib._exceptions import UnknownTagFormat

from enum import Enum, auto
import re

ID_FORMAT = r'^(.*) \[([a-zA-Z]+)\]$'

class Category(Enum):
    STUDY = auto()
    AUTHOR = auto()
    AFFILIATION = auto()
    DESCRIPTOR = auto()
    QUALIFIER = auto()
    KEYWORDS = auto()
    PUBLICATION_TYPE = auto()


class TagParser:
    def __init__(self, category: Category, attribute: str):
        self._category = category
        self._attribute = attribute

    def get_category(self) -> Category:
        return self._category

    def get_attribute(self) -> str:
        return self._attribute

    def parse(self, lines: list):
        """

        :param lines: the agglomerated set of lines corresponding to the tag being parsed
        :return:
        """
        # it appears that any space needed will already be present on the preceding line
        # note: it may be a bit faster to strip either 1 or 5 characters (leading spaces) by index instead of stripping
        return ''.join(line.lstrip() for line in lines)


class IntParser(TagParser):
    def parse(self, lines: list):
        return int(lines[0])


class DateParser(TagParser):
    def parse(self, lines: list):
        return


class IDParser(TagParser):
    """
    a naughty, stateful parser that depends on the parse() call to be made before the get_attribute() call
    """
    def __init__(self):
        super().__init__(Category.STUDY, 'unspecified_id')
        self._attribute = 'unspecified_id'

    def get_attribute(self) -> str:
        return self._attribute

    def parse(self, lines):
        match = re.match(ID_FORMAT, lines[0])
        if not match:
            raise UnknownTagFormat()

        groups = match.groups()
        # technically, we may get name collision this way, but the format is unlikely to change
        # and any additions are unlikely to collide
        self._attribute = groups[1]
        return groups[0]

# for a full list: https://pubmed.ncbi.nlm.nih.gov/help/#pubmed-format
tag_meta = {
    'AB': TagParser(Category.STUDY, 'abstract'),
    'AD': TagParser(Category.AFFILIATION, 'affiliation'),
    'AID': IDParser(),
    'AU': TagParser(Category.AUTHOR, 'author_abbreviated'),
    # skipping BTI (book title) as irrelevant
    'CI': TagParser(Category.STUDY, 'copyright'),
    # skipping CIN (comment in) since it's information rich + somewhat ambiguous
    'CN': TagParser(Category.STUDY, 'corporate_author'),
    'COI': TagParser(Category.STUDY, 'conflict_of_interest'),
    # skipping CON (comment on)
    # skipping CP (book chapter) as irrelevant
    # skipping CRDT (creation date), since at best is confused with other information
    # skipping CRF (corrected and republished form)
    # skipping CRI (corrected and republished in)
    # skipping CTDT (book contribution date)
    # skipping CTI (collection title)

}

