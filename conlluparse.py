#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import pdb
import argparse
import string
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
    def print_info(self):
        return "Token: "+self.id+", Form: "+self.form+", Lemma: "+ self.lemma+", UPOSTAG: "+self.upostag+ ", HEAD: "+self.head+", DEPREL: "+self.deprel + ", "

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
        elif str == "@rel":
            return self.deprel
        elif str == "deps":
            return self.deps
        elif str == "misc":
            return self.misc
        elif str == "none":
            return self.none
    def compare(self,word,number,word_two):
        if number == 0:
            return self.upostag.lower().strip() == word.lower().strip() or self.deprel.lower().strip() == word.lower().strip()
        elif number == 1:
            return self.id == word_two.head and (compare_without_caps(self.upostag, word) or compare_without_caps(self.deprel, word) or compare_without_caps(self.form, word) or compare_without_caps(self.lemma, word))


class Sentence:
    def __init__(self, words, id_name):
        self.words = words
        self.id_name = id_name
        sentences.append(self)
    def print_sentence(self):
        word = ", Sentence: "
        for i in self.words:
            word = word+" "+i.form
        return word


parser = argparse.ArgumentParser(description="""
        Use This Link For Documentation
        http://wiki.apertium.org/wiki/Conllu_Parsing_and_Searching#Example_Of_How_To_Use_This_Program
        """)

parser.add_argument('connlufile', metavar='connlufilename', type=open,
                    help='the file to read i.e. \'text.txt\'')
parser.add_argument('search', metavar='searchterms', type=str,
                    help="Please see above for how to use searching"

                    )
def inequality(user_input):
    local_input = user_input
    input_one = dict(e.split('=') for e in local_input.split(','))
    works_one_arr = []
    for word in i.words:
        works_l = True
        for no in input_one:
            if compare_without_caps(input_one[no], word.text_to_attr(no.strip())) == False:
                works_l = False
        if works_l:
            print(word.print_info()+sentences[overall_counter].id_name+sentences[overall_counter].print_sentence())
            works_one_arr.append(word)



args = parser.parse_args()
first = True

for line in args.connlufile:
    if first:
        sentence = Sentence([], "")

    first = False
    if line.strip() == "":
        sentence = Sentence([], "")

    if line[0] == "#" and line.strip()[2] == "s":
        line = line.replace("\t", "")
        line = line.replace("\n", "")
        sentences[-1].id_name = line

    if line[0] != "#" and line.strip() != "" : #check if it's not a comment
        line = line.replace("\t", " ")
        line = line.replace("\n", "")

        line = re.sub(' +',',', line) #removes whitespaces to make it a comma for easy splitting
        array_of_vals = line.strip().split(",") #splits string
        word = Word(array_of_vals[0], array_of_vals[1], array_of_vals[2],
        array_of_vals[3], array_of_vals[4], array_of_vals[5], array_of_vals[6],
        array_of_vals[7], array_of_vals[8], array_of_vals[9]) #create word object

        if word.feats != "_" and len(word.feats.split('|'))>1:
            try:
                word.feats = dict(e.split('=') for e in word.feats.split('|'))
            except ValueError:
                continue
        sentences[-1].words.append(word)


def find_string(text):
  matches=re.findall(r'\"(.+?)\"',text)
  return matches[0]

def remove_whitespaces_from_array(user_input):
    for counter,itwo in enumerate(user_input): #iterate through input
        user_input[counter] = itwo.strip() #remove all whitespaces

def remove_char(char, user_input):
    user_input = re.sub(char, '', str(user_input)) #removes the [ and the ]
    return user_input

def compare_without_caps(word_one, word_two):
    if word_one.strip().lower() == word_two.strip().lower():
        return True
    else:
        return False


user_input = args.search



