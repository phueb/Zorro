
from zorro import configs
from zorro.agreement_between_neighbors.shared import pre_nominals_plural, pre_nominals_singular

template1 = '{}' + f' {configs.Data.mask_symbol} ' + 'must be here .'
template2 = '{}' + f' {configs.Data.mask_symbol} ' + 'can be here .'


def main():
    """
    example:
    "this <mask> must be here."
    "this <mask> can be here."
    """

    for pre_nominal in pre_nominals_plural + pre_nominals_singular:
        yield template1.format(pre_nominal)
        yield template2.format(pre_nominal)


if __name__ == '__main__':
    for n, s in enumerate(main()):
        print(f'{n:>12,}', s)