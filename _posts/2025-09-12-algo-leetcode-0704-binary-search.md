---
title: "[LeetCode] 704. Binary Search"
date: 2025-09-12 13:41:43 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy']
description: "Solution for LeetCode 704: Binary Search"
image:
  path: /assets/img/posts/algo/leetcode.png
  alt: [LeetCode] 704. Binary Search
---

## Introduction
This is a solution for **[Binary Search](https://leetcode.com/problems/binary-search)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/binary-search)

<h2><a href="https://leetcode.com/problems/binary-search">704. Binary Search</a></h2><h3>Easy</h3><hr><p>Given an array of integers <code>nums</code> which is sorted in ascending order, and an integer <code>target</code>, write a function to search <code>target</code> in <code>nums</code>. If <code>target</code> exists, then return its index. Otherwise, return <code>-1</code>.</p>

<p>You must write an algorithm with <code>O(log n)</code> runtime complexity.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>

<pre>
<strong>Input:</strong> nums = [-1,0,3,5,9,12], target = 9
<strong>Output:</strong> 4
<strong>Explanation:</strong> 9 exists in nums and its index is 4
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> nums = [-1,0,3,5,9,12], target = 2
<strong>Output:</strong> -1
<strong>Explanation:</strong> 2 does not exist in nums so return -1
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li><code>1 &lt;= nums.length &lt;= 10<sup>4</sup></code></li>
	<li><code>-10<sup>4</sup> &lt; nums[i], target &lt; 10<sup>4</sup></code></li>
	<li>All the integers in <code>nums</code> are <strong>unique</strong>.</li>
	<li><code>nums</code> is sorted in ascending order.</li>
</ul>


## Approach
<!-- TODO: Describe your thought process here. -->
The solution is implemented in Python.

## Solution
```python
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        
        while left <= right:
            mid = left + (right - left) // 2
            
            if nums[mid] == target:
                return mid
                
            # Target is smaller, search left half
            elif nums[mid] > target:
                right = mid - 1
                
            # Target is larger, search right half
            else:  
                left = mid + 1
        
        # Target not found in the array
        return -1
```

## Complexity Analysis
- **Time Complexity**: <!-- TODO: O(?) -->
- **Space Complexity**: <!-- TODO: O(?) -->

## Conclusion
<!-- TODO: Add insights or what you learned. -->
Solved successfully.

