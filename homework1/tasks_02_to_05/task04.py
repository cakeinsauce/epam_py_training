"""
Classic task, a kind of walnut for you

Given four lists A, B, C, D of integer values,
    compute how many tuples (i, j, k, l) there are such that A[i] + B[j] + C[k] + D[l] is zero.

We guarantee, that all A, B, C, D have same length of N where 0 ≤ N ≤ 1000.
"""
from typing import List


def check_sum_of_four(a: List[int], b: List[int], c: List[int], d: List[int]) -> int:
    """Return amount of tuples (i, j, k, l) there are such that A[i] + B[j] + C[k] + D[l] = 0"""
    # My approach here is to create dictionary where dict[c[i] + d[j]]: <amount of this sum in C and D lists>,
    # then we check every sum in A and B, and if that sum -(a[i] + b[j]) == c[i] + d[j], we increase the counter
    # by the amount of sums c[i] + d[j], in a nutshell, counter += dict[c[i] + d[j]].
    # Consider code below, Big-O = O(n^2) + 0(n^2) = O(n^2).
    tuple_counter = 0
    list_range = range(len(a))
    c_d_dict = {}
    for i in list_range:  # Filling up the c_d_dict
        for j in list_range:
            c_d_sum = c[i] + d[j]
            c_d_dict[c_d_sum] = (
                c_d_dict.get(c_d_sum, 0) + 1
            )  # Return 0 if there is no such c_d_sum, either increase by 1

    for i in list_range:
        for j in list_range:
            a_b_neg_sum = -(a[i] + b[j])
            if a_b_neg_sum in c_d_dict:
                tuple_counter += c_d_dict[a_b_neg_sum]

    return tuple_counter
