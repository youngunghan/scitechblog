---
title: "[LeetCode] 241. Different Ways To Add Parentheses"
date: 2025-11-29 05:17:21 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium', 'Divide and Conquer', 'Recursion', 'Memoization']
description: "Solution for LeetCode 241: Different Ways To Add Parentheses"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 241. Different Ways To Add Parentheses"
author: seoultech
math: true
---

## Problem

> [LeetCode 241. Different Ways To Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses/)

Given a string like `"2*3-4*5"`, return all possible results from different ways to add parentheses.

```
Input: "2-1-1"
Output: [0, 2]

((2-1)-1) = 0
(2-(1-1)) = 2
```

---

## My First Approach (Failed)

I initially tried to generate all possible parenthesis combinations and evaluate each one.

**Problem**: How do you even enumerate all parenthesis patterns? Parsing nested parentheses is complex.

---

## Key Insight

Instead of thinking "where do I put parentheses?", I realized:

> **Every operator can be the "last" operation to compute.**

For `2*3-4*5`:
- If `-` is computed last: `(2*3) - (4*5)`
- If first `*` is last: `2 * (3-4*5)`

This is **Divide and Conquer**: split at each operator, solve recursively, combine results.

---

## Step-by-Step: `"2-1-1"`

### Table

| Call | Input | Split | Left | Right | Result |
|------|-------|-------|------|-------|--------|
| ① | `"2-1-1"` | 1st `-` | `"2"` | `"1-1"` | → ② |
| ② | `"1-1"` | `-` | `"1"` | `"1"` | `[0]` |
| ③ | `"2-1-1"` | 2nd `-` | `"2-1"` | `"1"` | → ④ |
| ④ | `"2-1"` | `-` | `"2"` | `"1"` | `[1]` |

### Visualization

```
                "2-1-1"
               /       \
        ①split@1      ③split@2
            |              |
     "2" - "1-1"      "2-1" - "1"
      |      |          |      |
     [2]    ②          ④     [1]
            |           |
        [1]-[1]     [2]-[1]
           ↓           ↓
         [0]         [1]
          ↓           ↓
       2-0=2       1-1=0
          ↓           ↓
        [2]         [0]

Final: [2, 0]
```

---

## Solution

```python
from typing import List
from functools import lru_cache

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        
        @lru_cache(maxsize=None)
        def compute(exp: str) -> tuple[int, ...]:
            # Base case: just a number
            if exp.isdigit():
                return (int(exp),)
            # end if
            
            result: list[int] = []
            
            # Try each operator as the "last" operation
            for i, char in enumerate(exp):
                if char in '-+*':
                    left_results = compute(exp[:i])
                    right_results = compute(exp[i + 1:])
                    
                    for left in left_results:
                        for right in right_results:
                            if char == '+':
                                result.append(left + right)
                            elif char == '-':
                                result.append(left - right)
                            else:
                                result.append(left * right)
                            # end if
                        # end for
                    # end for
                # end if
            # end for
            
            return tuple(result)
        # end def
        
        return list(compute(expression))
    # end def
```

---

## Complexity

### Time: $O(C_n)$ - Catalan Number

The number of ways to parenthesize $n$ operators:

$$C_n = \frac{1}{n+1} \binom{2n}{n}$$

| Operators | $C_n$ |
|-----------|-------|
| 1 | 1 |
| 2 | 2 |
| 3 | 5 |
| 4 | 14 |

### Space: $O(C_n)$

---

## Key Takeaways

| Lesson | Description |
|--------|-------------|
| **Think about the last operation** | "Which operator is computed last?" |
| **Divide and Conquer** | Split → Recurse → Combine |
| **Memoization** | Cache repeated subexpressions |
