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
        # Get the relative path for git command
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
        print(f"Error getting git date for {file_path}: {e}")
    
    # Fallback to current time
    return datetime.datetime.now().astimezone().isoformat()

def clean_filename(text):
    # Remove special chars, replace spaces with hyphens, lowercase
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-').lower()
    return text

def create_post(title, date, categories, tags, description, body, filename, image_path):
    # Ensure date is in correct format for Jekyll filename (YYYY-MM-DD)
    try:
        date_obj = datetime.datetime.fromisoformat(date)
        date_str = date_obj.strftime("%Y-%m-%d")
        # Format date for front matter: YYYY-MM-DD HH:MM:SS +0900
        front_matter_date = date_obj.strftime("%Y-%m-%d %H:%M:%S %z")
        if not front_matter_date.endswith("00"): # simple check for timezone
             front_matter_date += "00" # approximate if missing
    except:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        front_matter_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0900")

    full_filename = f"{date_str}-{filename}.md"
    file_path = os.path.join(POSTS_DIR, full_filename)
    
    # Always overwrite to update thumbnails
    
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
        
        # Check if this is a problem directory (contains README.md and a .py file)
        if "README.md" in files:
            readme_path = os.path.join(root, "README.md")
            py_files = [f for f in files if f.endswith(".py")]
            if not py_files:
                continue
            
            py_path = os.path.join(root, py_files[0])
            
            # Parse Directory Name: "10422. 괄호" -> ID: 10422, Title: 괄호
            dir_name = os.path.basename(root)
            match = re.match(r"(\d+)\.\s*(.+)", dir_name)
            if match:
                prob_id, prob_title = match.groups()
            else:
                prob_id = "0000"
                prob_title = dir_name

            # Read README
            with open(readme_path, "r") as f:
                readme_content = f.read()

            # Extract Date
            date_match = re.search(r"### 제출 일자\s*\n\s*(.+)", readme_content)
            if date_match:
                date_str = date_match.group(1).strip()
                # Convert "2024년 10월 18일 22:13:09" to ISO
                try:
                    dt = datetime.datetime.strptime(date_str, "%Y년 %m월 %d일 %H:%M:%S")
                    date_iso = dt.strftime("%Y-%m-%dT%H:%M:%S+09:00")
                except:
                    date_iso = get_git_date(os.path.join(TEMP_REPOS, "Algorithm-and-Problem-Solving"), py_path)
            else:
                date_iso = get_git_date(os.path.join(TEMP_REPOS, "Algorithm-and-Problem-Solving"), py_path)

            # Extract Tags
            tags_match = re.search(r"### 분류\s*\n\s*(.+)", readme_content)
            tags = ["Algorithm", "Baekjoon"]
            if tags_match:
                raw_tags = tags_match.group(1).split(",")
                tags.extend([t.strip() for t in raw_tags])

            # Extract Description (Simple extraction)
            # We want content after ### 문제 설명
            desc_match = re.search(r"### 문제 설명\s*\n(.+?)(?=### 입력|$)", readme_content, re.DOTALL)
            problem_desc = desc_match.group(1).strip() if desc_match else "See Problem Link."
            
            # Link
            link_match = re.search(r"\[문제 링크\]\((.+?)\)", readme_content)
            link = link_match.group(1) if link_match else f"https://www.acmicpc.net/problem/{prob_id}"

            # Read Code
            with open(py_path, "r") as f:
                code_content = f.read()

            # Construct Body
            body = f"""## Introduction
This is a solution for **[{prob_title}]({link})** on Baekjoon Online Judge.

## Problem Description
> [Problem Link]({link})

{problem_desc}

## Approach
<!-- TODO: Describe your thought process here. (e.g., "At first I thought..., but...") -->
The solution uses **{tags[-1] if len(tags)>2 else 'standard algorithm'}**.
See the code below for details.

## Solution
```python
{code_content}
```

## Complexity Analysis
- **Time Complexity**: <!-- TODO: O(?) -->
- **Space Complexity**: <!-- TODO: O(?) -->

## Conclusion
<!-- TODO: Add insights or what you learned. -->
Solved successfully.
"""
            
            create_post(
                title=f"[BOJ] {prob_id}. {prob_title}",
                date=date_iso,
                categories=["Algorithm", "Baekjoon"],
                tags=tags,
                description=f"Solution for Baekjoon {prob_id}: {prob_title}",
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
            # "0001-two-sum" -> ID: 1, Title: Two Sum
            match = re.match(r"(\d+)-(.+)", dir_name)
            if match:
                prob_id = str(int(match.group(1))) # remove leading zeros
                prob_slug = match.group(2)
                prob_title = prob_slug.replace("-", " ").title()
            else:
                prob_id = "0"
                prob_title = dir_name
                prob_slug = dir_name

            # Date from git
            date_iso = get_git_date(LEETCODE_DIR, py_path)

            # Read README
            with open(readme_path, "r") as f:
                readme_content = f.read()

            # Extract Difficulty (e.g. <h3>Easy</h3>)
            diff_match = re.search(r"<h3>(\w+)</h3>", readme_content)
            difficulty = diff_match.group(1) if diff_match else "Medium"
            
            tags = ["Algorithm", "LeetCode", difficulty]

            # Read Code
            with open(py_path, "r") as f:
                code_content = f.read()

            # Construct Body
            body = f"""## Introduction
This is a solution for **[{prob_title}](https://leetcode.com/problems/{prob_slug})** on LeetCode.

## Problem Description
> [Problem Link](https://leetcode.com/problems/{prob_slug})

{readme_content}

## Approach
<!-- TODO: Describe your thought process here. -->
The solution is implemented in Python.

## Solution
```python
{code_content}
```

## Complexity Analysis
- **Time Complexity**: <!-- TODO: O(?) -->
- **Space Complexity**: <!-- TODO: O(?) -->

## Conclusion
<!-- TODO: Add insights or what you learned. -->
Solved successfully.
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
