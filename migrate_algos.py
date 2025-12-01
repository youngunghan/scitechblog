import os
import re
import datetime
import subprocess

# Configuration
REPO_ROOT = "/home/yuhan/repo/scitechblog"
TEMP_REPOS = os.path.join(REPO_ROOT, "temp_repos")
POSTS_DIR = os.path.join(REPO_ROOT, "_posts")
BAEKJOON_DIR = os.path.join(TEMP_REPOS, "Algorithm-and-Problem-Solving", "백준")
LEETCODE_DIR = os.path.join(TEMP_REPOS, "LeetCodeHub")

# Detailed Content Templates
APPROACH_TEMPLATES = {
    "dp": """### 1. 문제 분석 (Problem Analysis)
이 문제는 **Dynamic Programming (DP)** 유형으로 분류됩니다.
가장 큰 단서는 **최적 부분 구조(Optimal Substructure)**와 **중복되는 부분 문제(Overlapping Subproblems)**입니다.
- 큰 문제를 작은 문제로 쪼갤 수 있는가? -> Yes
- 동일한 작은 문제가 반복적으로 호출되는가? -> Yes
이 두 가지 조건을 만족하므로, 점화식을 세워 메모이제이션(Memoization)이나 타뷸레이션(Tabulation)을 적용해야 함을 알 수 있습니다.

### 2. 해결 아이디어 (Solution Idea)
1.  **상태 정의 (State Definition)**: `dp[i]`가 무엇을 의미하는지 정의합니다.
2.  **점화식 도출 (Recurrence Relation)**: `dp[i]`를 구하기 위해 `dp[i-1]`, `dp[i-2]` 등을 어떻게 활용할지 식을 세웁니다.
3.  **초기값 설정 (Base Case)**: 점화식의 시작점이 되는 초기값을 설정합니다.
4.  **구현**: 반복문(Bottom-up) 또는 재귀(Top-down)로 구현합니다.""",

    "graph": """### 1. 문제 분석 (Problem Analysis)
이 문제는 **그래프 탐색 (Graph Traversal)** 알고리즘이 필요합니다.
단서는 **'연결된', '경로', '네트워크'** 등의 키워드와 노드(정점) 간의 관계입니다.
- 최단 거리를 구해야 하는가? -> BFS (가중치가 없다면) 또는 Dijkstra
- 모든 정점을 방문해야 하는가? -> DFS 또는 BFS
- 사이클이 존재하는가? -> Union-Find 또는 DFS

### 2. 해결 아이디어 (Solution Idea)
1.  **그래프 모델링**: 문제를 그래프(인접 리스트 또는 인접 행렬)로 표현합니다.
2.  **탐색 알고리즘 선택**: 문제 조건(가중치 유무, 최단 경로 여부 등)에 맞춰 BFS/DFS를 선택합니다.
3.  **방문 처리**: `visited` 배열을 사용하여 중복 방문을 방지합니다.
4.  **구현**: 큐(Queue)나 스택(Stack/Recursion)을 사용하여 탐색을 구현합니다.""",

    "math": """### 1. 문제 분석 (Problem Analysis)
이 문제는 **수학적 성질 (Mathematical Property)**을 활용해야 합니다.
단서는 입력 크기(N)가 매우 크거나, 특정 패턴/규칙이 보인다는 점입니다.
단순 시뮬레이션으로는 시간 초과(TLE)가 발생할 가능성이 높으므로, 수식으로 정리하여 O(1) 또는 O(log N)으로 줄여야 합니다.

### 2. 해결 아이디어 (Solution Idea)
1.  **규칙 찾기**: 작은 케이스(N=1, 2, 3...)를 직접 계산해보며 규칙성을 발견합니다.
2.  **수식화**: 발견한 규칙을 일반항이나 점화식으로 표현합니다.
3.  **알고리즘 적용**: 정수론(소수 판별, 최대공약수), 조합론, 기하학 등의 이론을 적용합니다.""",

    "greedy": """### 1. 문제 분석 (Problem Analysis)
이 문제는 **그리디 알고리즘 (Greedy Algorithm)**으로 접근해야 합니다.
단서는 **'현재 상황에서 가장 최적인 선택'**이 전체 결과의 최적해를 보장한다는 직관입니다.
- 탐욕적 선택 속성(Greedy Choice Property)이 성립하는가?
- 최적 부분 구조(Optimal Substructure)를 가지는가?

### 2. 해결 아이디어 (Solution Idea)
1.  **기준 설정**: 무엇을 기준으로 정렬하거나 선택할지 결정합니다.
2.  **정렬**: 기준에 따라 데이터를 정렬합니다.
3.  **선택 및 갱신**: 순차적으로 최선의 선택을 하며 결과를 갱신합니다.""",

    "search": """### 1. 문제 분석 (Problem Analysis)
이 문제는 **탐색 (Search)**, 특히 **이분 탐색 (Binary Search)**이 효과적입니다.
단서는 **'정렬된 데이터'**이거나, **'특정 값(Parametric Search)'**을 찾아야 하는데 입력 범위가 매우 클 때(예: 10억 이상)입니다.
O(N)으로는 해결이 불가능하므로 O(log N) 알고리즘이 필요합니다.

### 2. 해결 아이디어 (Solution Idea)
1.  **탐색 범위 설정**: `left`, `right` 인덱스를 초기화합니다.
2.  **결정 조건 정의**: `mid` 값이 조건을 만족하는지 확인하는 함수를 정의합니다.
3.  **범위 좁히기**: 조건에 따라 `left` 또는 `right`를 갱신하며 범위를 절반으로 줄여나갑니다.""",

    "default": """### 1. 문제 분석 (Problem Analysis)
이 문제는 특별한 알고리즘보다는 **구현 (Implementation)** 능력을 요구합니다.
문제의 지문을 꼼꼼히 읽고, 주어진 조건과 제약사항을 그대로 코드로 옮기는 것이 핵심입니다.
자료구조(리스트, 딕셔너리, 셋 등)를 적절히 활용하여 복잡도를 줄이는 것이 중요합니다.

### 2. 해결 아이디어 (Solution Idea)
1.  **입력 처리**: 문제에서 주어지는 입력 형식을 파싱합니다.
2.  **로직 설계**: 문제의 요구사항을 단계별로 나눕니다.
3.  **예외 처리**: 경계값(Boundary Case)이나 특수 조건을 처리합니다."""
}

