---
title: "[LeetCode] 678. Valid Parenthesis String"
date: 2025-09-26 08:08:26 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium', 'Greedy', 'String']
description: "Solution for LeetCode 678: Valid Parenthesis String"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 678. Valid Parenthesis String"
author: seoultech
math: true
---

## Problem

> [LeetCode 678. Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/)

Given a string containing `(`, `)`, and `*`, determine if it's valid. The `*` can be treated as `(`, `)`, or empty.

```
Input: s = "(*)"
Output: true
```

---

## Approach

Use **Greedy** with range tracking.

Instead of tracking exact count of `(`, track the possible range `[low, high]`:
- `low`: minimum possible count of unmatched `(`
- `high`: maximum possible count of unmatched `(`

---

## Solution

```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        low = 0   # minimum unmatched '('
        high = 0  # maximum unmatched '('
        
        for char in s:
            if char == '(':
                low += 1
                high += 1
            elif char == ')':
                low -= 1
                high -= 1
            else:  # char == '*'
                low -= 1   # treat as ')' or empty
                high += 1  # treat as '('
            # end if
            
            # Can't have negative high (too many ')')
            if high < 0:
                return False
            # end if
            
            # low can't go negative
            low = max(low, 0)
        # end for
        
        return low == 0
    # end def
```

---

## Complexity

- **Time**: $O(n)$ - single pass
- **Space**: $O(1)$ - only two variables

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Range tracking** | Instead of exact count, track min/max possible |
| **Greedy insight** | `*` creates a range of possibilities |
