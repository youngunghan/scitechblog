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
# What I first thought
for each way to add parentheses:
    evaluate the expression
    add to results
```

**Problem**: How do you even enumerate all parenthesis patterns? Parsing nested parentheses is a nightmare.

---

## Key Insight: Think About the LAST Operation

Instead of thinking "where do I put parentheses?", I realized:

> **Every operator can be the "last" operation to compute.**

For example, in `2*3-4*5`:
- If `-` is computed last: `(2*3) - (4*5)` → compute left and right first, then subtract
- If first `*` is last: `2 * (3-4*5)` → compute `2` and `3-4*5` separately

This is **Divide and Conquer**: split at each operator, solve recursively, combine results.

---

## Step-by-Step: Full Process for `"2-1-1"`

### Recursive Call Table

| Call | Input | Split Point | Left | Right | Result |
|------|-------|-------------|------|-------|--------|
| ① | `"2-1-1"` | 1st `-` | `"2"` | `"1-1"` | → go to ② |
| ② | `"1-1"` | `-` | `"1"` | `"1"` | `[0]` |
| ③ | `"2-1-1"` | 2nd `-` | `"2-1"` | `"1"` | → go to ④ |
| ④ | `"2-1"` | `-` | `"2"` | `"1"` | `[1]` |

### Combining Results

```
Call ②: "1-1" → left=[1], right=[1] → 1-1=0 → [0]
Call ①: "2" - "1-1" → left=[2], right=[0] → 2-0=2 → [2]

Call ④: "2-1" → left=[2], right=[1] → 2-1=1 → [1]  
Call ③: "2-1" - "1" → left=[1], right=[1] → 1-1=0 → [0]

Final: [2] + [0] = [2, 0]
```

### ASCII Recursion Tree

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

Final Result: [2, 0]
```

---

## Solution Code (Enhanced Comments)

```python
from typing import List
from functools import lru_cache

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        
        @lru_cache(maxsize=None)  # ← Cache to avoid recomputing same subexpressions
        def compute(exp: str) -> tuple[int, ...]:
            
            # Base case: if only a number, return it
            if exp.isdigit():
                return (int(exp),)  # e.g., "2" → (2,)
            # end if
            
            result: list[int] = []
            
            # Try each operator as the "last" operation
            for i, char in enumerate(exp):
                if char in '-+*':
                    # ↓ Split here!
                    left_results = compute(exp[:i])      # Left subexpression
                    right_results = compute(exp[i + 1:])  # Right subexpression
                    
                    # Combine all (left, right) pairs
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

### Code-Explanation Mapping

| Code Line | Purpose |
|-----------|---------|
| `@lru_cache` | Cache results for same subexpressions |
| `if exp.isdigit()` | Base case: `"2"` returns immediately |
| `for i, char in enumerate(exp)` | Try all operator positions |
| `exp[:i]`, `exp[i+1:]` | Split left/right at operator |
| `for left... for right...` | Generate all combinations |

---

## Complexity Analysis

### Time: $O(n \cdot C_n)$ - Catalan Number

The number of ways to parenthesize $n$ operators is the **Catalan number**:

$$C_n = \frac{1}{n+1} \binom{2n}{n}$$

| Operators | $C_n$ | Example |
|-----------|-------|---------|
| 1 | 1 | `a+b` → 1 way |
| 2 | 2 | `a+b-c` → 2 ways |
| 3 | 5 | `a+b-c*d` → 5 ways |
| 4 | 14 | 14 ways |

### Space: $O(C_n)$

Storing all results, plus memoization cache for intermediate subexpressions.

---

## Related Problems (Same Pattern)

Problems using the same **"Divide and Conquer + Memoization"** pattern:

| Problem | Difficulty | Key Similarity |
|---------|------------|----------------|
| [95. Unique Binary Search Trees II](https://leetcode.com/problems/unique-binary-search-trees-ii/) | Medium | Generate all possible BSTs (split by root) |
| [96. Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) | Medium | Count-only version of above (Catalan!) |
| [894. All Possible Full Binary Trees](https://leetcode.com/problems/all-possible-full-binary-trees/) | Medium | Generate all Full Binary Trees |
| [932. Beautiful Array](https://leetcode.com/problems/beautiful-array/) | Medium | D&C to construct array satisfying conditions |

**Common Pattern**: 
1. Generate all possible structures
2. Recursively solve subproblems
3. Combine results (or count them)

---

## Key Takeaways

| Lesson | Description |
|--------|-------------|
| **Think about the last operation** | Instead of "where to add parentheses", think "which operator is computed last" |
| **Divide and Conquer** | Split at each operator → solve recursively → combine |
| **Memoization is essential** | Same subexpressions appear multiple times |
| **Catalan Number** | This pattern's complexity is typically Catalan |
