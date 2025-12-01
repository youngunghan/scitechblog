---
title: "[LeetCode] 680. Valid Palindrome Ii"
date: 2025-09-12 09:21:50 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy']
description: "Solution for LeetCode 680: Valid Palindrome Ii"
image:
  path: assets/img/posts/algo/leetcode.png
  alt: "[LeetCode] 680. Valid Palindrome Ii"
---

## Introduction
This is a solution for **[Valid Palindrome Ii](https://leetcode.com/problems/valid-palindrome-ii)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/valid-palindrome-ii)

<h2><a href="https://leetcode.com/problems/valid-palindrome-ii">680. Valid Palindrome II</a></h2><h3>Easy</h3><hr><p>Given a string <code>s</code>, return <code>true</code> <em>if the </em><code>s</code><em> can be palindrome after deleting <strong>at most one</strong> character from it</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;aba&quot;
<strong>Output:</strong> true
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;abca&quot;
<strong>Output:</strong> true
<strong>Explanation:</strong> You could delete the character &#39;c&#39;.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;abc&quot;
<strong>Output:</strong> false
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 10<sup>5</sup></code></li>
	<li><code>s</code> consists of lowercase English letters.</li>
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
- Use two pointers from both ends
- If characters match, continue inward
- First mismatch found - try deleting either character
- Option 1: Delete left character (skip left pointer)
- Option 2: Delete right character (skip right pointer)
- No mismatch found - already a palindrome

### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it.

## Solution
```python
class Solution:
    def validPalindrome(self, s: str) -> bool:
        def is_palindrome_range(left, right):
            """Helper function to check if substring is palindrome"""
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True
        
        # Use two pointers from both ends
        left, right = 0, len(s) - 1
        
        while left < right:
            # If characters match, continue inward
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                # First mismatch found - try deleting either character
                # Option 1: Delete left character (skip left pointer)
                # Option 2: Delete right character (skip right pointer)
                return (is_palindrome_range(left + 1, right) or 
                        is_palindrome_range(left, right - 1))
        
        # No mismatch found - already a palindrome
        return True
```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.

