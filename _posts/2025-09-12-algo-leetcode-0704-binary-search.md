---
title: "[LeetCode] 704. Binary Search"
date: 2025-09-12 13:41:43 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Binary Search']
description: "Solution for LeetCode 704: Binary Search"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 704. Binary Search"
author: seoultech
math: true
---

## Problem

> [LeetCode 704. Binary Search](https://leetcode.com/problems/binary-search/)

Given a sorted array of integers `nums` and an integer `target`, return the index of `target` if it exists, otherwise return `-1`.

**Constraint**: You must write an algorithm with `O(log n)` runtime complexity.

```
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4
```

---

## Approach

Binary Search divides the search space in half with each comparison.

1. Start with `left = 0`, `right = len(nums) - 1`
2. While `left <= right`:
   - Calculate `mid = left + (right - left) // 2`
   - If `nums[mid] == target`: return `mid`
   - If `nums[mid] > target`: search left half (`right = mid - 1`)
   - Else: search right half (`left = mid + 1`)
3. If not found, return `-1`

---

## Solution

```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        # end while
        
        return -1
    # end def
```

---

## Complexity

- **Time**: $O(\log n)$ - halving the search space each iteration
- **Space**: $O(1)$ - only using a few variables

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Overflow prevention** | Use `left + (right - left) // 2` instead of `(left + right) // 2` |
| **Boundary condition** | `left <= right` (not `<`) to check the last element |