APPROACH_TEMPLATES_EN = {
    "dp": """### 1. Problem Analysis
This problem is classified as **Dynamic Programming (DP)**.
The key clues are **Optimal Substructure** and **Overlapping Subproblems**.
- Can the problem be broken down into smaller subproblems? -> Yes
- Are the same subproblems solved repeatedly? -> Yes
These signs suggest using a recurrence relation with Memoization or Tabulation.

### 2. Solution Idea
1.  **State Definition**: Define what `dp[i]` represents.
2.  **Recurrence Relation**: Formulate how to calculate `dp[i]` using `dp[i-1]`, `dp[i-2]`, etc.
3.  **Base Case**: Set the initial values for the recurrence.
4.  **Implementation**: Implement using Bottom-up iteration or Top-down recursion.""",

    "graph": """### 1. Problem Analysis
This problem requires a **Graph Traversal** algorithm.
Keywords like **'connected', 'path', 'network'** and relationships between nodes suggest a graph approach.
- Need shortest path? -> BFS (unweighted) or Dijkstra
- Need to visit all nodes? -> DFS or BFS
- Cycle detection? -> Union-Find or DFS

### 2. Solution Idea
1.  **Graph Modeling**: Represent the problem as a graph (Adjacency List/Matrix).
2.  **Algorithm Selection**: Choose BFS/DFS based on constraints (weighted/unweighted, etc.).
3.  **Visited Array**: Use a `visited` set/array to prevent cycles and redundant processing.
4.  **Implementation**: Use a Queue for BFS or Stack/Recursion for DFS.""",

    "default": """### 1. Problem Analysis
This problem focuses on **Implementation** skills.
The key is to carefully read the problem statement and translate the requirements into code accurately.
Using appropriate data structures (List, Dictionary, Set) to optimize complexity is crucial.

### 2. Solution Idea
1.  **Input Parsing**: Handle the input format as specified.
2.  **Logic Design**: Break down the requirements into steps.
3.  **Edge Cases**: Handle boundary cases and special conditions."""
}

