
from zorro import configs
from zorro.agreement_between_neighbors.shared import pre_nominals_plural, pre_nominals_singular

template = 'look at {}' + f' {configs.Data.mask_symbol} ' + '.'


def main():
    """
    example:
    "look at this [MASK]"
    """

    for pre_nominal in pre_nominals_plural + pre_nominals_singular:
        yield template.format(pre_nominal)


if __name__ == '__main__':
    for s in main():
        print(s)