def get_agreement_across_adjectives(start_words, adjectives_list):
    for start_word in start_words:
        template_3 = start_word + " " + "[MASK]" + " " + "."
        print(template_3, file = open("agreement_across_adjectives.txt","a"))
        for adjective in adjectives_list:
            template_1 = start_word + " " + adjective + " " + "[MASK]" + " " + "."
            print(template_1, file = open("agreement_across_adjectives.txt","a"))
            list_length = len(adjectives_list)
            for i in range(list_length):
                if adjective != adjectives_list[i]:
                    template_2 = start_word + " " + adjective + " " + adjectives_list[i] + " " + "[MASK]" + " " + "."
                    # print(template_2, file = open("agreement_across_adjectives.txt","a"))