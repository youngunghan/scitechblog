---
title: "[LeetCode] 217. Contains Duplicate"
date: 2025-09-12 08:12:49 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Hash Table', 'Array']
description: "Solution for LeetCode 217: Contains Duplicate"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 217. Contains Duplicate"
author: seoultech
math: true
---

## Problem

> [LeetCode 217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

Given an integer array `nums`, return `true` if any value appears at least twice, and return `false` if every element is distinct.

```
Input: nums = [1,2,3,1]
Output: true
```

---

## Approach

Use a **Hash Set** to track seen numbers.

1. Iterate through the array
2. If the number is already in the set, return `true`
3. Otherwise, add it to the set
4. If we finish without finding a duplicate, return `false`

---

## Solution

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        
        for num in nums:
            if num in seen:
                return True
            # end if
            seen.add(num)
        # end for
        
        return False
    # end def
```

---

## Complexity

- **Time**: $O(n)$ - single pass through the array
- **Space**: $O(n)$ - storing up to n elements in the set

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Hash Set** | $O(1)$ lookup makes this efficient |
| **Alternative** | Sorting would be $O(n \log n)$ time, $O(1)$ space |
