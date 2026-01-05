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
mermaid: true
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

## Initial Thought (Failed)

Check all possible substrings and verify if they have unique characters (**Brute Force**).

- **Number of substrings**: $O(N^2)$.
- **Verification**: $O(N)$.
- **Total Complexity**: $O(N^3)$.

For $N=50,000$, this will definitely time out. We need a linear time approach.

---

## Key Insight

We only care about the **current valid window**.
We can maintain a window `[left, right]` that guarantees uniqueness.

- Expand `right` as much as possible.
- If we meet a duplicate character, shrink `left` until the duplicate is removed.
- This is the classic **Sliding Window** technique.

---

## Step-by-Step Analysis

Example: `s = "abca"`

```mermaid
graph TD
    S1[Start: left=0, right=0, char='a'] --> S2[Set: {'a'}, Len=1]
    S2 --> S3[Expand: right=1, char='b']
    S3 --> S4[Set: {'a', 'b'}, Len=2]
    S4 --> S5[Expand: right=2, char='c']
    S5 --> S6[Set: {'a', 'b', 'c'}, Len=3]
    S6 --> S7[Expand: right=3, char='a' <br> Duplicate Found!]
    
    S7 --> S8[Shrink: Remove s[left]='a', left++]
    S8 --> S9[Now Valid Again: {'b', 'c', 'a'}]
    style S7 fill:#ffaaaa
    style S9 fill:#90EE90
```

1.  Use a **Hash Set** to store characters in the current window.
2.  `right` pointer iterates from $0$ to $N-1$.
3.  While `s[right]` is in the set, remove `s[left]` and increment `left`.
4.  Update max length.

---

## Solution

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_set = set()
        left = 0
        max_length = 0
        
        for right in range(len(s)):
            # If duplicate found, shrink window from left
            while s[right] in char_set:
                char_set.remove(s[left])
                left += 1
            # end while
            
            # Add new character
            char_set.add(s[right])
            max_length = max(max_length, right - left + 1)
        # end for
        
        return max_length
    # end def
```

---

## Complexity

- **Time Complexity**: $O(N)$
    - Each character is visited at most twice (once by `right`, once by `left`).
- **Space Complexity**: $O(\min(N, \Sigma))$
    - Hash Set stores at most unique characters. $\Sigma$ is alphabet size.

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Sliding Window** | Expand right, shrink left pattern for subarray problems |
| **Hash Set** | $O(1)$ check for duplicates |
| **Invariant** | The window `[left, right]` always contains unique characters |
