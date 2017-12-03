import re
import pdb
import argparse

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
        self.none = "none"

    def text_to_attr(self,str):
        if str == "id":
            return self.id
        elif str == "form":
            return self.form
        elif str == "lemma":
            return self.lemma
        elif str == "upostag":
            return self.upostag
        elif str == "xpostag":
            return self.xpostag
        elif str == "feats":
            return self.feats
        elif str == "head":
            return self.head
        elif str == "deprel":
            return self.deprel
        elif str == "deps":
            return self.deps
        elif str == "misc":
            return self.misc
        elif str == "none":
            return self.none



class Sentence:
    def __init__(self, words):
        self.words = words
        sentences.append(self)


parser = argparse.ArgumentParser(description='Parse a conllu file')

parser.add_argument('connlufile', metavar='C', type=file,
                    help='the file to read')
parser.add_argument('search', metavar='S', type=str,
                    help='the searching')
args = parser.parse_args()
first = True
for line in args.connlufile:
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
    for counter,itwo in enumerate(user_input): #iterate through input
        user_input[counter] = itwo.strip() #remove all whitespaces

def remove_char(char, user_input):
    user_input = re.sub(char, '', str(user_input)) #removes the [ and the ]
    return user_input

user_input = args.search

for i in sentences:

    #for finding with label(first) and feature(second): use ':[cop, past]'
    #to find with relation: use ';nsubj:POS'
    #for plain searching for word: use '<word'
    #for searching with tree use '{eat>bread'
    #for more complex searching(i.e you are using arguments) use '{argument=name, argument=name, form=eat>argument=name, form=bread'
    #when searching with ambiguity do '{none=none>form=bread}'

    if user_input[0] == ":": #this is for the label and feature finder
        user_input = remove_char('[\[\]]', user_input)
        user_input = user_input.split(',') # makes array based on comma

        user_input[0] = remove_char(':', user_input[0]) #remove the :
        remove_whitespaces_from_array(user_input)

        for word in i.words: #itervate through words in this sentence
            right_label = False #is this the right label
            right_feature = False #is this the right feature
            if word.upostag.lower().strip() == user_input[0].lower().strip():
                right_label = True

            if word.feats != "_":
                for value in word.feats.values():
                    if value.lower().strip() == user_input[1].lower().strip():
                        right_feature = True

            if right_label and right_feature:
                print(word.form, word.id)

    elif user_input[0] == ";": #this is for the relation
        correct = False
        user_input = remove_char(';', user_input) #remove the ;

        user_input = user_input.split(":")

        for itwo in user_input: #iterate through input
            user_input[user_input.index(itwo)] = itwo.strip() #remove all whitespaces

        for word_two in i.words:

            if word_two.deprel.lower().strip() == user_input[0].lower().strip():
                for word in i.words:
                    if word.id == word_two.head and word.upostag.lower() == user_input[1]:
                        correct = True
                        print(word.form, word.id)

    elif user_input[0] == "<": #search for word
        counter = 0
        user_input = remove_char('<', user_input)
        for word in i.words:
            if word.form.lower().strip() == user_input.lower().strip():
                counter += 1
                print(word.id)
        print(counter)

    elif user_input[0] == "{": #tree
        user_input = remove_char('{', user_input)
        user_input = user_input.split(">")
        user_input[0] = remove_char(">", user_input[0])
        remove_whitespaces_from_array(user_input)

        if not('=' in user_input[0]) and not('=' in user_input[1]):
            for word in i.words:
                for word_two in i.words:
                    if user_input[0].strip().lower() == word.form.strip().lower() and user_input[1].strip().lower() == word_two.form.strip().lower():
                        if word.id == word_two.head:
                            print(word.id)

        else:
            input_one = dict(e.split('=') for e in user_input[0].split(','))
            input_two = dict(e.split('=') for e in user_input[1].split(','))
            # '{argument=name, argument=name, form=eat>argument=name, form=bread'
            # [deprel=root upostag=VERB eat [deprel=obj upostag=NOUN bread]] is represented as
            # '{deprel=root, upostag=Verb, form=eat > deprel=obj, upostag=noun, form=bread}'
            count = 0

            works_one_arr = []
            works_two_arr = []

            for word in i.words:
                works = True
                for n in input_one:

                    if input_one[n].strip().lower() != word.text_to_attr(n.strip()).lower():
                        works = False
                if works:
                    works_one_arr.append(word)

            for word in i.words:
                works = True
                for n in input_two:
                    if input_two[n].strip().lower() != word.text_to_attr(n.strip()).lower():
                        works = False
                if works:

                    works_two_arr.append(word)

            for word in works_one_arr:
                for word_two in works_two_arr:
                    if word.id == word_two.head:
                        print(word.id)
