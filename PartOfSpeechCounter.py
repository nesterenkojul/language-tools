from string import punctuation 
import numpy as np
import pandas as pd
from sys import argv
import nltk
nltk.download(['punkt', 'averaged_perceptron_tagger'])


TAGS = {'CC': "conjunction, coordinating", 'CD': "numeral, cardinal", 
        'DT': "determiner", 'EX': "existential there", 
        'IN': "preposition or conjunction, subordinating", 
        'JJ': "adjective or numeral, ordinal", 'JJR': "adjective, comparative", 
        'JJS': "adjective, superlative", 'LS': "list item marker", 
        'MD': "modal auxiliary", 'NN': "noun, common, singular or mass", 
        'NNP': "noun, proper, singular", 'NNS': "noun, common, plural", 
        'PDT': "pre-determiner", 'POS': "genitive marker", 
        'PRP': "pronoun, personal", 'PRP$': "pronoun, possessive", 'RB': "adverb",
        'RBR': "adverb, comparative", 'RBS': "adverb, superlative", 'RP': "particle", 
        'TO': '''"to" as preposition or infinitive marker''', 'UH': "interjection",
        'VB': "verb, base form", 'VBD': "verb, past tense", 
        'VBG': "verb, present participle or gerund", 'VBN': "verb, past participle",
        'VBP': "verb, present tense, not 3rd person singular", 
        'VBZ': "verb, present tense, 3rd person singular", 'WDT': "WH-determiner", 
        'WP': "Wh-pronoun", 'WRB': "Wh-adverb"}


# FUNCTION FORM
"""
def PartOfSpeechCounter(text):
  txt = nltk.word_tokenize(text)
  pos = [y for y in map(lambda x: x[1], nltk.pos_tag(txt)) if y not in punctuation]
  part, count = np.unique(pos, return_counts=True)
  return pd.DataFrame({"tag": part, 
                       "part of speech": map(lambda x: TAGS.get(x, None), part), 
                       "count": count}).sort_values(by="count", ascending=False)
"""


# FROM-CONSOLE FORM

# If text is in a file
"""
file = argv[1]
with open(file, r) as f:
  text = f.read()
"""

text = argv[1]  # If text is a string argument

txt = nltk.word_tokenize(text)
pos = [y for y in map(lambda x: x[1], nltk.pos_tag(txt)) if y not in punctuation]
part, count = np.unique(pos, return_counts=True)
pos_count = pd.DataFrame({"tag": part, 
                       "part of speech": map(lambda x: TAGS.get(x, None), part), 
                       "count": count}).sort_values(by="count", ascending=False)

print(pos_count)

"""
output_name = f"part_of_speech_count_of_{file}.csv"  # if reading from file
"""

output_name = "part_of_speech_count_result.csv" 
pos_count.to_csv(output_name)
