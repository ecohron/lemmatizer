# Lemmatizer
Solves lemmatization for in vocabulary and out of vocabulary English verbs using finite state transducers. Implemented in Python3 using OpenFST.

## writeup.pdf
Describes the original assignment goals and parameters.

## lemmatizer.py
Builds the lemmatizer using OpenFST. Creates a finite state transducer which handles all forms of English verb lemmatization, both from the lemma to the conjugated forms and vice versa.

## in_vocab_dictionary_verbs.txt
Contains line-separated list of in vocabulary words in their infinitive (lemma) form and several other conjugated forms such as past, present participle, and past participle.
