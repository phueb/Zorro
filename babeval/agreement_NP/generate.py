def get_agreement_across_adjectives(start_words, adjectives_list):
    for start_word in start_words:
        template_3 = start_word + " " + "[MASK]" + " " + "."
        print(template_3, file = open("agreement_across_adjectives.txt","a"))
        for adjective in adjectives_list:
            template_1 = start_word + " " + adjective + " " + "[MASK]" + " " + "."
            # print(template_1, file = open("agreement_across_adjectives.txt","a"))
            list_length = len(adjectives_list)
            for i in range(list_length):
                if adjective != adjectives_list[i]:
                    template_2 = start_word + " " + adjective + " " + adjectives_list[i] + " " + "[MASK]" + " " + "."
                    # print(template_2, file = open("agreement_across_adjectives.txt","a"))

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

def get_agreement_across_RC(nouns_list, pronouns_list, adjectives_list, pronouns_third_person_list):
    for noun in nouns_list:
        for pronoun in pronouns_list:
            for adjective in adjectives_list:
                pronoun_sentence = "the" + " " + noun + " " + "that" + " " + pronoun + " " + "like" + " " + "[MASK]" + " " + adjective + " " + "."
                # print(pronoun_sentence, file = open("agreement_across_RC.txt","a")) 

    for noun in nouns_list:
        for pronoun in pronouns_third_person_list:
            for adjective in adjectives_list:
                pronoun_sentence_third_person = "the" + " " + noun + " " + "that" + " " + pronoun + " " + "likes" + " " + "[MASK]" + " " + adjective + " " + "."
                # print(pronoun_sentence_third_person, file = open("agreement_across_RC.txt","a")) 
