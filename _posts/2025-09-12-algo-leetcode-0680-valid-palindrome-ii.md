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
mermaid: true
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

## Initial Thought (Failed)

Try deleting every character one by one and checking if the rest is a palindrome?

- String length $N$.
- $N$ possible deletions.
- Each check takes $O(N)$.
- Total: $O(N^2)$. Too slow for $N=10^5$.

---

## Key Insight

We only need to act when we find a **mismatch**.
Standard palindrome check (Two Pointers) works fine until `s[left] != s[right]`.

At that moment locally, we have two choices to fix the mismatch:
1.  Skip `left` character (delete `s[left]`).
2.  Skip `right` character (delete `s[right]`).

Since we can delete **at most one** character, if either of these modified substrings is a palindrome, the answer is True.

---

## Step-by-Step Analysis

`s = "abca"`

```mermaid
graph TD
    S1[L=0 'a', R=3 'a' <br> Match] --> S2[L=1 'b', R=2 'c' <br> Mismatch!]
    S2 --> C1{Try Option 1: <br> Skip 'b'}
    S2 --> C2{Try Option 2: <br> Skip 'c'}
    
    C1 --> R1[Left with "c" <br> Palindrome? YES]
    C2 --> R2[Left with "b" <br> Palindrome? YES]
    
    R1 --> Success[Return True]
    style Success fill:#90EE90
```

1.  Start `left`, `right`.
2.  Loop while `left < right`.
3.  If mismatch: return `isPalindrome(left+1, right)` OR `isPalindrome(left, right-1)`.
4.  If loop finishes: return `True`.

---

## Solution

```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_palindrome_range(l: int, r: int) -> bool:
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True
        # end def
        
        left, right = 0, len(s) - 1
        
        while left < right:
            if s[left] != s[right]:
                # Try deleting s[left] OR s[right]
                # If either one works, we are good.
                return is_palindrome_range(left + 1, right) or \
                       is_palindrome_range(left, right - 1)
            # end if
            left += 1
            right -= 1
        # end while
        
        return True
    # end def
```

---

## Complexity

- **Time Complexity**: $O(N)$
    - Main loop runs at most $N/2$ steps.
    - If mismatch, sub-checks run at most $N$ steps.
    - Total is linear.
- **Space Complexity**: $O(1)$
    - Only variables.

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Greedy Choice** | When stuck, we explore finite possibilities (only 2 here) |
| **Reuse** | Helper function prevents code duplication |
