---
title: "[LeetCode] 680. Valid Palindrome II"
date: 2025-09-12 17:42:34 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Two Pointers', 'String']
description: "Solution for LeetCode 680: Valid Palindrome II"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 680. Valid Palindrome II"
author: seoultech
math: true
---

## Problem

> [LeetCode 680. Valid Palindrome II](https://leetcode.com/problems/valid-palindrome-ii/)

Given a string `s`, return `true` if you can make it a palindrome by deleting **at most one** character.

```
Input: s = "abca"
Output: true
Explanation: Delete 'c' to get "aba".
```

---

## Approach

Use **Two Pointers** with one chance to skip.

1. Start with pointers at both ends
2. If characters match, move both inward
3. If mismatch, try skipping left OR right character
4. Check if either resulting substring is a palindrome

---

## Solution

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_palindrome(left: int, right: int) -> bool:
            while left < right:
                if s[left] != s[right]:
                    return False
                # end if
                left += 1
                right -= 1
            # end while
            return True
        # end def
        
        left, right = 0, len(s) - 1
        
        while left < right:
            if s[left] != s[right]:
                # Try skipping left or right character
                return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
            # end if
            left += 1
            right -= 1
        # end while
        
        return True
    # end def
```

---

## Complexity

- **Time**: $O(n)$ - at most two passes through the string
- **Space**: $O(1)$ - only using pointers

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Greedy skip** | Try both options (skip left or right) |
| **Helper function** | Reuse palindrome check logic |
