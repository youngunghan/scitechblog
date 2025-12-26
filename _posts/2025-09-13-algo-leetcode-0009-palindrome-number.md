---
title: "[LeetCode] 9. Palindrome Number"
date: 2025-09-13 13:55:54 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Math']
description: "Solution for LeetCode 9: Palindrome Number"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 9. Palindrome Number"
author: seoultech
math: true
---

## Problem

> [LeetCode 9. Palindrome Number](https://leetcode.com/problems/palindrome-number/)

Given an integer `x`, return `true` if it's a palindrome (reads the same backward).

```
Input: x = 121
Output: true
```

---

## Approach

Reverse half the number and compare.

1. Negative numbers are not palindromes
2. Numbers ending in 0 (except 0 itself) are not palindromes
3. Reverse the second half of the number
4. Compare with the first half

---

## Solution

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Negative or ends with 0 (but not 0 itself)
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        # end if
        
        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10
        # end while
        
        # For odd-length numbers, middle digit is in reversed_half
        return x == reversed_half or x == reversed_half // 10
    # end def
```

---

## Complexity

- **Time**: $O(\log_{10} n)$ - processing half the digits
- **Space**: $O(1)$ - only using a few variables

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Half reversal** | Avoids overflow, more elegant than string conversion |
| **Edge cases** | Negative numbers, trailing zeros |