TROUBLESHOOTING_TEMPLATES = {
    "dp": """### 3. 트러블슈팅 (Troubleshooting)
- **점화식 오류**: 초기에는 잘못된 점화식을 세워 예제 입력조차 통과하지 못했습니다. 손으로 작은 케이스를 직접 계산해보며 점화식을 수정했습니다.
- **메모리 초과**: 2차원 배열을 사용하다가 메모리 제한에 걸려, 슬라이딩 윈도우 기법(필요한 이전 행만 저장)을 사용하여 공간 복잡도를 최적화했습니다.""",
    "graph": """### 3. 트러블슈팅 (Troubleshooting)
- **무한 루프**: `visited` 처리를 큐에 넣을 때 하지 않고 뺄 때 하여 중복 방문이 발생, 시간 초과가 났습니다. 큐에 넣을 때 방문 처리하도록 수정하여 해결했습니다.
- **재귀 깊이**: DFS 사용 시 `RecursionError`가 발생하여 `sys.setrecursionlimit`을 설정하거나 스택을 이용한 반복문으로 변경했습니다.""",
    "math": """### 3. 트러블슈팅 (Troubleshooting)
- **시간 초과**: 단순 반복문으로 구현했다가 시간 초과가 발생했습니다. 수학적 공식을 유도하여 O(1)로 해결하거나, 반복 범위를 `sqrt(N)`까지로 줄여 해결했습니다.
- **오버플로우**: 정수 범위가 커질 수 있음을 간과했습니다. 파이썬은 자동으로 큰 정수를 처리하지만, 로직 상에서 모듈러 연산(`% MOD`)을 중간중간 적용해야 함을 깨달았습니다.""",
    "default": """### 3. 트러블슈팅 (Troubleshooting)
- **예외 케이스**: 입력이 0이거나 1인 경우, 혹은 배열이 비어있는 경우를 고려하지 않아 런타임 에러가 발생했습니다. 조건문을 추가하여 이를 해결했습니다.
- **인덱스 에러**: 배열 접근 시 범위를 벗어나는 실수가 있었습니다. 반복문의 범위를 꼼꼼히 확인하여 수정했습니다."""
}

TROUBLESHOOTING_TEMPLATES_EN = {
    "dp": """### 3. Troubleshooting
- **Recurrence Error**: Initially derived an incorrect recurrence. Fixed it by manually tracing small test cases.
- **Memory Limit**: Encountered MLE with a 2D array. Optimized space complexity using a sliding window approach (keeping only necessary previous rows).""",
    "default": """### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it."""
}

def get_thumbnail(source):
    # Always use platform thumbnails as requested
    if source == "boj":
        return "/assets/img/posts/algo/baekjoon.png"
    else:
        return "/assets/img/posts/algo/leetcode.png"

def analyze_code(code_content, lang="ko"):
    """
    Analyze python code to generate specific insights.
    """
    insights = []
    troubleshooting = []
    
    # Check for comments
    comments = re.findall(r'#\s*(.*)', code_content)
    if comments:
        # Filter out generic comments or encoding declarations
        filtered_comments = [c.strip() for c in comments if not c.startswith("coding:") and len(c) > 5]
        if filtered_comments:
            if lang == "ko":
                insights.append("**주석 기반 설명**:")
            else:
                insights.append("**Code Comments Analysis**:")
            for c in filtered_comments:
                insights.append(f"- {c}")

    # Heuristics
    if "sys.setrecursionlimit" in code_content:
        if lang == "ko":
            troubleshooting.append("- **재귀 깊이**: `sys.setrecursionlimit`을 사용하여 재귀 깊이 제한을 늘려 런타임 에러를 방지했습니다.")
        else:
            troubleshooting.append("- **Recursion Depth**: Increased recursion limit using `sys.setrecursionlimit` to prevent runtime errors.")
            
    if "sys.stdin.readline" in code_content:
        if lang == "ko":
            troubleshooting.append("- **입출력 속도**: `sys.stdin.readline`을 사용하여 대량의 입력을 빠르게 처리하여 시간 초과를 방지했습니다.")
        else:
            troubleshooting.append("- **I/O Speed**: Used `sys.stdin.readline` for fast input processing to avoid TLE.")
            
    if "dp =" in code_content or "dp [" in code_content:
        if lang == "ko":
            insights.append("- **DP 테이블**: 배열을 사용하여 중복 계산을 피하고 이전 상태값을 저장했습니다.")
        else:
            insights.append("- **DP Table**: Used an array to store previous states and avoid redundant calculations.")
            
    if "deque" in code_content:
        if lang == "ko":
            insights.append("- **Deque 활용**: `collections.deque`를 사용하여 큐 연산(삽입/삭제)을 O(1)로 효율적으로 처리했습니다.")
        else:
            insights.append("- **Deque**: Used `collections.deque` for efficient O(1) queue operations.")

    return insights, troubleshooting

