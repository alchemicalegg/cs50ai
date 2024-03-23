from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


class Person:
    def __init__(self, knight, knave):
        self.knight = knight
        self.knave = knave


A = Person(AKnight, AKnave)
B = Person(BKnight, BKnave)
C = Person(CKnight, CKnave)

people = [A, B, C]


def facts(person):
    return And(
        Or(person.knight, person.knave),
        Not(And(person.knight, person.knave)),
    )


basic_facts = And(*[facts(person) for person in people])


def claim(statement, person):
    return Or(
        And(person.knight, statement),
        And(person.knave, Not(statement)),
    )


# Puzzle 0
# A says "I am both a knight and a knave."
statement1 = And(AKnight, AKnave)
knowledge0 = And(
    basic_facts,
    claim(statement1, A),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
statement1 = And(AKnave, BKnave)
knowledge1 = And(
    basic_facts,
    claim(statement1, A),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
statement1 = Or((And(AKnight, BKnight)), And(AKnave, BKnave))
claim1 = claim(statement1, A)
statement2 = Or(And(AKnight, BKnave), And(AKnave, BKnight))
claim2 = claim(statement2, B)
knowledge2 = And(
    basic_facts,
    claim1,
    claim2,
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
a_says_i_am_a_knight = claim(AKnight, A)
a_says_i_am_a_knave = claim(AKnave, A)
claim1 = Or(a_says_i_am_a_knight, a_says_i_am_a_knave)
# B says "A said 'I am a knave'."
claim2 = claim(claim(AKnave, A), B)
# B says "C is a knave."
claim3 = claim(CKnave, B)
# C says "A is a knight."
claim4 = claim(AKnight, C)
knowledge3 = And(
    basic_facts,
    claim1,
    claim2,
    claim3,
    claim4
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
