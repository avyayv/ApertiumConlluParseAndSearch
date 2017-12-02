import re
import pdb

# We use a revised version of the CoNLL-X format called CoNLL-U. Annotations are encoded in plain text files (UTF-8, using only the LF character as line break, including an LF character at the end of file) with three types of lines:
#
# Word lines containing the annotation of a word/token in 10 fields separated by single tab characters; see below.
# Blank lines marking sentence boundaries.
# Comment lines starting with hash (#).
# Sentences consist of one or more word lines, and word lines contain the following fields:
#
# ID: Word index, integer starting at 1 for each new sentence; may be a range for multiword tokens; may be a decimal number for empty nodes.
# FORM: Word form or punctuation symbol.
# LEMMA: Lemma or stem of word form.
# UPOSTAG: Universal part-of-speech tag.
# XPOSTAG: Language-specific part-of-speech tag; underscore if not available.
# FEATS: List of morphological features from the universal feature inventory or from a defined language-specific extension; underscore if not available.
# HEAD: Head of the current word, which is either a value of ID or zero (0).
# DEPREL: Universal dependency relation to the HEAD (root iff HEAD = 0) or a defined language-specific subtype of one.
# DEPS: Enhanced dependency graph in the form of a list of head-deprel pairs.
# MISC: Any other annotation.

sentences = []
class Word:
    def __init__(self, id, form, lemma, upostag, xpostag, feats, head, deprel, deps, misc):
        self.id = id
        self.form = form
        self.lemma = lemma
        self.upostag = upostag
        self.xpostag = xpostag
        self.feats = feats
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc

class Sentence:
    def __init__(self, words):
        self.words = words
        sentences.append(self)

conllu_file = open("text.txt") #this is where the conllu file name goes.
first = True
for line in conllu_file:
    sentence = 0
    if first:
        sentence = Sentence([])

    first = False
    if line.strip() == "":
        sentence = Sentence([])

    if line[0] != "#" and line.strip() != "" : #check if it's a comment

        line = re.sub(' +',',', line) #removes whitespaces to make it a comma for easy splitting
        array_of_vals = line.strip().split(",") #splits string

        word = Word(array_of_vals[0], array_of_vals[1], array_of_vals[2],
        array_of_vals[3], array_of_vals[4], array_of_vals[5], array_of_vals[6],
        array_of_vals[7], array_of_vals[8], array_of_vals[9]) #create word object

        if word.feats != "_" and word.deps != "_":
            word.feats = dict(e.split('=') for e in word.feats.split('|'))
            word.deps = dict(e.split(':') for e in word.deps.split('|'))
        sentences[-1].words.append(word)



def remove_whitespaces_from_array(user_input):
    for itwo in user_input: #iterate through input
        user_input[user_input.index(itwo)] = itwo.strip() #remove all whitespaces

def remove_char(char, user_input):
    user_input = re.sub(char, '', str(user_input)) #removes the [ and the ]
    return user_input
user_input = input()
for i in sentences:

    #for finding with label(first) and feature(second): use ':[cop, past]'
    #to find with relation: use ';nsubj:POS'
    #for plain searching for word: use '<word'

    if user_input[0] == ":": #this is for the label and feature finder
        user_input = remove_char('[\[\]]', user_input)
        user_input = user_input.split(',') # makes array based on comma

        user_input[0] = remove_char(':', user_input[0]) #remove the :
        remove_whitespaces_from_array(user_input)

        for word in i.words: #itervate through words in this sentence
            right_label = False #is this the right label
            right_feature = False #is this the right feature
            if word.xpostag.lower().strip() == user_input[0].lower().strip():
                right_label = True

            if word.feats != "_":
                for value in word.feats.values():
                    if value.lower().strip() == user_input[1].lower().strip():
                        right_feature = True

            if right_label and right_feature:
                print(word.form)

    elif user_input[0] == ";": #this is for the relation
        correct = False
        user_input = remove_char(';', user_input) #remove the ;

        user_input = user_input.split(":")

        for itwo in user_input: #iterate through input
            user_input[user_input.index(itwo)] = itwo.strip() #remove all whitespaces

        for word in i.words:
            if word.deprel.lower().strip() == user_input[0].lower().strip():
                for dependency in word.deps.keys():
                    for word in i.words:
                        if word.id == dependency and word.upostag.lower() == user_input[1]:
                            correct = True
                            print(word.form)

    elif user_input[0] == "<":
        counter = 0
        user_input = remove_char('<', user_input)
        for word in i.words:
            if word.form.lower().strip() == user_input.lower().strip():
                counter += 1
        print(counter)
