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
mermaid: true
---

## Problem

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

```python
# Pseudocode of my first attempt
for each way to add parentheses:
    evaluate the expression
    add to results
```

**Problem**: How do you even enumerate all parenthesis patterns? The number of valid patterns grows exponentially, and parsing nested parentheses is a nightmare.

---

## The Insight: Think About the LAST Operation

Instead of thinking "where do I put parentheses?", I realized:

> **Every operator can be the "last" operation to compute.**

For `2*3-4*5`:
- If `-` is computed last: `(2*3) - (4*5)` → left side and right side are computed first
- If first `*` is last: `2 * (3-4*5)` → we compute `2` and `3-4*5` separately

This is **Divide and Conquer**: split at each operator, solve left and right recursively, combine results.

---

## Step-by-Step: How `"2-1-1"` Works

### Step 1: Find All Operators

```
"2-1-1"
   ^   ^
   |   |
  op1  op2
```

We can split at position 1 (first `-`) or position 3 (second `-`).

### Step 2: Split at First `-`

| Left | Operator | Right |
|------|----------|-------|
| `"2"` | `-` | `"1-1"` |

- Left `"2"` → just a number → `[2]`
- Right `"1-1"` → needs recursive call

### Step 3: Recursively Solve `"1-1"`

| Left | Operator | Right |
|------|----------|-------|
| `"1"` | `-` | `"1"` |

- Left `"1"` → `[1]`
- Right `"1"` → `[1]`
- Combine: `1 - 1 = 0` → `[0]`

### Step 4: Combine Step 2

- Left results: `[2]`
- Right results: `[0]` (from Step 3)
- Combine: `2 - 0 = 2` → `[2]`

### Step 5: Split at Second `-`

| Left | Operator | Right |
|------|----------|-------|
| `"2-1"` | `-` | `"1"` |

- Left `"2-1"` → `2 - 1 = 1` → `[1]`
- Right `"1"` → `[1]`
- Combine: `1 - 1 = 0` → `[0]`

### Final Result

Combining Step 4 and Step 5: `[2, 0]`

---

## Visualizing the Recursion Tree

```
                    "2-1-1"
                   /       \
            split@1st-    split@2nd-
                |              |
         "2" - "1-1"      "2-1" - "1"
          |      |          |      |
         [2]    [0]        [1]    [1]
          \    /            \    /
          2-0=2            1-1=0

        Results: [2]        Results: [0]

Final: [2, 0]
```

---

## Solution Code

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
                    
                    # Combine all pairs
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

## Complexity Analysis

### Time: $O(C_n)$ - Catalan Number

The number of ways to parenthesize $n$ operators is the **Catalan number**:

$$C_n = \frac{1}{n+1} \binom{2n}{n}$$

| Operators | $C_n$ | Examples |
|-----------|-------|----------|
| 1 | 1 | `a+b` → 1 way |
| 2 | 2 | `a+b+c` → 2 ways |
| 3 | 5 | `a+b+c+d` → 5 ways |
| 4 | 14 | 14 ways |

### Space: $O(C_n)$

We store all possible results, and memoization caches intermediate results.

---

## Key Takeaways

| Lesson | Description |
|--------|-------------|
| **Think about the last operation** | Instead of "where to add parentheses", think "which operator is computed last" |
| **Divide and Conquer** | Split at each operator, solve recursively, combine |
| **Memoization** | Same subexpressions appear multiple times, cache them |
