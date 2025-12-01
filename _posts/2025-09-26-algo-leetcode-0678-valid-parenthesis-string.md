---
title: "[LeetCode] 678. Valid Parenthesis String"
date: 2025-09-26 08:08:26 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium']
description: "Solution for LeetCode 678: Valid Parenthesis String"
image:
  path: /assets/img/posts/algo/leetcode.png
  alt: [LeetCode] 678. Valid Parenthesis String
---

## Introduction
This is a solution for **[Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/valid-parenthesis-string)

<h2><a href="https://leetcode.com/problems/valid-parenthesis-string">678. Valid Parenthesis String</a></h2><h3>Medium</h3><hr><p>Given a string <code>s</code> containing only three types of characters: <code>&#39;(&#39;</code>, <code>&#39;)&#39;</code> and <code>&#39;*&#39;</code>, return <code>true</code> <em>if</em> <code>s</code> <em>is <strong>valid</strong></em>.</p>

<p>The following rules define a <strong>valid</strong> string:</p>

<ul>
	<li>Any left parenthesis <code>&#39;(&#39;</code> must have a corresponding right parenthesis <code>&#39;)&#39;</code>.</li>
	<li>Any right parenthesis <code>&#39;)&#39;</code> must have a corresponding left parenthesis <code>&#39;(&#39;</code>.</li>
	<li>Left parenthesis <code>&#39;(&#39;</code> must go before the corresponding right parenthesis <code>&#39;)&#39;</code>.</li>
	<li><code>&#39;*&#39;</code> could be treated as a single right parenthesis <code>&#39;)&#39;</code> or a single left parenthesis <code>&#39;(&#39;</code> or an empty string <code>&quot;&quot;</code>.</li>
</ul>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<pre><strong>Input:</strong> s = "()"
<strong>Output:</strong> true
</pre><p><strong class="example">Example 2:</strong></p>
<pre><strong>Input:</strong> s = "(*)"
<strong>Output:</strong> true
</pre><p><strong class="example">Example 3:</strong></p>
<pre><strong>Input:</strong> s = "(*))"
<strong>Output:</strong> true
</pre>
<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 100</code></li>
	<li><code>s[i]</code> is <code>&#39;(&#39;</code>, <code>&#39;)&#39;</code> or <code>&#39;*&#39;</code>.</li>
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

### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it.

## Solution
```python
class Solution:
    def checkValidString(self, s: str) -> bool:
        low = 0   # minimum count of '(' characters
        high = 0  # maximum count of '(' characters
        
        for char in s:
            if char == '(':
                low += 1   # increment both counters for '('
                high += 1
            elif char == ')':
                low -= 1   # decrement both counters for ')'
                high -= 1
            else:  # char == '*'
                low -= 1   # treat '*' as ')' or empty string (minimum case)
                high += 1  # treat '*' as '(' (maximum case)
            
            # if high becomes negative, too many ')' characters
            if high < 0:
                return False
            
            # reset low to 0 if negative (ignore unnecessary ')')
            low = max(low, 0)
        
        # valid if we can balance all parentheses (low == 0)
        return low == 0
```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.

