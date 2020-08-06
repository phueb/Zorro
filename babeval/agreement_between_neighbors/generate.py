

template = 'look at {} [MASK] .'

pre_nominals = ['this', 'these', 'that', 'those']


def main():
    """
    example:
    "look at this [MASK]"
    """

    for pre_nominal in pre_nominals:
        yield template.format(pre_nominal)
