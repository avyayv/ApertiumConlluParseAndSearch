# Conllu Parsing and Searching
Please see the page on the apertium wiki for documentation http://wiki.apertium.org/w/index.php?title=Conllu_Parsing_and_Searching

== Parse and Search through a conllu file ==

Searching is as follows: 


These are the terms for searching. Between the words you are searching for a relation between, add a '>'. You can also use and '<' if you are searching for a word that is a dependent of another word. This, the '<', will find the dependent word. For instance, if you wanted to see when 'have' did action to 'clue' (i.e. I have no clue') you could do it like this:

For example <code> python conlluparse.py "text.conllu" 'have>clue'</code> might output:
 Token: 2, Form: have, Lemma: have, UPOSTAG: VERB, HEAD: 0, DEPREL: root, # sent_id = 2, Sentence:  I have no clue .

If you wanted, you could also be more specific or ambigious with your searches. When you specify these arguments, you also need to make sure that you concatenate "Form=" with the word you are searching for. When you have nothing specified on one side, you need to add 'none=none' to that side. For instance if you wanted to find if something was a dependent of 'have', you could do:

<code> none=none<form=have </code>

When searching with attributes (i.e UPOSTAG), you could do this like: 

<code>python conlluparse.py "text.conllu" 'upostag=verb, form=have>form=clue'</code> which may output:
 Token: 2, Form: have, Lemma: have, UPOSTAG: VERB, HEAD: 0, DEPREL: root, # sent_id = 2, Sentence:  I have no clue .

You can search with any of these tags - upostag, xpostag, lemma, or deprel. You would do this by just putting the tag name + and '=' and then the actual value. Concatenate the tag an '=' and the value like upostag=noun' or 'lemma=clue' or @.

You can also specify attributes instead of 'form=clue' such as 'upostag=noun' 

 Token: 2, Form: have, Lemma: have, UPOSTAG: VERB, HEAD: 0, DEPREL: root, # sent_id = 2, Sentence:  I have no clue .

Now, instead, if you search with <code>python conlluparse.py "text.conllu" 'form=clue<none=none' </code>, it will print:

 Token: 4, Form: clue, Lemma: clue, UPOSTAG: NOUN, HEAD: 2, DEPREL: obj, # sent_id = 2, Sentence:  I have no clue .

ou can search for a word with a specific deprel or upostag like 

<code> @root, upostag=noun>none=none </code>

You can search for relationships like the ; character:

<code> @nsubj>upostag=noun </code>

You can search for a plain word like:

<code> form=have>none=none </code>

You can do very simple searches like <code> python conlluparse.py "text.conllu" "lemma=Еуровидение,form=Еуровидениенің" </code> without the > or <

== Examples ==


<code>python conlluparse.py "text.conllu" "none=none>none=none, @obj"</code>
This is how you would run the program. Could output: 
 Token: 6, Form: іліп, Lemma: іл, UPOSTAG: VERB, HEAD: 0, DEPREL: root, # sent_id = Ер_Төстік.tagged.txt:23:396, Sentence:  Сөйткенде Төстіктің бір бақайы өрмекті іліп кетеді .
