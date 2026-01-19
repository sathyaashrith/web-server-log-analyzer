from collections import Counter


def top_n(counter: Counter, n: int = 5):
    """
    Returns top N items from a Counter.
    """
    return counter.most_common(n)
