from numpy.random import default_rng

file_name_1 = "nouns.txt"
file_name_2 = "adjectives.txt"
file_name_3 = "prepositions.txt"
file_name_4 = "pronouns.txt"
file_name_5 = "pronoun_third_person.txt"
input_directory = "sorted_word_list/"

start_words = ['this', 'these', 'that', 'those']
mask = "[MASK]"

#open and read word_lists
with open(input_directory + file_name_1) as f:
    nouns_list = f.read().lower().split("\n")

with open(input_directory + file_name_2) as f:
    adjectives_list = f.read().lower().split("\n")

with open(input_directory + file_name_3) as f:
    prepositions_list = f.read().lower().split("\n")

with open(input_directory + file_name_4) as f:
    pronouns_list = f.read().lower().split("\n")

with open(input_directory + file_name_5) as f:
    pronouns_third_person_list = f.read().lower().split("\n")

#agreement_across_adjectives: template_1/2/3
for start_word in start_words:
    template_3 = start_word + " " + mask + " " + "."
    # print(template_3, file = open("agreement_across_adjectives.txt","a"))
    for adjective in adjectives_list:
        template_1 = start_word + " " + adjective + " " + mask + " " + "."
        # print(template_1, file = open("agreement_across_adjectives.txt","a"))
        list_length = len(adjectives_list)
        for i in range(list_length):
            if adjective != adjectives_list[i]:
                template_2 = start_word + " " + adjective + " " + adjectives_list[i] + " " + mask + " " + "."
                # print(template_2, file = open("agreement_across_adjectives.txt","a"))

#PP_template
PP_list = []
for preposition in prepositions_list:
    for noun in nouns_list:
        PP = preposition + ' ' + 'the' + ' ' + noun 
        PP_list.append(PP)

#agreement_across_PP
for noun_1 in nouns_list:
    for PP in PP_list:
        PP = PP.split(' ')
        noun_2 = PP[2]
        complete_PP = " ".join(PP)
        if noun_1 != noun_2:
            for adjective in adjectives_list:
                agreement_across_PP = 'the' + ' ' + noun_1 + ' ' + complete_PP + ' ' + mask + ' ' + adjective + " " + '.'
                # print(agreement_across_PP, file = open("agreement_across_PP.txt","a"))

# agreement_across_RC
for noun in nouns_list:
    for pronoun in pronouns_list:
        for adjective in adjectives_list:
            pronoun_sentence = "the" + " " + noun + " " + "that" + " " + pronoun + " " + "like" + " " + mask + " " + adjective + " " + "."
            # print(pronoun_sentence, file = open("agreement_across_RC.txt","a")) 


for noun in nouns_list:
    for pronoun in pronouns_third_person_list:
        for adjective in adjectives_list:
            pronoun_sentence_third_person = "the" + " " + noun + " " + "that" + " " + pronoun + " " + "likes" + " " + mask + " " + adjective + " " + "."
            # print(pronoun_sentence_third_person, file = open("agreement_across_RC.txt","a")) 

# if print random sentences:

with open(file_name) as f:
    lst = f.read().split("\n")

rng = default_rng()
numbers = rng.choice(len(lst), size=2500, replace=False)

for i in numbers:
    print(lst[i], file = open(file_name,"a")) 










