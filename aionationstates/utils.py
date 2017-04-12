import re


def normalize(identifier):
    identifier = identifier.lower().replace(' ', '_')
    if not re.match('^[a-z0-9_-]+$', identifier):
        raise ValueError(f'provided identifier {identifier} contains invalid'
                          ' characters.')
    return identifier

