import dateutil.parser as dup

from nbib.exceptions import UnknownTagFormat
from nbib._structure import Category

import re

NESTED_BRACKET_FORMAT = r'^(.*) \[([a-zA-Z\-]+)\]$'
ISSN_FORMAT = r'^([0-9]{4}\-[0-9]{3}[0-9X]) \(([a-zA-Z]+)\)$'


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


class DateTimeParser(TagParser):
    """
    this class parses well-formatted, complete dates
    """
    def parse(self, lines: list):
        return dup.parse(lines[0])


class IDParser(TagParser):
    """
    a naughty, stateful parser that depends on the parse() call to be made before the get_attribute() call
    """
    def __init__(self):
        super().__init__(Category.STUDY, 'unspecified_id')

    def parse(self, lines):
        content = ''.join(line.lstrip() for line in lines)
        match = re.match(NESTED_BRACKET_FORMAT, content)

        if not match:
            raise UnknownTagFormat(f'For line(s): "{content}"')

        groups = match.groups()
        # technically, we may get name collision this way, but the format is unlikely to change
        # and any additions are unlikely to collide
        self._attribute = groups[1]
        return groups[0]


class ISSNParser(TagParser):
    def __init__(self):
        super().__init__(Category.STUDY, 'unspecified_id')
        self._attribute_prefix = 'unspecified'

    def get_attribute(self) -> str:
        return f'{self._attribute_prefix}_issn'

    def parse(self, lines):
        match = re.match(ISSN_FORMAT, lines[0])

        if not match:
            raise UnknownTagFormat(f'For line: "{lines[0]}"')

        groups = match.groups()
        # technically, we may get name collision this way, but the format is unlikely to change
        # and any additions are unlikely to collide
        self._attribute_prefix = groups[1].lower()
        return groups[0]


class PubMedHistoryParser(TagParser):
    def __init__(self):
        super().__init__(Category.STUDY, 'unspecified_event')

    def parse(self, lines):
        match = re.match(NESTED_BRACKET_FORMAT, lines[0])

        if not match:
            raise UnknownTagFormat(f'For line: "{lines[0]}"')

        groups = match.groups()
        # technically, we may get name collision this way, but the format is unlikely to change
        # and any additions are unlikely to collide
        self._attribute = f"{groups[1]}_time"
        return dup.parse(groups[0])


def get_tag_parsers():
    """
    note: currently, may be stateful, which means a given set of parsers should not be used in parallel

    for a full list: https://pubmed.ncbi.nlm.nih.gov/help/#pubmed-format
    """
    return {
        'AB': TagParser(Category.STUDY, 'abstract'),
        'AD': TagParser(Category.AFFILIATION, 'affiliation'),
        'AID': IDParser(),
        'AU': TagParser(Category.AUTHOR, 'author_abbreviated'),
        # skipping BTI (book title) as irrelevant
        'CI': TagParser(Category.STUDY, 'copyright'),
        # skipping CIN (comment in) since it's information rich + somewhat ambiguous
        'CN': TagParser(Category.STUDY, 'corporate_author'),
        'COIS': TagParser(Category.STUDY, 'conflict_of_interest'),  # note: documentation incorrectly calls this 'COI'
        # skipping CON (comment on)
        # skipping CP (book chapter) as irrelevant
        # skipping CRDT (creation date), since at best is confused with other information
        # skipping CRF (corrected and republished form)
        # skipping CRI (corrected and republished in)
        # skipping CTDT (book contribution date)
        # skipping CTI (collection title)
        # skipping DCOM (nlm completion date) due to near duplication with phst
        # skipping DDIN (dataset described in) no examples found
        # skipping DRIN (dataset use reported in) no examples found
        'DEP': DateTimeParser(Category.STUDY, 'electronic_publication_date'),
        'DP': TagParser(Category.STUDY, 'publication_date'),  # TODO: this is an incomplete date - how to represent?
        # skipping DRDT (book revision date) as irrelevant
        # skipping ECF (expression of concern for) no examples found
        # skipping ECI (expression of concern in) no examples found
        # skipping EDAT (entrez date) duplicated exactly in phst
        # skipping EFR (erratum for) no examples found
        # skipping EIN (erratum in) no examples found
        # skipping ED (book editors) as irrelevant
        # skipping EN (book edition) as irrelevant
        'FAU': TagParser(Category.AUTHOR, 'author'),
        # skipping FED (editors) no examples found
        # skipping FIR (investigator name) no examples found
        # skipping FPS (full personal name as subject) as irrelevant
        # skipping GN (general note) no examples found
        'GR': TagParser(Category.GRANT, 'grant'),
        # skippping GS (gene symbol) as irrelevant
        'IP': TagParser(Category.STUDY, 'journal_issue'),
        # skipping IR (investigator) no examples found
        # skipping IRAD (investigator affiliation) no examples found
        'IS': ISSNParser(),
        # skipping ISBN as irrelevant
        'JID': TagParser(Category.STUDY, 'nlm_journal_id'),  # not an integer because sometimes suffixed with 'R'
        'JT': TagParser(Category.STUDY, 'journal'),
        'LA': TagParser(Category.STUDY, 'language'),
        # skipping LID (location id) as a duplicate of AID
        'LR': DateTimeParser(Category.STUDY, 'last_revision_date'),
        'MH': TagParser(Category.DESCRIPTOR, 'mesh_heading'),
        # skipping MHDA (mesh date) as duplicate of [medline] PHST
        # skipping OAB (other abstract) as irrelevant
        # skipping OABL (other abstract language) as irrelevant
        # skipping OCI (other copyright information) as irrelevant
        # skipping OID (other id) no examples
        # skipping ORI (original report in) no examples
        'OT': TagParser(Category.KEYWORD, 'keyword'),
        # skipping OTO (keyword owner) no examples
        'OWN': TagParser(Category.STUDY, 'citation_owner'),
        # skipping PB as irrelevant
        'PG': TagParser(Category.STUDY, 'pages'),
        'PHST': PubMedHistoryParser(),
        'PL': TagParser(Category.STUDY, 'place_of_publication'),
        # skipping PMCR (pmc released) in favor of exposing the (undocumented) PMC id (if present)
        'PMID': IntParser(Category.STUDY, 'pubmed_id'),
        # skipping PRIN (partial retraction in) no examples
        # skipping PROF (partial retraction of) no examples
        # skipping PS (personal name as subject) no examples
        'PST': TagParser(Category.STUDY, 'publication_status'),
        'PT': TagParser(Category.PUBLICATION_TYPE, 'publication_type'),
        # skipping RF (number of references) no examples
        # skipping RIN (retraction in) no examples
        # skipping RN (EC/RN number) for lack of understanding
        # skipping ROF (retraction of) no examples
        # skipping RPF (republished from) no examples
        # skipping RRI (retracted and republished in) no examples
        # skipping RRF (Retracted and Republished From) no examples
        # skipping SB (Subset) for lack of understanding
        # skipping SFM as no examples / irrelevant
        'SI': TagParser(Category.STUDY, 'secondary_source'),
        # skipping SO (source) as duplicate of a variety of the information already present
        # skipping SPIN (summary for patients in) no examples
        'STAT': TagParser(Category.STUDY, 'nlm_status'),
        'TA': TagParser(Category.STUDY, 'journal_abbreviated'),
        'TI': TagParser(Category.STUDY, 'title'),
        'TT': TagParser(Category.STUDY, 'transliterated_title'),
        # skipping UIN (update in) no examples
        # skipping UOF (update of) no examples
        'VI': TagParser(Category.STUDY, 'journal_volume'),
        # skipping VTI (book volume title) irrelevant
    }
