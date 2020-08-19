

from babeval.agreement_between_neighbors import *

template = 'look at {} [MASK] .'


def main():
    """
    example:
    "look at this [MASK]"
    """

    for pre_nominal in pre_nominals:
        yield template.format(pre_nominal)
