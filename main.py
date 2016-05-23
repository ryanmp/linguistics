
'''

alright, what else did we want to figure out?
analysis tools for Txt() ->
avg_words_per_line, avg_syllables_per_word, word_freqs

we could also add a couple more useful things to our dictionary:

frequencies of most common words ->
then we could get a rating: how much do you use common vs uncommon words

also want to write functions to look for alliteration & rhyming, or to create 
alliterations & rhymes

perhaps we could start with the standard rhyming dictionary function:
given a word... return a list of rhyming words


'''

import string
import ling
from pprint import pprint

d = ling.Dict()


txt1 = ling.Txt('onthewaydown.txt', d)




#find_line_with_stresses('shake.txt', '1111110111')






