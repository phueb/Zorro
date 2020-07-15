

## Nouns

1. Started with words in 4K vocab tagged as noun by NLTK and in English dictionary
2. removed  kinds of words manually:
- gerunds
- quantifiers: lots, some, many, none, plenty, anything, something, anyone, someone, somehow, everybody, everyone, nobody, some, sort, whoever
- number, day, and month words
- greetings: hey, hi, goodbye, hello ...
- interjections: hurrah, hurray, jeez, darn, nope, okay, oh, oops, ow, pardon, phooey, please, aha, psst, sh, shoo, sorry, uh, um, wee, whew, whoa, whoops, whoosh, wow, yuck, yucky, yum, yummy, yo, yep, yeah, achoo, goodness, hurrah, peekaboo, phooey
- onomatopoeia: oink, kaboom, meow, plop, ...
- locations: downstairs, outdoors, someplace, somewhere, wherever
- times: today, tonight, tomorrow, yesterday, sometime, everyday, whenever
3. removed words that are judged as ungrammatical in template



## Singular vs Plural Nouns

1. Started with nouns identified by human annotators
2. Plural nouns were removed manually by American-English native speaker. 
Annotators were given the instruction: "Does the word fit the slot in Look at these _ ?"

## Scoring edge cases:

- Should be scored as correct, but currently is not:

                look                 look
                  at                   at
                that                 that
              smooth               smooth
              [MASK]                 ##ie

                look                 look
                  at                   at
                this                 this
              secret               secret
              [MASK]                  ##s
              
                look                 look
                  at                   at
               those                those
           expensive            expensive
                wild                 wild
             musical              musical
              [MASK]                  ##s
                   .                    .
                   
                look                 look
                  at                   at
               those                those
              stable               stable
              [MASK]                  ##s
                   .                    .  
                   
                look                 look
                  at                   at
               these                these
                dear                 dear
             patient              patient
              [MASK]                  ##s
                   .                    .
                                          