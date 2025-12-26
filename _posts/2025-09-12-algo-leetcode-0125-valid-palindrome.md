---
title: "[LeetCode] 125. Valid Palindrome"
date: 2025-09-12 09:12:17 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Two Pointers', 'String']
description: "Solution for LeetCode 125: Valid Palindrome"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 125. Valid Palindrome"
author: seoultech
math: true
---

## Problem

> [LeetCode 125. Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward.

```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

---

## Approach

Use **Two Pointers** - one from the start, one from the end.

1. Skip non-alphanumeric characters
2. Compare characters (case-insensitive)
3. If any mismatch, return `false`
4. If pointers meet, return `true`

---

## Solution

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        
        while left < right:
            # Skip non-alphanumeric from left
            while left < right and not s[left].isalnum():
                left += 1
            # end while
            
            # Skip non-alphanumeric from right
            while left < right and not s[right].isalnum():
                right -= 1
            # end while
            
            # Compare (case-insensitive)
            if s[left].lower() != s[right].lower():
                return False
            # end if
            
            left += 1
            right -= 1
        # end while
        
        return True
    # end def
```

---

## Complexity

- **Time**: $O(n)$ - single pass through the string
- **Space**: $O(1)$ - only using pointers

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Two Pointers** | Classic pattern for palindrome checking |
| **In-place** | No need to create a cleaned string |
