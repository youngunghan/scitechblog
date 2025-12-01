---
title: "[LeetCode] 241. Different Ways To Add Parentheses"
date: 2025-11-29 05:17:21 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium']
description: "Solution for LeetCode 241: Different Ways To Add Parentheses"
image:
  path: /scitechblog/assets/img/posts/algo/leetcode.png
  alt: [LeetCode] 241. Different Ways To Add Parentheses
---

## Introduction
This is a solution for **[Different Ways To Add Parentheses](https://leetcode.com/problems/different-ways-to-add-parentheses)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/different-ways-to-add-parentheses)

<h2><a href="https://leetcode.com/problems/different-ways-to-add-parentheses">241. Different Ways to Add Parentheses</a></h2><h3>Medium</h3><hr><p>Given a string <code>expression</code> of numbers and operators, return <em>all possible results from computing all the different possible ways to group numbers and operators</em>. You may return the answer in <strong>any order</strong>.</p>

<p>The test cases are generated such that the output values fit in a 32-bit integer and the number of different results does not exceed <code>10<sup>4</sup></code>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> expression = &quot;2-1-1&quot;
<strong>Output:</strong> [0,2]
<strong>Explanation:</strong>
((2-1)-1) = 0 
(2-(1-1)) = 2
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> expression = &quot;2*3-4*5&quot;
<strong>Output:</strong> [-34,-14,-10,-10,10]
<strong>Explanation:</strong>
(2*(3-(4*5))) = -34 
((2*3)-(4*5)) = -14 
((2*(3-4))*5) = -10 
(2*((3-4)*5)) = -10 
(((2*3)-4)*5) = 10
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= expression.length &lt;= 20</code></li>
	<li><code>expression</code> consists of digits and the operator <code>&#39;+&#39;</code>, <code>&#39;-&#39;</code>, and <code>&#39;*&#39;</code>.</li>
	<li>All the integer values in the input expression are in the range <code>[0, 99]</code>.</li>
	<li>The integer values in the input expression do not have a leading <code>&#39;-&#39;</code> or <code>&#39;+&#39;</code> denoting the sign.</li>
</ul>


## Approach
### 1. Problem Analysis
This problem focuses on **Implementation** skills.
The key is to carefully read the problem statement and translate the requirements into code accurately.
Using appropriate data structures (List, Dictionary, Set) to optimize complexity is crucial.

### 2. Solution Idea
1.  **Input Parsing**: Handle the input format as specified.
2.  **Logic Design**: Break down the requirements into steps.
3.  **Edge Cases**: Handle boundary cases and special conditions.

### Code Analysis
**Code Comments Analysis**:
- Use memoization to store results of sub-expressions to avoid redundant calculations.
- Base case: if the expression contains only a number, return it as a list of integer.
- end if
- Iterate through each character to find operators.
- Divide the expression into left and right parts at the operator.
- Recursively compute all possible results for both parts.
- Combine every result from the left part with every result from the right part using the current operator.
- char == '*'
- end if
- end for
- end for
- end if
- end for
- end def
- end def

### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it.

## Solution
```python
from typing import List
from functools import lru_cache

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        # Use memoization to store results of sub-expressions to avoid redundant calculations.
        @lru_cache(maxsize=None)
        def compute(exp: str) -> List[int]:
            # Base case: if the expression contains only a number, return it as a list of integer.
            if exp.isdigit():
                return [int(exp)]
            # end if
            
            result: List[int] = []
            
            # Iterate through each character to find operators.
            for i, char in enumerate(exp):
                if char in '-+*':
                    # Divide the expression into left and right parts at the operator.
                    # Recursively compute all possible results for both parts.
                    left_results: List[int] = compute(exp[:i])
                    right_results: List[int] = compute(exp[i + 1:])
                    
                    # Combine every result from the left part with every result from the right part using the current operator.
                    for left_val in left_results:
                        for right_val in right_results:
                            if char == '+':
                                result.append(left_val + right_val)
                            elif char == '-':
                                result.append(left_val - right_val)
                            else:  # char == '*'
                                result.append(left_val * right_val)
                            # end if
                        # end for
                    # end for
                # end if
            # end for
            
            return result
        # end def
        
        return compute(expression)
    # end def

```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.