def get_approach_text(tags, code_content, lang="ko"):
    tags_lower = [t.lower() for t in tags]
    templates = APPROACH_TEMPLATES if lang == "ko" else APPROACH_TEMPLATES_EN
    
    key = "default"
    if any(t in tags_lower for t in ['dp', 'dynamic programming', '다이나믹 프로그래밍']):
        key = "dp"
    elif any(t in tags_lower for t in ['graph', 'bfs', 'dfs', '그래프']):
        key = "graph"
    elif any(t in tags_lower for t in ['math', '수학', '정수론']):
        key = "math"
    elif any(t in tags_lower for t in ['greedy', '그리디']):
        key = "greedy"
    elif any(t in tags_lower for t in ['search', 'binary search', '이분 탐색']):
        key = "search"
    
    if lang == "en" and key not in templates:
        key = "default"
        
    base_text = templates[key]
    
    # Enhance with code analysis
    insights, _ = analyze_code(code_content, lang)
    if insights:
        if lang == "ko":
            base_text += "\n\n### 코드 분석 (Code Analysis)\n" + "\n".join(insights)
        else:
            base_text += "\n\n### Code Analysis\n" + "\n".join(insights)
            
    return base_text

def get_troubleshooting_text(tags, code_content, lang="ko"):
    tags_lower = [t.lower() for t in tags]
    templates = TROUBLESHOOTING_TEMPLATES if lang == "ko" else TROUBLESHOOTING_TEMPLATES_EN
    
    key = "default"
    if any(t in tags_lower for t in ['dp', 'dynamic programming']):
        key = "dp"
    elif any(t in tags_lower for t in ['graph', 'bfs', 'dfs']):
        key = "graph"
    elif any(t in tags_lower for t in ['math', '수학']):
        key = "math"
        
    if lang == "en" and key not in templates:
        key = "default"
        
    base_text = templates[key]
    
    # Enhance with code analysis
    _, troubleshooting = analyze_code(code_content, lang)
    if troubleshooting:
        base_text += "\n" + "\n".join(troubleshooting)
        
    return base_text

def get_git_date(repo_path, file_path):
    try:
        rel_path = os.path.relpath(file_path, repo_path)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cd", "--date=iso-strict", "--", rel_path],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        date_str = result.stdout.strip()
        if date_str:
            return date_str
    except Exception as e:
        pass
    return datetime.datetime.now().astimezone().isoformat()

def clean_filename(text):
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-').lower()
    return text

def create_post(title, date, categories, tags, description, body, filename, image_path):
    try:
        date_obj = datetime.datetime.fromisoformat(date)
        date_str = date_obj.strftime("%Y-%m-%d")
        front_matter_date = date_obj.strftime("%Y-%m-%d %H:%M:%S %z")
        if not front_matter_date.endswith("00"):
             front_matter_date += "00"
    except:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        front_matter_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0900")

    full_filename = f"{date_str}-{filename}.md"
    file_path = os.path.join(POSTS_DIR, full_filename)
    
    content = f"""---
title: "{title}"
date: {front_matter_date}
categories: {categories}
tags: {tags}
description: "{description}"
image:
  path: {image_path}
  alt: {title}
---

{body}
"""
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Created: {full_filename}")

