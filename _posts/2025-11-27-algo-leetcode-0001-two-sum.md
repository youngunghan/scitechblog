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

## Approach

### Initial Thought: Brute Force

Check every possible pair of numbers: $O(N^2)$.

### Optimization: Hash Map (One-pass)

Use a Hash Map to store numbers we've seen:
1. For each `num`, calculate `complement = target - num`
2. If `complement` is in the map, we found the pair
3. Otherwise, add `num` to the map

This reduces lookup to $O(1)$.

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

- **Time**: $O(N)$ - single pass, $O(1)$ lookup per element
- **Space**: $O(N)$ - storing up to N elements in hash map

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Hash Map** | Trade space for time: $O(N^2)$ → $O(N)$ |
| **One-pass** | Check and store in the same loop |
