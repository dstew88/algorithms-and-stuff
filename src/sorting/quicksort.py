from typing import List

def quicksort(l: List[int]) -> List[int]:

    if len(l) <= 1:
        return l

    pivot = l[0]

    left = [x for x in l[1:] if x <= pivot]
    right = [x for x in l[1:] if x > pivot]

    return quicksort(left) + [pivot] + quicksort(right)