---
title: "[LeetCode] 1. Two Sum"
date: 2025-09-12 08:59:39 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy']
description: "Solution for LeetCode 1: Two Sum"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 1. Two Sum"
---

## Introduction
This is a solution for **[Two Sum](https://leetcode.com/problems/two-sum)** on LeetCode.

## Problem Description

<h2><a href="https://leetcode.com/problems/two-sum">1. Two Sum</a></h2><h3>Easy</h3><hr><p>Given an array of integers <code>nums</code>&nbsp;and an integer <code>target</code>, return <em>indices of the two numbers such that they add up to <code>target</code></em>.</p>

<p>You may assume that each input would have <strong><em>exactly</em> one solution</strong>, and you may not use the <em>same</em> element twice.</p>

<p>You can return the answer in any order.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [2,7,11,15], target = 9
<strong>Output:</strong> [0,1]
<strong>Explanation:</strong> Because nums[0] + nums[1] == 9, we return [0, 1].
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,2,4], target = 6
<strong>Output:</strong> [1,2]
</pre>

<p><strong class="example">Example 3:</strong></p>

<pre>
<strong>Input:</strong> nums = [3,3], target = 6
<strong>Output:</strong> [0,1]
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>2 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>-10<sup>9</sup> &lt;= nums[i] &lt;= 10<sup>9</sup></code></li>
	<li><code>-10<sup>9</sup> &lt;= target &lt;= 10<sup>9</sup></code></li>
	<li><strong>Only one valid answer exists.</strong></li>
</ul>

<p>&nbsp;</p>
<strong>Follow-up:&nbsp;</strong>Can you come up with an algorithm that is less than <code>O(n<sup>2</sup>)</code><font face="monospace">&nbsp;</font>time complexity?

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
- Dictionary to store value -> index mapping for fast lookup
- Iterate through array with both index and value
- Calculate the complement number needed to reach target
- Check if the complement exists in our hashmap (O(1) lookup)
- Found the pair! Return the indices of```mplement and current number
- Store current number and its index for```ture lookups

### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it.

## Solution
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Dictionary to store value -> index mapping for fast lookup
        num_map = {}
        
        # Iterate through array with both index and value
        for i, num in enumerate(nums):
            # Calculate the complement number needed to reach target
            complement = target - num
            
            # Check if the complement exists in our hashmap (O(1) lookup)
            if complement in num_map:
                # Found the pair! Return the indices of```mplement and current number
                return [num_map[complement], i]
            
            # Store current number and its index for```ture lookups
            num_map[num] = i
        
        return []
```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.

