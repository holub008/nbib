

def load_file(path):
    pass


def load(content):
    pass


def _process(content):
    lines = content.split('\n')

    refs = []
    current_ref = {}

    authors = []
    current_author = {}


# authors are sequentially demarcated by a new FAU, or a non-author category tag
# for mesh, we should use a follow up approach. first pass, just dump to string. second pass, structure
# for authors, use a follow up approach to get first + last names