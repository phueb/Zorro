from typing import Tuple, List


def check_agreement_between_pre_nominal_and_noun(s: List[str],
                                                 pre_nominals_singular,
                                                 pre_nominals_plural,
                                                 nouns_singular,
                                                 nouns_plural,
                                                 ) -> bool:
    """
    find two words in sentence which must agree (e.g. "this" and "dog") in single for loop.
    of the three returned objects, only 2 are defined, while the other are of NoneType.
    in theory, this prevents need to search through nouns and pre-nominals again, to determine their number.
    """
    pre_nominal_s1 = None
    pre_nominal_p1 = None
    noun_s1 = None
    noun_p1 = None
    for w_forward, w_backward in zip(s, reversed(s)):
        if pre_nominal_s1 is None and pre_nominal_p1 is None and w_forward in pre_nominals_singular:
            pre_nominal_s1 = w_forward
        elif pre_nominal_s1 is None and pre_nominal_p1 is None and w_forward in pre_nominals_plural:
            pre_nominal_p1 = w_forward
        if noun_s1 is None and noun_p1 is None and w_backward in nouns_singular:
            noun_s1 = w_backward
        elif noun_s1 is None and noun_p1 is None and w_backward in nouns_plural:
            noun_p1 = w_backward

    return True if (pre_nominal_s1 and noun_s1) or (pre_nominal_p1 and noun_p1) else False


def check_agreement_between_subject_and_verb(s: List[str],
                                             subjects_s,
                                             subjects_p,
                                             verbs_s,
                                             verbs_p,
                                             ) -> bool:
    """
    find two words in sentence which must agree (e.g. "dog" and "barks") in single for loop.
    of the three returned objects, only 2 are defined, while the other are of NoneType.
    in theory, this prevents need to search through verbs and subjects again, to determine their number.
    """
    sub_s1 = None
    sub_p2 = None
    verb_s1 = None
    verb_p1 = None
    for w_forward, w_backward in zip(s, reversed(s)):
        if sub_s1 is None and sub_p2 is None and w_forward in subjects_s:
            sub_s1 = w_forward
        elif sub_s1 is None and sub_p2 is None and w_forward in subjects_p:
            sub_p2 = w_forward
        if verb_s1 is None and verb_p1 is None and w_backward in verbs_s:
            verb_s1 = w_backward
        elif verb_s1 is None and verb_p1 is None and w_backward in verbs_p:
            verb_p1 = w_backward

    return True if (sub_s1 and verb_s1) or (sub_p2 and verb_p1) else False