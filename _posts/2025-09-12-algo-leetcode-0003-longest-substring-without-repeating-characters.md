---
title: "[LeetCode] 3. Longest Substring Without Repeating Characters"
date: 2025-09-12 18:16:57 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium', 'Sliding Window', 'Hash Table']
description: "Solution for LeetCode 3: Longest Substring Without Repeating Characters"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 3. Longest Substring Without Repeating Characters"
author: seoultech
math: true
---

## Problem

> [LeetCode 3. Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

Given a string `s`, find the length of the longest substring without repeating characters.

```
Input: s = "abcabcbb"
Output: 3
Explanation: "abc" is the longest substring.
```

---

## Approach

Use **Sliding Window** with a hash set.

1. Maintain a window `[left, right]`
2. Expand `right` to include new characters
3. If duplicate found, shrink from `left` until no duplicate
4. Track maximum window size

---

## Solution

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # Shrink window until no duplicate
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            # end while
            
            char_set.add(s[right])
            max_length = max(max_length, right - left + 1)
        # end for
        
        return max_length
    # end def
```

---

## Complexity

- **Time**: $O(n)$ - each character is added and removed at most once
- **Space**: $O(min(n, m))$ - where $m$ is the character set size

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Sliding Window** | Classic pattern for substring problems |
| **Hash Set** | $O(1)$ lookup for duplicate check |
