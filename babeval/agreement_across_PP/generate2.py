def get_agreement_across_PP(prepositions_list, nouns_list, adjectives_list):
    PP_list = []
    for preposition in prepositions_list:
        for noun in nouns_list:
            PP = preposition + ' ' + 'the' + ' ' + noun 
            PP_list.append(PP)

    for noun_1 in nouns_list:
        for PP in PP_list:
            PP = PP.split(' ')
            noun_2 = PP[2]
            complete_PP = " ".join(PP)
            if noun_1 != noun_2:
                for adjective in adjectives_list:
                    agreement_across_PP = 'the' + ' ' + noun_1 + ' ' + complete_PP + ' ' + "[MASK]" + ' ' + adjective + " " + '.'
                    # print(agreement_across_PP, file = open("agreement_across_PP.txt","a"))