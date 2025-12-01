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
            algo_tag = "알고리즘"
            if tags_match:
                raw_tags = tags_match.group(1).split(",")
                tags.extend([t.strip() for t in raw_tags])
                if len(tags) > 2:
                    algo_tag = tags[-1]

            desc_match = re.search(r"### 문제 설명\s*\n(.+?)(?=### 입력|$)", readme_content, re.DOTALL)
            problem_desc = desc_match.group(1).strip() if desc_match else "문제 링크를 참조하세요."
            
            link_match = re.search(r"\[문제 링크\]\((.+?)\)", readme_content)
            link = link_match.group(1) if link_match else f"https://www.acmicpc.net/problem/{prob_id}"

            with open(py_path, "r") as f:
                code_content = f.read()

            # Korean Template
            body = f"""## Introduction
백준 온라인 저지(BOJ)의 **[{prob_title}]({link})** 문제 풀이입니다.

## Problem Description
> [문제 링크]({link})

{problem_desc}

## Approach
이 문제는 **{algo_tag}**을(를) 사용하여 해결할 수 있습니다.

초기에는 문제의 조건을 분석하여 적절한 자료구조나 알고리즘을 선택해야 합니다. {algo_tag}의 특성을 고려하여 효율적인 접근 방식을 고민했습니다.

## Solution
```python
{code_content}
```

## Complexity Analysis
- **Time Complexity**: 문제의 입력 크기와 제한 시간을 고려할 때, 효율적인 알고리즘 선택이 필수적입니다.
- **Space Complexity**: 메모리 제한 내에서 해결할 수 있도록 불필요한 공간 사용을 최소화했습니다.

## Conclusion
문제를 해결하면서 **{algo_tag}**에 대한 이해를 높일 수 있었습니다. 다양한 예외 케이스를 고려하는 것이 중요함을 다시 한번 느꼈습니다.
"""
            
            create_post(
                title=f"[BOJ] {prob_id}. {prob_title}",
                date=date_iso,
                categories=["Algorithm", "Baekjoon"],
                tags=tags,
                description=f"백준 {prob_id}번: {prob_title} 풀이",
                body=body,
                filename=f"algo-boj-{prob_id}-{clean_filename(prob_title)}",
                image_path="/assets/img/posts/algo/baekjoon.png"
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

            date_iso = get_git_date(LEETCODE_DIR, py_path)

            with open(readme_path, "r") as f:
                readme_content = f.read()

            diff_match = re.search(r"<h3>(\w+)</h3>", readme_content)
            difficulty = diff_match.group(1) if diff_match else "Medium"
            
            tags = ["Algorithm", "LeetCode", difficulty]

            with open(py_path, "r") as f:
                code_content = f.read()

            # English Template
            body = f"""## Introduction
This is a solution for **[{prob_title}](https://leetcode.com/problems/{prob_slug})** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/{prob_slug})

{readme_content}

## Approach
The solution is implemented in Python.

Based on the problem constraints and requirements, an efficient approach is needed. The code below demonstrates how to solve the problem within the given limits.

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
                image_path="/assets/img/posts/algo/leetcode.png"
            )

if __name__ == "__main__":
    process_baekjoon()
    process_leetcode()