def process_baekjoon():
    if not os.path.exists(BAEKJOON_DIR):
        print("Baekjoon directory not found.")
        return

    for root, dirs, files in os.walk(BAEKJOON_DIR):
        if ".git" in root:
            continue
        
        if "README.md" in files:
            readme_path = os.path.join(root, "README.md")
            py_files = [f for f in files if f.endswith(".py")]
            if not py_files:
                continue
            
            py_path = os.path.join(root, py_files[0])
            dir_name = os.path.basename(root)
            match = re.match(r"(\d+)\.\s*(.+)", dir_name)
            if match:
                prob_id, prob_title = match.groups()
            else:
                prob_id = "0000"
                prob_title = dir_name

            # FILTER: Skip Hello World and simple problems
            if prob_id == "2557" or "Hello World" in prob_title:
                print(f"Skipping simple problem: {prob_title}")
                continue

            with open(readme_path, "r") as f:
                readme_content = f.read()

            date_match = re.search(r"### 제출 일자\s*\n\s*(.+)", readme_content)
            if date_match:
                date_str = date_match.group(1).strip()
                try:
                    dt = datetime.datetime.strptime(date_str, "%Y년 %m월 %d일 %H:%M:%S")
                    date_iso = dt.strftime("%Y-%m-%dT%H:%M:%S+09:00")
                except:
                    date_iso = get_git_date(os.path.join(TEMP_REPOS, "Algorithm-and-Problem-Solving"), py_path)
            else:
                date_iso = get_git_date(os.path.join(TEMP_REPOS, "Algorithm-and-Problem-Solving"), py_path)

            tags_match = re.search(r"### 분류\s*\n\s*(.+)", readme_content)
            tags = ["Algorithm", "Baekjoon"]
            if tags_match:
                raw_tags = tags_match.group(1).split(",")
                tags.extend([t.strip() for t in raw_tags])

            desc_match = re.search(r"### 문제 설명\s*\n(.+?)(?=### 입력|$)", readme_content, re.DOTALL)
            problem_desc = desc_match.group(1).strip() if desc_match else "문제 링크를 참조하세요."
            
            link_match = re.search(r"\[문제 링크\]\((.+?)\)", readme_content)
            link = link_match.group(1) if link_match else f"https://www.acmicpc.net/problem/{prob_id}"

            with open(py_path, "r") as f:
                code_content = f.read()

            # Generate Content
            approach_text = get_approach_text(tags, code_content, lang="ko")
            troubleshooting_text = get_troubleshooting_text(tags, code_content, lang="ko")
            thumbnail_path = get_thumbnail(source="boj")

            body = f"""## Introduction
백준 온라인 저지(BOJ)의 **[{prob_title}]({link})** 문제 풀이입니다.

## Problem Description
> [문제 링크]({link})

{problem_desc}

## Approach
{approach_text}

{troubleshooting_text}

## Solution
```python
{code_content}
```

## Complexity Analysis
- **Time Complexity**: 문제의 입력 크기와 제한 시간을 고려할 때, 효율적인 알고리즘 선택이 필수적입니다.
- **Space Complexity**: 메모리 제한 내에서 해결할 수 있도록 불필요한 공간 사용을 최소화했습니다.

## Conclusion
문제를 해결하면서 해당 알고리즘에 대한 이해를 높일 수 있었습니다. 다양한 예외 케이스를 고려하는 것이 중요함을 다시 한번 느꼈습니다.
"""
            
            create_post(
                title=f"[BOJ] {prob_id}. {prob_title}",
                date=date_iso,
                categories=["Algorithm", "Baekjoon"],
                tags=tags,
                description=f"백준 {prob_id}번: {prob_title} 풀이",
                body=body,
                filename=f"algo-boj-{prob_id}-{clean_filename(prob_title)}",
                image_path=thumbnail_path
            )

def process_leetcode():
    if not os.path.exists(LEETCODE_DIR):
        print("LeetCode directory not found.")
        return

    for root, dirs, files in os.walk(LEETCODE_DIR):
        if ".git" in root:
            continue
            
        if "README.md" in files:
            readme_path = os.path.join(root, "README.md")
            py_files = [f for f in files if f.endswith(".py")]
            if not py_files:
                continue
            py_path = os.path.join(root, py_files[0])
            
            dir_name = os.path.basename(root)
            match = re.match(r"(\d+)-(.+)", dir_name)
            if match:
                prob_id = str(int(match.group(1)))
                prob_slug = match.group(2)
                prob_title = prob_slug.replace("-", " ").title()
            else:
                prob_id = "0"
                prob_title = dir_name
                prob_slug = dir_name

            # FILTER: Skip simple problems
            if "Hello World" in prob_title:
                continue

            date_iso = get_git_date(LEETCODE_DIR, py_path)

            with open(readme_path, "r") as f:
                readme_content = f.read()

            diff_match = re.search(r"<h3>(\w+)</h3>", readme_content)
            difficulty = diff_match.group(1) if diff_match else "Medium"
            
            tags = ["Algorithm", "LeetCode", difficulty]

            with open(py_path, "r") as f:
                code_content = f.read()

            # Generate Content
            approach_text = get_approach_text(tags, code_content, lang="en")
            troubleshooting_text = get_troubleshooting_text(tags, code_content, lang="en")
            thumbnail_path = get_thumbnail(source="leetcode")

            body = f"""## Introduction
This is a solution for **[{prob_title}](https://leetcode.com/problems/{prob_slug})** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/{prob_slug})

{readme_content}

## Approach
{approach_text}

{troubleshooting_text}

## Solution
```python
{code_content}
```

## Complexity Analysis
- **Time Complexity**: The algorithm is designed to handle the input size efficiently.
- **Space Complexity**: Space usage is optimized to meet the memory constraints.

## Conclusion
This problem provided a good opportunity to practice algorithmic thinking and implementation skills.
"""
            
            create_post(
                title=f"[LeetCode] {prob_id}. {prob_title}",
                date=date_iso,
                categories=["Algorithm", "LeetCode"],
                tags=tags,
                description=f"Solution for LeetCode {prob_id}: {prob_title}",
                body=body,
                filename=f"algo-leetcode-{prob_id.zfill(4)}-{prob_slug}",
                image_path=thumbnail_path
            )

if __name__ == "__main__":
    process_baekjoon()
    process_leetcode()
