---
title: "[LeetCode] 241. Different Ways To Add Parentheses"
date: 2025-11-29 05:17:21 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium', 'Divide and Conquer', 'Recursion', 'Memoization']
description: "Solution for LeetCode 241: Different Ways To Add Parentheses"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 241. Different Ways To Add Parentheses"
author: seoultech
math: true
mermaid: true
---

## Problem

Given a string like `"2*3-4*5"`, return all possible results from different ways to add parentheses.

```
Input: "2-1-1"
Output: [0, 2]

((2-1)-1) = 0
(2-(1-1)) = 2
```

---

## My First Approach (Failed)

처음엔 모든 괄호 조합을 생성해서 각각 계산하려 했다.

```python
# 처음 생각한 방식
for each way to add parentheses:
    evaluate the expression
    add to results
```

**문제점**: 괄호 패턴을 어떻게 열거하지? 중첩된 괄호를 파싱하는 건 복잡하다.

---

## Key Insight: 마지막 연산을 기준으로 생각하자

괄호를 어디에 넣을지 고민하는 대신, 이렇게 생각을 바꿨다:

> **모든 operator는 "마지막으로 계산될" 가능성이 있다.**

예를 들어 `2*3-4*5`에서:
- `-`가 마지막이면: `(2*3) - (4*5)` → 좌우를 먼저 계산하고 빼기
- 첫 번째 `*`가 마지막이면: `2 * (3-4*5)` → 2와 나머지를 따로 계산

이게 바로 **Divide and Conquer**: operator마다 분할하고, 재귀적으로 풀고, 결과를 조합한다.

---

## Step-by-Step: `"2-1-1"` 전체 과정

### 전체 재귀 호출 테이블

| 호출 | 입력 | Split 위치 | Left | Right | 결과 |
|------|------|-----------|------|-------|------|
| ① | `"2-1-1"` | 1번째 `-` | `"2"` | `"1-1"` | → ②로 진행 |
| ② | `"1-1"` | `-` | `"1"` | `"1"` | `[0]` |
| ③ | `"2-1-1"` | 2번째 `-` | `"2-1"` | `"1"` | → ④로 진행 |
| ④ | `"2-1"` | `-` | `"2"` | `"1"` | `[1]` |

### 결과 조합 과정

```
호출 ②: "1-1" → left=[1], right=[1] → 1-1=0 → [0]
호출 ①: "2" - "1-1" → left=[2], right=[0] → 2-0=2 → [2]

호출 ④: "2-1" → left=[2], right=[1] → 2-1=1 → [1]  
호출 ③: "2-1" - "1" → left=[1], right=[1] → 1-1=0 → [0]

최종: [2] + [0] = [2, 0]
```

### ASCII 재귀 트리

```
                    "2-1-1"
                   /       \
            ①split@1      ③split@2
                |              |
         "2" - "1-1"      "2-1" - "1"
          |      |          |      |
         [2]    ②          ④     [1]
                |           |
            [1]-[1]     [2]-[1]
               ↓           ↓
             [0]         [1]
              ↓           ↓
           2-0=2       1-1=0
              ↓           ↓
            [2]         [0]

최종 결과: [2, 0]
```

---

## Solution Code (주석 강화)

```python
from typing import List
from functools import lru_cache

class Solution:
    def diffWaysToCompute(self, expression: str) -> List[int]:
        
        @lru_cache(maxsize=None)  # ← 같은 부분식 재계산 방지
        def compute(exp: str) -> tuple[int, ...]:
            
            # Base case: 숫자만 있으면 그대로 반환
            if exp.isdigit():
                return (int(exp),)  # ← 예: "2" → (2,)
            # end if
            
            result: list[int] = []
            
            # 각 operator를 "마지막 연산"으로 시도
            for i, char in enumerate(exp):
                if char in '-+*':
                    # ↓ 여기서 분할!
                    left_results = compute(exp[:i])      # 왼쪽 부분식
                    right_results = compute(exp[i + 1:])  # 오른쪽 부분식
                    
                    # 모든 (왼쪽, 오른쪽) 조합을 계산
                    for left in left_results:
                        for right in right_results:
                            if char == '+':
                                result.append(left + right)
                            elif char == '-':
                                result.append(left - right)
                            else:  # char == '*'
                                result.append(left * right)
                            # end if
                        # end for
                    # end for
                # end if
            # end for
            
            return tuple(result)
        # end def
        
        return list(compute(expression))
    # end def
```

### 코드-설명 매핑

| 코드 라인 | 역할 |
|----------|------|
| `@lru_cache` | 같은 부분식이 여러 번 나오면 캐시에서 가져옴 |
| `if exp.isdigit()` | Base case: `"2"` 같은 숫자만 남으면 종료 |
| `for i, char in enumerate(exp)` | 모든 operator 위치를 시도 |
| `exp[:i]`, `exp[i+1:]` | operator 기준 좌/우 분할 |
| `for left... for right...` | 가능한 모든 조합 생성 |

---

## Complexity Analysis

### Time: $O(n \cdot C_n)$ - Catalan Number

$n$개의 operator로 만들 수 있는 괄호 패턴 수는 **Catalan number**:

$$C_n = \frac{1}{n+1} \binom{2n}{n}$$

| Operators | $C_n$ | 예시 |
|-----------|-------|------|
| 1 | 1 | `a+b` → 1가지 |
| 2 | 2 | `a+b-c` → 2가지 |
| 3 | 5 | `a+b-c*d` → 5가지 |
| 4 | 14 | 14가지 |

### Space: $O(C_n)$

모든 결과를 저장하고, memoization으로 중간 결과 캐싱.

---

## Related Problems (같은 패턴)

이 문제와 같은 **"Divide and Conquer + Memoization"** 패턴을 쓰는 문제들:

| Problem | 난이도 | 핵심 유사점 |
|---------|--------|-----------|
| [95. Unique Binary Search Trees II](https://leetcode.com/problems/unique-binary-search-trees-ii/) | Medium | 가능한 모든 BST 생성 (숫자 범위를 분할) |
| [96. Unique Binary Search Trees](https://leetcode.com/problems/unique-binary-search-trees/) | Medium | 위 문제의 "개수만" 세는 버전 (Catalan!) |
| [894. All Possible Full Binary Trees](https://leetcode.com/problems/all-possible-full-binary-trees/) | Medium | 가능한 모든 Full Binary Tree 생성 |
| [932. Beautiful Array](https://leetcode.com/problems/beautiful-array/) | Medium | D&C로 조건 만족하는 배열 생성 |

**공통점**: 
1. 모든 가능한 구조를 생성
2. 재귀적으로 부분 문제 해결
3. 결과 조합 (또는 개수 계산)

---

## Key Takeaways

| 교훈 | 설명 |
|------|------|
| **마지막 연산 기준 사고** | "어디에 괄호?" 대신 "어떤 연산이 마지막?" |
| **Divide and Conquer** | Operator 기준 분할 → 재귀 → 조합 |
| **Memoization 필수** | 같은 부분식이 여러 번 등장 |
| **Catalan Number** | 이 패턴의 복잡도는 보통 Catalan |
