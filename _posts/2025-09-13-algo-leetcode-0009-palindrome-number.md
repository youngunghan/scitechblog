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
mermaid: true
---

## Problem

> [LeetCode 9. Palindrome Number](https://leetcode.com/problems/palindrome-number/)

Given an integer `x`, return `true` if it's a palindrome (reads the same backward).

```
Input: x = 121
Output: true
```

---

## Initial Thought (Failed)

Convert the integer to a string and check if it reads the same backwards.
- `s = str(x)`
- `return s == s[::-1]`

**Why avoid this?**
- It uses **extra space** proportional to the number of digits.
- The problem often asks (as a follow-up) to do it without converting to string.

---

## Key Insight

We can construct the **reverse** of the number mathematically.
However, reversing the *entire* number might cause **integer overflow** (in languages with fixed integer sizes).

**Better Idea**: Revert only **half** of the number!
- Given `1221`.
- Right Half Reversed: `12`. Remaining Left Half: `12`.
- `12 == 12`.

---

## Step-by-Step Analysis

`x = 1221`

```mermaid
graph TD
    S1["x=1221, rev=0"] --> S2["Process 1: <br> rev = 0*10 + 1 = 1 <br> x = 122"]
    S2 --> S3["Process 2: <br> rev = 1*10 + 2 = 12 <br> x = 12"]
    S3 --> C{"x <= rev?"}
    C -- Yes --> R["Compare x == rev?"]
    R --> F["12 == 12: True"]
    style F fill:#90EE90
```

1.  Stop loop when `x <= reversed_half`.
2.  If even length (`1221`), `x == reversed_half`.
3.  If odd length (`121`), `x == reversed_half // 10` (ignore middle digit).

---

## Solution

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Edge cases: Negative numbers or numbers ending with 0 (except 0)
        if x < 0 or (x % 10 == 0 and x != 0):
            return False
        # end if
        
        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10
        # end while
        
        # Even length vs Odd length
        return x == reversed_half or x == reversed_half // 10
    # end def
```

---

## Complexity

- **Time Complexity**: $O(\log_{10} N)$
    - We iterate through half the number of digits.
- **Space Complexity**: $O(1)$
    - No strings, just integers.

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Math Reversal** | `rev = rev * 10 + digit` pattern |
| **Half Execution** | Stopping halfway avoids overflow and redundant checks |
| **Edge Cases** | Negative numbers and logic for trailing zeros |
