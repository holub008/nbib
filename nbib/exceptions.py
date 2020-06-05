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
