import nltk
import re
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> Section | Section Conj Section
Section -> NP V | NP V NP | NP V NP NP | NP V Adv | V NP | V NP NP | NP V NP NP NP
NP -> N | Det NP | P NP | Adj NP | NP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.tokenize.word_tokenize(sentence)
    r = []
    for word in words:
        word = word.lower()
        if re.search('[a-z]', word):
            r.append(word)
    return r


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    nps = []
    for subtree in tree.subtrees():
        if is_np_chunk(subtree):
            nps.append(subtree)
        if subtree != tree:
            nps += np_chunk(subtree)
    return nps


def contains_np(tree):
    for subtree in tree.subtrees():
        if tree != subtree and contains_np(subtree):
            return True
    return False

def is_np_chunk(tree):
    if tree.label() != "NP":
        return False
    for subtree in tree.subtrees():
        if tree != subtree and subtree.label() == "NP":
            return False
    return True

if __name__ == "__main__":
    main()
