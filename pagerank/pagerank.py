import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, current_page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    links = corpus[current_page]
    true_damping_factor = 0 if len(links) == 0 else damping_factor
    for page in corpus:
        # Do we need to exclude the current page?
        if page not in links:
            link_chance = 0
        else:
            link_chance = damping_factor / len(links)
        random_chance = (1 - true_damping_factor) / len(corpus)
        model[page] = link_chance + random_chance
    return model

def choice(choices):
    n = random.random() # 0.34
    total = 0
    for page, probability in choices.items(): # {"page1.html": 0.05, "page2.html": 0.475,…}
        total += probability
        if total >= n:
            return page
    raise Exception("oops")

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visits = {}
    page = random.choice(list(corpus.keys()))
    for i in range(0, n):
        visits[page] = visits.get(page, 0) + 1
        model = transition_model(corpus, page, damping_factor)
        page = choice(model)
    pagerank = {}
    for page in corpus:
        pagerank[page] = visits.get(page, 0) / n
    return pagerank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # -- Do this part once

    # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
    for page, links in corpus.items():
        if not links:
            corpus[page] = corpus.keys()

    # Build up a dict of inbound links that we'll need later
    inbound_links = {}
    for away, outbound_links in corpus.items():
        for here in outbound_links:
            if not inbound_links.get(here):
                inbound_links[here] = set()
            inbound_links[here].add(away)

    # The function should begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    n = len(corpus)
    pagerank = {}
    for page in corpus:
        damping_part = (1 - damping_factor) / n
        pagerank_part = damping_factor * (1 / n)
        pagerank[page] = damping_part + pagerank_part


    # -- Do this part a lot of times

    while True:
        highest_change_seen = 0
        new_pagerank = {}
        for page in corpus:
            damping_part = (1 - damping_factor) / n
            links_to = inbound_links.get(page, set())
            pagerank_part = damping_factor * calc_pagerank(links_to, corpus, pagerank)
            new_pagerank[page] = damping_part + pagerank_part
            highest_change_seen = max(highest_change_seen, abs(pagerank[page] - new_pagerank[page]))
        pagerank = new_pagerank
        if highest_change_seen < 0.001:
            break
    return pagerank

def calc_pagerank(links_to, corpus, pagerank):
    x = 0
    for page in links_to:
        num_links_away = len(corpus[page])
        if num_links_away == 0:
            num_links_away = len(corpus)
        x += pagerank[page] / num_links_away
    return x

if __name__ == "__main__":
    main()
