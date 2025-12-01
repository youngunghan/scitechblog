---
title: "[LeetCode] 1. Two Sum"
date: 2025-11-27 00:00:00 +0900
categories: [Algorithm, LeetCode]
tags: [Array, Hash Table, Python]
description: "A classic algorithmic problem that demonstrates the power of Hash Maps for optimizing time complexity."
image:
  path: assets/img/posts/algo/leetcode.png
  alt: "[LeetCode] 1. Two Sum"
---

## Introduction
"Two Sum" is often the first problem developers encounter on LeetCode. While it seems deceptively simple, it serves as a perfect example to demonstrate the trade-off between time and space complexity. It teaches us how to move from a naive $O(N^2)$ solution to an optimized $O(N)$ one using a Hash Map.

## Problem Description
> [Link to Problem](https://leetcode.com/problems/two-sum)

Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to `target`*.

You may assume that each input would have **exactly one solution**, and you may not use the *same* element twice.

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

## Approach

### 1. Initial Thought: Brute Force
The most intuitive approach is to check every possible pair of numbers.
-   Iterate through each number `x`.
-   Iterate through every other number `y`.
-   If `x + y == target`, return their indices.

However, this results in a time complexity of $O(N^2)$, which is inefficient for large datasets.

### 2. Optimization: Hash Map (One-pass)
We can improve this by using a **Hash Map** (Dictionary in Python) to store the numbers we have seen so far.
-   As we iterate through the array, for each number `num`, we calculate the `complement` needed to reach the `target` (`complement = target - num`).
-   If the `complement` is already in our map, it means we found the pair! We return the index of the complement and the current index.
-   If not, we add the current `num` and its index to the map and continue.

This reduces the lookup time to $O(1)$, making the overall complexity linear.

## Solution

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Dictionary to store value -> index mapping for fast lookup
        num_map = {}
        
        # Iterate through array with both index and value
        for i, num in enumerate(nums):
            # Calculate the complement number needed to reach target
            complement = target - num
            
            # Check if the complement exists in our hashmap (O(1) lookup)
            if complement in num_map:
                # Found the pair! Return the indices of complement and current number
                return [num_map[complement], i]
            
            # Store current number and its index for future lookups
            num_map[num] = i
        
        return []
```

## Complexity Analysis
-   **Time Complexity**: $O(N)$
    -   We traverse the list containing $N$ elements exactly once. Each lookup in the hash table costs only $O(1)$ time.
-   **Space Complexity**: $O(N)$
    -   The extra space required depends on the number of items stored in the hash table, which stores at most $N$ elements.

## Conclusion
This problem is a great reminder that sometimes, sacrificing a bit of memory (Space Complexity) can lead to significant gains in speed (Time Complexity). The **Hash Map** strategy used here is a fundamental pattern applicable to many other algorithmic problems involving "finding pairs" or "checking existence".
