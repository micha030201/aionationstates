import re


def normalize(nation):
    nation = nation.lower().replace(' ', '_')
    if not re.match('^[a-z0-9_-]+$', nation):
        raise ValueError('Nation name contains invalid characters.')
    return nation
