---
title: "[LeetCode] 104. Maximum Depth Of Binary Tree"
date: 2025-09-12 13:51:19 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy']
description: "Solution for LeetCode 104: Maximum Depth Of Binary Tree"
image:
  path: /assets/img/posts/algo/leetcode.png
  alt: [LeetCode] 104. Maximum Depth Of Binary Tree
---

## Introduction
This is a solution for **[Maximum Depth Of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree)** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/maximum-depth-of-binary-tree)

<h2><a href="https://leetcode.com/problems/maximum-depth-of-binary-tree">104. Maximum Depth of Binary Tree</a></h2><h3>Easy</h3><hr><p>Given the <code>root</code> of a binary tree, return <em>its maximum depth</em>.</p>

<p>A binary tree&#39;s <strong>maximum depth</strong>&nbsp;is the number of nodes along the longest path from the root node down to the farthest leaf node.</p>

<p>&nbsp;</p>
<p><strong class="example">Example 1:</strong></p>
<img alt="" src="https://assets.leetcode.com/uploads/2020/11/26/tmp-tree.jpg" style="width: 400px; height: 277px;" />
<pre>
<strong>Input:</strong> root = [3,9,20,null,null,15,7]
<strong>Output:</strong> 3
</pre>

<p><strong class="example">Example 2:</strong></p>

<pre>
<strong>Input:</strong> root = [1,null,2]
<strong>Output:</strong> 2
</pre>

<p>&nbsp;</p>
<p><strong>Constraints:</strong></p>

<ul>
	<li>The number of nodes in the tree is in the range <code>[0, 10<sup>4</sup>]</code>.</li>
	<li><code>-100 &lt;= Node.val &lt;= 100</code></li>
</ul>


## Approach
<!-- TODO: Describe your thought process here. -->
The solution is implemented in Python.

## Solution
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
    
        # Stack stores (node, current_depth) pairs
        stack = [(root, 1)]
        max_depth = 0
        
        while stack:
            node, current_depth = stack.pop()
            
            # Update maximum depth found so far
            max_depth = max(max_depth, current_depth)
            
            # Add children to stack with incremented depth
            if node.left:
                stack.append((node.left, current_depth + 1))
            if node.right:
                stack.append((node.right, current_depth + 1))
        
        return max_depth
```

## Complexity Analysis
- **Time Complexity**: <!-- TODO: O(?) -->
- **Space Complexity**: <!-- TODO: O(?) -->

## Conclusion
<!-- TODO: Add insights or what you learned. -->
Solved successfully.

