---
title: "[LeetCode] 1. Two Sum"
date: 2025-11-27 00:00:00 +0900
categories: [Algorithm, LeetCode]
tags: [Algorithm, LeetCode, Easy, Array, Hash Table]
description: "Solution for LeetCode 1: Two Sum"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 1. Two Sum"
author: seoultech
math: true
mermaid: true
---

## Problem

> [LeetCode 1. Two Sum](https://leetcode.com/problems/two-sum/)

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: nums[0] + nums[1] == 9
```

---

## Initial Thought (Failed)

Check every possible pair of numbers (**Brute Force**).

- Loop `i` from $0$ to $N$.
- Loop `j` from $i+1$ to $N$.
- Check if `nums[i] + nums[j] == target`.

**Complexity**: $O(N^2)$.
This is acceptable for small $N$, but we can do better.

---

## Key Insight

We are looking for `target - num`.
Instead of scanning the array again to find this complement, we can use a **Hash Map** for $O(1)$ lookup.

- As we iterate, we store `{value: index}` in the map.
- Before adding the current number, we check if its complement is already in the map.

---

## Step-by-Step Analysis

`nums = [2, 7, 11, 15]`, `target = 9`

```mermaid
graph TD
    S1[Start: Map={}] --> N1[Num: 2 <br> Need: 7 <br> In Map? No]
    N1 --> A1[Map Add: {2: 0}]
    A1 --> N2[Num: 7 <br> Need: 2 <br> In Map? YES!]
    N2 --> F[Found Pair! <br> Indices: 0, 1]
    style F fill:#90EE90
```

1.  Current: 2. Need: 9-2=7. Not found. Map `{2: 0}`.
2.  Current: 7. Need: 9-7=2. Found at index 0. Return `[0, 1]`.

---

## Solution

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_map = {}
        
        for i, num in enumerate(nums):
            complement = target - num
            
            if complement in num_map:
                return [num_map[complement], i]
            # end if
            
            num_map[num] = i
        # end for
        
        return []
    # end def
```

---

## Complexity

- **Time Complexity**: $O(N)$
    - Single pass through the array. Map lookups are $O(1)$.
- **Space Complexity**: $O(N)$
    - Hash Map stores up to $N$ elements.

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Space-Time Tradeoff** | Use memory ($O(N)$ Map) to save time ($O(N^2) \to O(N)$) |
| **One-pass** | You don't need to populate the map first; check as you go |
