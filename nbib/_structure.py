from enum import Enum, auto


class Category(Enum):
    """
        a category represents a class of object that may be contained in a ref
        categories may be hierarchical
    """
    STUDY = auto()
    AUTHOR_LIST = auto()
    AUTHOR = auto()
    AFFILIATION = auto()
    DESCRIPTOR = auto()
    KEYWORD = auto()
    PUBLICATION_TYPE = auto()
    GRANT = auto()

    def list_appendable(self) -> bool:
        """
            tag content of this category may simply be placed in a list
        """
        return self in [Category.GRANT, Category.PUBLICATION_TYPE, Category.KEYWORD, Category.AFFILIATION,
                        Category.AUTHOR_LIST, Category.DESCRIPTOR]

    def attribute_appendable(self) -> bool:
        """
            tag content of this category
        """
        return self in [Category.STUDY, Category.AUTHOR]

    def get_start_tag(self) -> str:
        """
            for tags that occur in sequence (i.e. list & attribute appendable), get the tag that marks the start of a
            new entity. will throw for Enums that aren't both list & attribute appendable
        """
        if self == Category.AUTHOR:
            return 'FAU'

        raise ValueError('Only attribute appendable categories rooted beneath a list appendable have a start tag')

    def get_category_path(self) -> list:
        """
            defines how to navigate to the location to append the next tag of the category
        """
        return _category_to_path[self]

    def get_attribute_name(self) -> str:
        """
            get the attribute name defining this category
        """
        return _category_to_attribute_name[self]


# corresponds to a DFS of the goal structure
_category_to_path = {
    Category.STUDY: tuple(),
    Category.AUTHOR_LIST: (Category.STUDY, ),
    Category.AUTHOR: (Category.STUDY, Category.AUTHOR_LIST),
    Category.AFFILIATION: (Category.STUDY, Category.AUTHOR_LIST, Category.AUTHOR),
    Category.DESCRIPTOR: (Category.STUDY, ),
    Category.KEYWORD: (Category.STUDY, ),
    Category.PUBLICATION_TYPE: (Category.STUDY, ),
    Category.GRANT: (Category.STUDY, )
}

_category_to_attribute_name = {
    Category.STUDY: None,
    Category.AUTHOR_LIST: 'authors',
    Category.AUTHOR: None,
    Category.AFFILIATION: 'affiliations',
    Category.DESCRIPTOR: 'descriptors',
    Category.KEYWORD: 'keywords',
    Category.PUBLICATION_TYPE: 'publication_types',
    Category.GRANT: 'grants',
}