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

# Tag-based Content Templates
APPROACH_TEMPLATES = {
    "dp": "이 문제는 **Dynamic Programming (DP)**을 사용하여 해결할 수 있습니다.\n\n문제의 구조를 살펴보면 작은 부분 문제들의 해가 전체 문제의 해를 구성하는 **Optimal Substructure**를 가지고 있으며, 동일한 부분 문제가 반복되는 **Overlapping Subproblems** 특성이 보입니다.\n\n따라서 점화식을 세워 바텀업(Bottom-up) 또는 탑다운(Top-down) 방식으로 접근하는 것이 효율적입니다.",
    "graph": "이 문제는 **그래프 탐색 (Graph Traversal)** 알고리즘을 적용해야 합니다.\n\n노드와 간선의 관계를 파악하고, **BFS (너비 우선 탐색)** 또는 **DFS (깊이 우선 탐색)**를 사용하여 연결된 요소들을 순회하거나 최단 경로를 찾아야 합니다. 문제의 조건에 따라 적절한 탐색 방법을 선택하는 것이 중요합니다.",
    "math": "이 문제는 **수학적 직관 (Mathematical Insight)**이 필요한 유형입니다.\n\n단순한 시뮬레이션보다는 수식으로 정리하거나, 정수론/조합론 등의 성질을 활용하여 계산 복잡도를 줄이는 것이 핵심입니다. 문제에 주어진 수의 범위나 규칙성을 주의 깊게 관찰해야 합니다.",
    "greedy": "이 문제는 **그리디 알고리즘 (Greedy Algorithm)**으로 접근할 수 있습니다.\n\n매 순간 최적이라고 생각되는 선택을 하는 것이 전체적으로도 최적의 해를 보장하는지 확인해야 합니다. 탐욕적 선택 속성(Greedy Choice Property)이 성립하는지 고민해보았습니다.",
    "string": "이 문제는 **문자열 처리 (String Manipulation)** 능력을 요구합니다.\n\n문자열의 패턴을 분석하거나, 특정 조건에 맞는 부분 문자열을 찾는 과정이 필요합니다. 효율적인 문자열 연산을 위해 적절한 라이브러리나 알고리즘을 활용해야 합니다.",
    "search": "이 문제는 **탐색 (Search)** 기법, 특히 **이분 탐색 (Binary Search)** 등을 활용할 수 있습니다.\n\n탐색 범위를 절반씩 줄여가며 원하는 값을 찾는 방식으로, O(log N)의 시간 복잡도로 효율적인 해결이 가능합니다. 결정 문제로 변환하여 접근하는 아이디어가 필요할 수 있습니다.",
    "default": "이 문제는 문제의 요구사항을 정확히 구현하는 **구현 (Implementation)** 능력이 중요합니다.\n\n특별한 알고리즘보다는 문제에서 주어진 조건을 빠짐없이 코드로 옮기는 과정이 필요하며, 예외 케이스 처리에 유의해야 합니다."
}

APPROACH_TEMPLATES_EN = {
    "dp": "This problem can be solved using **Dynamic Programming (DP)**.\n\nThe problem exhibits **Optimal Substructure**, where the solution to the problem can be constructed from solutions to its subproblems, and **Overlapping Subproblems**, where the same subproblems are solved multiple times.\n\nTherefore, defining a recurrence relation and using a Bottom-up or Top-down approach is efficient.",
    "graph": "This problem requires a **Graph Traversal** algorithm.\n\nWe need to model the problem as nodes and edges and use **BFS (Breadth-First Search)** or **DFS (Depth-First Search)** to traverse connected components or find the shortest path. Choosing the right traversal method based on the constraints is key.",
    "math": "This problem requires **Mathematical Insight**.\n\nInstead of naive simulation, we should look for mathematical properties (Number Theory, Combinatorics) to reduce computational complexity. Observing patterns and constraints is crucial.",
    "greedy": "This problem can be approached using a **Greedy Algorithm**.\n\nWe need to verify if making the locally optimal choice at each step leads to the global optimum. Checking for the Greedy Choice Property is essential.",
    "string": "This problem involves **String Manipulation**.\n\nAnalyzing string patterns or finding substrings satisfying certain conditions is required. Using efficient string operations or libraries is important.",
    "search": "This problem can be solved using **Search** techniques, such as **Binary Search**.\n\nBy reducing the search space by half at each step, we can achieve O(log N) time complexity. Converting the problem into a decision problem might be a useful strategy.",
    "default": "This problem focuses on **Implementation** skills.\n\nThe key is to translate the problem requirements into code accurately, handling all edge cases and constraints without relying on complex algorithms."
}

def get_thumbnail(tags, source):
    tags_lower = [t.lower() for t in tags]
    
    # Prioritize specific thumbnails if available
    if any(t in tags_lower for t in ['math', '수학', '정수론', '조합론', 'geometry']):
        return "/assets/img/posts/algo/math.png"
    elif any(t in tags_lower for t in ['dp', 'dynamic programming', '다이나믹 프로그래밍']):
        return "/assets/img/posts/algo/dp.png"
    
    # Fallback to platform thumbnails
    if source == "boj":
        return "/assets/img/posts/algo/baekjoon.png"
    else:
        return "/assets/img/posts/algo/leetcode.png"

def get_approach_text(tags, lang="ko"):
    tags_lower = [t.lower() for t in tags]
    templates = APPROACH_TEMPLATES if lang == "ko" else APPROACH_TEMPLATES_EN
    
    if any(t in tags_lower for t in ['dp', 'dynamic programming', '다이나믹 프로그래밍']):
        return templates["dp"]
    elif any(t in tags_lower for t in ['graph', 'bfs', 'dfs', '그래프', '너비 우선 탐색', '깊이 우선 탐색']):
        return templates["graph"]
    elif any(t in tags_lower for t in ['math', '수학', '정수론', '조합론']):
        return templates["math"]
    elif any(t in tags_lower for t in ['greedy', '그리디']):
        return templates["greedy"]
    elif any(t in tags_lower for t in ['string', '문자열']):
        return templates["string"]
    elif any(t in tags_lower for t in ['search', 'binary search', '이분 탐색', '탐색']):
        return templates["search"]
    else:
        return templates["default"]

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
            approach_text = get_approach_text(tags, lang="ko")
            thumbnail_path = get_thumbnail(tags, source="boj")

            body = f"""## Introduction
백준 온라인 저지(BOJ)의 **[{prob_title}]({link})** 문제 풀이입니다.

## Problem Description
> [문제 링크]({link})

{problem_desc}

## Approach
{approach_text}

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
            approach_text = get_approach_text(tags, lang="en")
            thumbnail_path = get_thumbnail(tags, source="leetcode")

            body = f"""## Introduction
This is a solution for **[{prob_title}](https://leetcode.com/problems/{prob_slug})** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/{prob_slug})

{readme_content}

## Approach
{approach_text}

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