def tree(user_input):
    local_input = user_input
    if ">" in local_input:
        local_input = local_input.split(">")
        local_input[0] = remove_char(">", local_input[0])
        remove_whitespaces_from_array(local_input)
        if not('=' in local_input[0]) and not('=' in local_input[1]):
            for word in i.words:
                for word_two in i.words:
                    if compare_without_caps(local_input[0], word.form) and compare_without_caps(local_input[1], word_two.form.strip().lower()):
                        if word.id == word_two.head:

                            print(word.print_info()+sentences[overall_counter].id_name+sentences[overall_counter].print_sentence())
        else:
            input_one = dict(e.split('=') for e in local_input[0].split(','))
            input_two = dict(e.split('=') for e in local_input[1].split(','))
            # '{argument=name, argument=name, form=eat>argument=name, form=bread'
            # [deprel=root upostag=VERB eat [deprel=obj upostag=NOUN bread]] is represented as
            # '{deprel=root, upostag=Verb, form=eat > deprel=obj, upostag=noun, form=bread}'
            works_one_arr = []
            works_two_arr = []
            for word in i.words:
                works = True
                for n in input_one:
                    if compare_without_caps(input_one[n], word.text_to_attr(n.strip())) == False:
                        works = False
                if works:
                    works_one_arr.append(word)
            for word in i.words:
                works = True
                for n in input_two:
                    if compare_without_caps(input_two[n], word.text_to_attr(n.strip())) == False:
                        works = False
                if works:
                    works_two_arr.append(word)
            for word in works_one_arr:
                for word_two in works_two_arr:
                    if word.id == word_two.head:

                        print(word.print_info()+sentences[overall_counter].id_name+sentences[overall_counter].print_sentence())
    elif "<" in local_input:

        local_input = local_input.split("<")
        local_input[0] = remove_char("<", local_input[0])
        remove_whitespaces_from_array(local_input)
        if not('=' in local_input[1]) and not('=' in local_input[0]):
            wor = []
            for word_two in i.words:
                for word in i.words:
                    if compare_without_caps(local_input[1], word.form) and compare_without_caps(local_input[0], word_two.form.strip().lower()):
                        if word.id == word_two.head:
                            if not word in wor:
                                wor.append(word)
            for w in wor:
                print(word_two.print_info()+sentences[overall_counter].id_name+sentences[overall_counter].print_sentence())
        else:
            input_one = dict(e.split('=') for e in local_input[0].split(','))
            input_two = dict(e.split('=') for e in local_input[1].split(','))
            # '{argument=name, argument=name, form=eat>argument=name, form=bread'
            # [deprel=root upostag=VERB eat [deprel=obj upostag=NOUN bread]] is represented as
            # '{deprel=root, upostag=Verb, form=eat > deprel=obj, upostag=noun, form=bread}'
            count = 0
            wor = []
            works_one_arr = []
            works_two_arr = []
            for word in i.words:
                works = True
                for n in input_one:
                    if compare_without_caps(input_one[n], word.text_to_attr(n.strip())) == False:
                        works = False
                if works:
                    count = count+1
                    works_one_arr.append(word)

            for word in i.words:
                works = True
                for n in input_two:
                    if compare_without_caps(input_two[n], word.text_to_attr(n.strip())) == False:
                        works = False
                if works:
                    works_two_arr.append(word)
            for word in works_one_arr:
                for word_two in works_two_arr:
                    if word.id == word_two.head:
                        if not word in wor:
                            wor.append(word)
            for w in wor:
                print(word.print_info()+sentences[overall_counter].id_name+sentences[overall_counter].print_sentence())

#                print(word.print_info()+sentences[overall_counter].id_name+sentences[overall_counter].print_sentence())
    else:

        inequality(user_input)

for overall_counter, i in enumerate(sentences):
    #for finding with label(first) and feature(second): use ':[cop, past]'
    #to find with relation: use ';nsubj:POS'
    #for plain searching for word: use '<word'
    #for searching with tree use '{eat>bread'
    #for more complex searching(i.e you are using arguments) use '{argument=name, argument=name, form=eat>argument=name, form=bread'
    #when searching with ambiguity do '{none=none>form=bread}'
    try:


        if not('@' in user_input):
            tree(user_input)
        else:
            actual = user_input
            for iz in actual.split(" "):
                if iz[0] == "@":
                    actual = string.replace(actual, iz[0], "deprel=")
            tree(actual)





    except AttributeError:
        continue
