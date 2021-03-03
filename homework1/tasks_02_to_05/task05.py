"""
Given a list of integers numbers "nums".

You need to find a sub-array with length less equal to "k", with maximal sum.

The written function should return the sum of this sub-array.

Examples:
    nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
    result = 16
"""
from typing import List


def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    """Return the largest sum of k-length sub-array."""
    nums_len = len(nums)
    result = None
    if k > nums_len:  # Size of k-length sub-array is greater than array.
        k = nums_len

    for num in range(nums_len - k + 1):
        sub_arr_sum = sum(
            nums[num : num + k]
        )  # Slicing sub-arrays of nums to calculate a sum
        if result is None or sub_arr_sum > result:
            result = sub_arr_sum
    return result
