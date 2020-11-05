
from zorro.agreement_across_RC.shared import task_name, pronouns_3p, pronouns_1p_2p, adjectives
from zorro import configs

NUM_NOUNS = 4
NUM_ADJECTIVES = 4

# object-relative clause
template1a = 'the {} that {} like' + f' {configs.Data.mask_symbol} ' + '{} .'
template1b = 'the {} that {} likes' + f' {configs.Data.mask_symbol} ' + '{} .'
# subject-relative clause - contains hint about number in relative clause
template2a = 'the {} that is there' + f' {configs.Data.mask_symbol} ' + '{} .'
template2b = 'the {} that are there' + f' {configs.Data.mask_symbol} ' + '{} .'


def main():
    """
    example:
    "the dog that I like [MASK] lazy"
    """

    # object-relative

    for noun in nouns_balanced:
        for pronoun in pronouns_1p_2p:
            for adjective in adjectives_sample:
                yield template1a.format(noun, pronoun, adjective)

    for noun in nouns_balanced:
        for pronoun in pronouns_3p:
            for adjective in adjectives_sample:
                yield template1b.format(noun, pronoun, adjective)

    # subject-relative

    for noun in nouns_sample_singular:
        for adjective in adjectives_sample:
            yield template2a.format(noun, adjective)

    for noun in nouns_sample_plural:
        for adjective in adjectives_sample:
            yield template2b.format(noun, adjective)