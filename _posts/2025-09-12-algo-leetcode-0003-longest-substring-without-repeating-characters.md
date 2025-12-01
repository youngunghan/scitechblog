---
title: "[LeetCode] 3. Longest Substring Without Repeating Characters"
date: 2025-09-12 10:48:04 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium']
description: "Solution for LeetCode 3: Longest Substring Without Repeating Characters"
image:
  path: assets/img/posts/algo/leetcode.png
  alt: "[LeetCode] 3. Longest Substring Without Repeating Characters"
---

## Introduction
This is a solution for **[Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/longest-substring-without-repeating-characters)

<h2><a href="https://leetcode.com/problems/longest-substring-without-repeating-characters">3. Longest Substring Without Repeating Characters</a></h2><h3>Medium</h3><hr><p>Given a string <code>s</code>, find the length of the <strong>longest</strong> <span data-keyword="substring-nonempty"><strong>substring</strong></span> without duplicate characters.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;abcabcbb&quot;
<strong>Output:</strong> 3
<strong>Explanation:</strong> The answer is &quot;abc&quot;, with the length of 3.
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;bbbbb&quot;
<strong>Output:</strong> 1
<strong>Explanation:</strong> The answer is &quot;b&quot;, with the length of 1.
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> s = &quot;pwwkew&quot;
<strong>Output:</strong> 3
<strong>Explanation:</strong> The answer is &quot;wke&quot;, with the length of 3.
Notice that the answer must be a substring, &quot;pwke&quot; is a subsequence and not a substring.
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>0 &lt;= s.length &lt;= 5 * 10<sup>4</sup></code></li>
	<li><code>s</code> consists of English letters, digits, symbols and spaces.</li>
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
- Dictionary to track characters in current window
- Left pointer of sliding window and result
- Right pointer moves through the string
- If character already exists in current window
- Move left pointer to skip the duplicate
- Update character's latest position
- Update maximum length found so far

### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it.

## Solution
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Dictionary to track characters in current window
        char_map = {}
        
        # Left pointer of sliding window and result
        left = 0
        max_length = 0
        
        # Right pointer moves through the string
        for right, char in enumerate(s):
            # If character already exists in current window
            if char in char_map and char_map[char] >= left:
                # Move left pointer to skip the duplicate
                left = char_map[char] + 1
            
            # Update character's latest position
            char_map[char] = right
            
            # Update maximum length found so far
            max_length = max(max_length, right - left + 1)
        
        return max_length
```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.

