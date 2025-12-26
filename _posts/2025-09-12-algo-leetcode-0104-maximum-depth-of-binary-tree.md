---
title: "[LeetCode] 104. Maximum Depth of Binary Tree"
date: 2025-09-12 17:56:31 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Tree', 'DFS', 'Recursion']
description: "Solution for LeetCode 104: Maximum Depth of Binary Tree"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 104. Maximum Depth of Binary Tree"
author: seoultech
math: true
---

## Problem

> [LeetCode 104. Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

Given the root of a binary tree, return its maximum depth (number of nodes along the longest path from root to leaf).

```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

---

## Approach

Use **DFS (Depth-First Search)** recursively.

1. Base case: if node is `null`, depth is 0
2. Recursively get depth of left and right subtrees
3. Return `1 + max(left_depth, right_depth)`

---

## Solution

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        # end if
        
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        
        return 1 + max(left_depth, right_depth)
    # end def
```

---

## Complexity

- **Time**: $O(n)$ - visit every node once
- **Space**: $O(h)$ - recursion stack depth, where $h$ is tree height

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Recursion** | Natural fit for tree problems |
| **Space** | Worst case $O(n)$ for skewed tree, $O(\log n)$ for balanced |
