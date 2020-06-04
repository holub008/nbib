class UnknownTagFormat(Exception):
    """
        occurs when a tag's contents violate expected format
    """
    pass


class MalformedLine(Exception):
    """
        occurs when an nbib line doesn't conform to the standard {Tag|spaces}-value format
    """
    pass


class MalformedSequentialData(Exception):
    """
        occurs when a tag that should be sequentially "beneath" another tag is above it
        for example, author affiliations occurring before the author name (FAU)
    """
    pass
