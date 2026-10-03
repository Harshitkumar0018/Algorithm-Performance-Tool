"""Task 2: Linear and Binary search with comparison counting."""
import random


def generate_dataset(n, seed=42):
    """Sorted list of n unique integers."""
    random.seed(seed)
    return sorted(random.sample(range(n * 10), n))


def linear_search(data, key):
    """Returns (index or -1, comparisons)."""
    comparisons = 0
    for i, value in enumerate(data):
        comparisons += 1
        if value == key:
            return i, comparisons
    return -1, comparisons


def binary_search(data, key):
    """Returns (index or -1, comparisons). Data must be sorted."""
    low, high = 0, len(data) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if data[mid] == key:
            return mid, comparisons
        if data[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons


ALGORITHMS = {"Linear Search": linear_search, "Binary Search": binary_search}
