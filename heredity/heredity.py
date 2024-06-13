import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.8f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    probability = 1
    for person in people:
        person_prob = 1
        father = people[person]['father']
        mother = people[person]['mother']
        if father and mother:
            gene_chance = inheritance_chances(father, mother, one_gene, two_genes)
        else:
            gene_chance = PROBS["gene"]
        person_genes = number_of_genes(person, one_gene, two_genes)
        person_gene_prob = gene_chance[person_genes]
        person_prob *= person_gene_prob

        person_trait = person in have_trait
        person_trait_prob = trait_likelihood(person_trait, person_genes)

        person_prob *= person_trait_prob

        probability *= person_prob

    return probability

def inheritance_chances(father, mother, one_gene, two_genes):
    dadyes, dadno = chance_of_passing_on(number_of_genes(father, one_gene, two_genes))
    mumyes, mumno = chance_of_passing_on(number_of_genes(mother, one_gene, two_genes))
    print(dadyes, mumyes)
    return {
        0: dadno * mumno,
        1: dadyes * mumno + dadno * mumyes,
        2: dadyes * mumyes,
    }

def number_of_genes(person, one_gene, two_genes):
    if person in one_gene:
        return 1
    if person in two_genes:
        return 2
    return 0

def chance_of_passing_on(genes):
    if genes == 2:
        return 1 - PROBS["mutation"], PROBS["mutation"]
    if genes == 1:
        return 0.5, 0.5
    if genes == 0:
        return PROBS["mutation"], 1 - PROBS["mutation"]


def trait_likelihood(has_trait, num_genes):
    return PROBS["trait"][num_genes][has_trait]

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    all_people = probabilities.keys()
    no_genes = all_people - one_gene - two_genes
    for person in no_genes:
        probabilities[person]["gene"][0] += p
    for person in one_gene:
        probabilities[person]["gene"][1] += p
    for person in two_genes:
        probabilities[person]["gene"][2] += p
    no_trait = all_people - have_trait
    for person in no_trait:
        probabilities[person]["trait"][False] += p
    for person in have_trait:
        probabilities[person]["trait"][True] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person, attributes in probabilities.items():
        for attribute, probs in attributes.items():
            denominator = sum(probs.values())
            for key, value in probs.items():
                probs[key] = value / denominator

def test_normalize():
    input = {
        'Pev': {
            "gene": {2: 0.2, 1: 0.3, 0: 0.4},
            "trait": {True: 97, False: 11},
        },
        'Melody': {
            "gene": {2: 4, 1: 2, 0: 6},
            "trait": {True: 1000, False: 1},
        },
    }
    expected = {
        'Pev': {
            "gene": {2: 0.222, 1: 0.333, 0: 0.444},
            "trait": {True: 0.898, False: 0.102},
        },
        'Melody': {
            "gene": {2: 0.333, 1: 0.167, 0: 0.5},
            "trait": {True: 0.999, False: 0.001},
        },
    }
    normalize(input)
    for person in input:
        for k in ["gene", "trait"]:
            for k2 in input[person][k]:
                assert round(input[person][k][k2], 3) == expected[person][k][k2]

if __name__ == "__main__":
    test_normalize()
    main()
