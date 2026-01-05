---
title: "[LeetCode] 217. Contains Duplicate"
date: 2025-09-12 08:12:49 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Easy', 'Hash Table', 'Array']
description: "Solution for LeetCode 217: Contains Duplicate"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 217. Contains Duplicate"
author: seoultech
math: true
mermaid: true
---

## Problem

> [LeetCode 217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/)

Given an integer array `nums`, return `true` if any value appears at least twice, and return `false` if every element is distinct.

```
Input: nums = [1,2,3,1]
Output: true
```

---

## Initial Thought (Failed)

Check every pair of numbers to see if they are the same (**Brute Force**).

- Compare `nums[i]` with `nums[j]` for all $i < j$.
- **Time Complexity**: $O(N^2)$.
- For large inputs ($N=10^5$), this will time out.

**Alternative**: Sort the array first?
- Sorting takes $O(N \log N)$.
- Then check neighbors: `nums[i] == nums[i+1]`.
- This is good, but can we be faster?

---

## Key Insight

We need to check "Have I seen this number before?" in **$O(1)$** time.
The **Hash Set** data structure is designed exactly for this.

- Lookup: $O(1)$ on average.
- Insert: $O(1)$ on average.
- Total time: $O(N)$.

---

## Step-by-Step Analysis

`nums = [1, 2, 3, 1]`

```mermaid
graph TD
    S1[Start: Set={}] --> N1[Num: 1 <br> In Set? No]
    N1 --> A1[Add 1: Set={1}]
    A1 --> N2[Num: 2 <br> In Set? No]
    N2 --> A2[Add 2: Set={1, 2}]
    A2 --> N3[Num: 3 <br> In Set? No]
    N3 --> A3[Add 3: Set={1, 2, 3}]
    A3 --> N4[Num: 1 <br> In Set? YES!]
    N4 --> F[Return True]
    style F fill:#90EE90
```

1.  Initialize empty `seen` set.
2.  Traverse `nums`.
3.  If `num` in `seen` -> Duplicate found!
4.  If end reached -> No duplicates.

---

## Solution

```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        
        for num in nums:
            if num in seen:
                return True
            # end if
            seen.add(num)
        # end for
        
        return False
    # end def
```

---

## Complexity

- **Time Complexity**: $O(N)$
    - We iterate through the array once.
- **Space Complexity**: $O(N)$
    - In the worst case (no duplicates), all elements are stored in the set.

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Hash Set** | Trades space ($O(N)$) for speed ($O(1)$ lookup) |
| **Trading Resource** | Choose between Space ($O(N)$ with Set) vs Time ($O(N \log N)$ with Sort) |
