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

## Introduction

This is a solution for **[Different Ways To Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses)** on LeetCode.

## Problem Description

Given a string `expression` of numbers and operators (`+`, `-`, `*`), return all possible results from computing all the different possible ways to group numbers and operators.

**Example 1:**
```
Input: expression = "2-1-1"
Output: [0, 2]
Explanation:
  ((2-1)-1) = 0
  (2-(1-1)) = 2
```

**Example 2:**
```
Input: expression = "2*3-4*5"
Output: [-34, -14, -10, -10, 10]
Explanation:
  (2*(3-(4*5))) = -34
  ((2*3)-(4*5)) = -14
  ((2*(3-4))*5) = -10
  (2*((3-4)*5)) = -10
  (((2*3)-4)*5) = 10
```

---

## Approach: Divide and Conquer

### Key Insight

Every operator in the expression is a potential "split point". When we place parentheses, we're essentially choosing which operator to compute **last**.

For example, in `2*3-4*5`:
- If `-` is computed last: `(2*3) - (4*5)` → we compute left and right separately, then subtract
- If first `*` is computed last: `2 * (3-4*5)` → we compute `2` and `3-4*5` separately

### Algorithm

1. **Base Case**: If the expression is just a number, return `[number]`
2. **Recursive Case**: For each operator in the expression:
   - Split into left and right sub-expressions
   - Recursively compute all possible results for both parts
   - Combine every left result with every right result using the operator

### Visual Example: `2-1-1`

```
         "2-1-1"
         /     \
   split at    split at
   1st '-'     2nd '-'
      |            |
  "2" - "1-1"   "2-1" - "1"
      |    |       |      |
    [2]   [0]    [1]    [1]
      \   /        \    /
      [2-0]       [1-1]
       [2]         [0]

Final: [2, 0] (order may vary)
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
            # Base case: expression is just a number
            if exp.isdigit():
                return (int(exp),)
            # end if
            
            result: list[int] = []
            
            # Try splitting at each operator
            for i, char in enumerate(exp):
                if char in '-+*':
                    # Recursively solve left and right parts
                    left_results = compute(exp[:i])
                    right_results = compute(exp[i + 1:])
                    
                    # Combine all possible left-right pairs
                    for left in left_results:
                        for right in right_results:
                            if char == '+':
                                result.append(left + right)
                            elif char == '-':
                                result.append(left - right)
                            else:  # char == '*'
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

Let $n$ be the number of operators in the expression.

### Time Complexity: $O(C_n)$ where $C_n$ is the n-th Catalan number

The number of ways to parenthesize $n$ operators follows the **Catalan number** sequence:

$$
C_n = \frac{1}{n+1} \binom{2n}{n} \approx \frac{4^n}{n^{3/2}\sqrt{\pi}}
$$

For each way, we do $O(n)$ work to combine results. So total: $O(n \cdot C_n)$.

### Space Complexity: $O(C_n)$

We store all possible results, and there are $C_n$ of them.

### Why Catalan Numbers?

The number of ways to fully parenthesize an expression with $n$ binary operators is exactly $C_n$:
- $n=1$: 1 way → $C_1 = 1$
- $n=2$: 2 ways → $C_2 = 2$
- $n=3$: 5 ways → $C_3 = 5$

This is the same as the number of structurally different binary trees with $n+1$ leaves.

---

## Summary

| Aspect | Description |
|--------|-------------|
| **Pattern** | Divide and Conquer |
| **Key Insight** | Each operator is a potential "last operation" |
| **Optimization** | Memoization with `@lru_cache` |
| **Time** | $O(n \cdot C_n)$ where $C_n$ is Catalan number |
