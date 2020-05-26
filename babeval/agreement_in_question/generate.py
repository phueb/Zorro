def main(nouns_list):
    for noun in nouns_list:
        sentence_1 = "where" + " " + "[MASK]" + " " + "the" + " " + noun + " " + "go" + " " + "?"
        print(sentence_1, file = open("agreement_in_question.txt","a"))
        sentence_2 = "where" + " " + "[MASK]" + " " + "the" + " " + noun + " " + "?"
        print(sentence_2, file = open("agreement_in_question.txt","a"))