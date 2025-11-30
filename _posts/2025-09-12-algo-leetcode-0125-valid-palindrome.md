---
title: "[LeetCode] 125. Valid Palindrome"
date: 2025-09-12 09:12:17 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy']
description: "Solution for LeetCode 125: Valid Palindrome"
image:
  path: /assets/img/posts/algo/leetcode.png
  alt: [LeetCode] 125. Valid Palindrome
---

## Introduction
This is a solution for **[Valid Palindrome](https://leetcode.com/problems/valid-palindrome)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/valid-palindrome)

<h2><a href="https://leetcode.com/problems/valid-palindrome">125. Valid Palindrome</a></h2><h3>Easy</h3><hr><p>A phrase is a <strong>palindrome</strong> if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.</p>

<p>Given a string <code>s</code>, return <code>true</code><em> if it is a <strong>palindrome</strong>, or </em><code>false</code><em> otherwise</em>.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;A man, a plan, a canal: Panama&quot;
<strong>Output:</strong> true
<strong>Explanation:</strong> &quot;amanaplanacanalpanama&quot; is a palindrome.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;race a car&quot;
<strong>Output:</strong> false
<strong>Explanation:</strong> &quot;raceacar&quot; is not a palindrome.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s = &quot; &quot;
<strong>Output:</strong> true
<strong>Explanation:</strong> s is an empty string &quot;&quot; after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= s.length &lt;= 2 * 10<sup>5</sup></code></li>
	<li><code>s</code> consists only of printable ASCII characters.</li>
</ul>


## Approach
<!-- TODO: Describe your thought process here. -->
The solution is implemented in Python.

## Solution
```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Initialize two pointers from both ends
        left, right = 0, len(s) - 1
        
        while left < right:
            # Skip non-alphanumeric characters from left
            if not s[left].isalnum():
                left += 1
                continue
                
            # Skip non-alphanumeric characters from right
            if not s[right].isalnum():
                right -= 1
                continue
                
            # Compare characters (case-insensitive)
            if s[left].lower() != s[right].lower():
                return False
                
            # Move both pointers inward
            left += 1
            right -= 1
        
        return True
```

## Complexity Analysis
- **Time Complexity**: <!-- TODO: O(?) -->
- **Space Complexity**: <!-- TODO: O(?) -->

## Conclusion
<!-- TODO: Add insights or what you learned. -->
Solved successfully.

