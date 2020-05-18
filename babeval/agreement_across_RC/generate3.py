def get_agreement_across_RC(nouns_list, pronouns_list, adjectives_list, pronouns_third_person_list):
    for noun in nouns_list:
        for pronoun in pronouns_list:
            for adjective in adjectives_list:
                pronoun_sentence = "the" + " " + noun + " " + "that" + " " + pronoun + " " + "like" + " " + "[MASK]" + " " + adjective + " " + "."
                print(pronoun_sentence, file = open("agreement_across_RC.txt","a")) 

    for noun in nouns_list:
        for pronoun in pronouns_third_person_list:
            for adjective in adjectives_list:
                pronoun_sentence_third_person = "the" + " " + noun + " " + "that" + " " + pronoun + " " + "likes" + " " + "[MASK]" + " " + adjective + " " + "."
                # print(pronoun_sentence_third_person, file = open("agreement_across_RC.txt","a")) 