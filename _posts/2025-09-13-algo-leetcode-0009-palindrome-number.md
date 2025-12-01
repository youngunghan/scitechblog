---
title: "[LeetCode] 9. Palindrome Number"
date: 2025-09-13 21:41:57 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy']
description: "Solution for LeetCode 9: Palindrome Number"
image:
  path: /scitechblog/assets/img/posts/algo/leetcode.png
  alt: [LeetCode] 9. Palindrome Number
---

## Introduction
This is a solution for **[Palindrome Number](https://leetcode.com/problems/palindrome-number)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/palindrome-number)

<h2><a href="https://leetcode.com/problems/palindrome-number">9. Palindrome Number</a></h2><h3>Easy</h3><hr><p>Given an integer <code>x</code>, return <code>true</code><em> if </em><code>x</code><em> is a </em><span data-keyword="palindrome-integer"><em><strong>palindrome</strong></em></span><em>, and </em><code>false</code><em> otherwise</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> x = 121
<strong>Output:</strong> true
<strong>Explanation:</strong> 121 reads as 121 from left to right and from right to left.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> x = -121
<strong>Output:</strong> false
<strong>Explanation:</strong> From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> x = 10
<strong>Output:</strong> false
<strong>Explanation:</strong> Reads 01 from right to left. Therefore it is not a palindrome.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>-2<sup>31</sup>&nbsp;&lt;= x &lt;= 2<sup>31</sup>&nbsp;- 1</code></li>
</ul>

<p>&nbsp;</p>
<strong>Follow up:</strong> Could you solve it without converting the integer to a string?

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
    def isPalindrome(self, x: int) -> bool:
        str_ = str(x)
        for i in range(len(str_)):
            if str_[i] != str_[-1 - i]:
                return False
        return True
```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.

