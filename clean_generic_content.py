import glob
import re

# Generic content to remove from LeetCode posts
LEETCODE_GENERIC = """### 1. Problem Analysis
This problem focuses on **Implementation** skills.
The key is to carefully read the problem statement and translate the requirements into code accurately.
Using appropriate data structures (List, Dictionary, Set) to optimize complexity is crucial.

### 2. Solution Idea
1.  **Input Parsing**: Handle the input format as specified.
2.  **Logic Design**: Break down the requirements into steps.
3.  **Edge Cases**: Handle boundary cases and special conditions."""

# Generic content to remove from BOJ posts
BOJ_GENERIC = """### 1. 문제 분석 (Problem Analysis)
이 문제는 **수학적 성질 (Mathematical Property)**을 활용해야 합니다.
단서는 입력 크기(N)가 매우 크거나, 특정 패턴/규칙이 보인다는 점입니다.
단순 시뮬레이션으로는 시간 초과(TLE)가 발생할 가능성이 높으므로, 수식으로 정리하여 O(1) 또는 O(log N)으로 줄여야 합니다.

### 2. 해결 아이디어 (Solution Idea)
1.  **규칙 찾기**: 작은 케이스(N=1, 2, 3...)를 직접 계산해보며 규칙성을 발견합니다.
2.  **수식화**: 발견한 규칙을 일반항이나 점화식으로 표현합니다.
3.  **알고리즘 적용**: 정수론(소수 판별, 최대공약수), 조합론, 기하학 등의 이론을 적용합니다."""

def clean_leetcode_posts():
    """Remove generic approach sections from LeetCode posts."""
    files = glob.glob("_posts/*leetcode*.md")
    count = 0
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original = content
        
        # Remove the generic LeetCode approach section
        content = content.replace(LEETCODE_GENERIC, "")
        
        # Also remove partial matches for the generic troubleshooting section
        troubleshooting = """### 3. Troubleshooting
- **Edge Cases**: Missed cases where input is 0, 1, or empty, causing runtime errors. Added conditional checks to handle them.
- **Index Error**: Accessed array out of bounds. Carefully reviewed loop boundaries to fix it."""
        content = content.replace(troubleshooting, "")
        
        if content != original:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Cleaned {file_path}")
            count += 1
    
    print(f"LeetCode files cleaned: {count}")

def clean_boj_posts():
    """Remove generic approach sections from BOJ posts."""
    files = ["_posts/2024-10-09-algo-boj-11401-이항-계수-3.md", "_posts/2024-10-10-algo-boj-23832-서로소-그래프.md"]
    count = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            continue
        
        original = content
        
        # Remove the generic BOJ approach section
        content = content.replace(BOJ_GENERIC, "")
        
        # Remove generic troubleshooting
        troubleshooting = """### 3. 트러블슈팅 (Troubleshooting)
- **시간 초과**: 단순 반복문으로 구현했다가 시간 초과가 발생했습니다. 수학적 공식을 유도하여 O(1)로 해결하거나, 반복 범위를 `sqrt(N)`까지로 줄여 해결했습니다.
- **오버플로우**: 정수 범위가 커질 수 있음을 간과했습니다. 파이썬은 자동으로 큰 정수를 처리하지만, 로직 상에서 모듈러 연산(`% MOD`)을 중간중간 적용해야 함을 깨달았습니다.
- **입출력 속도**: `sys.stdin.readline`을 사용하여 대량의 입력을 빠르게 처리하여 시간 초과를 방지했습니다."""
        content = content.replace(troubleshooting, "")
        
        # Also try partial troubleshooting
        troubleshooting2 = """### 3. 트러블슈팅 (Troubleshooting)
- **시간 초과**: 단순 반복문으로 구현했다가 시간 초과가 발생했습니다. 수학적 공식을 유도하여 O(1)로 해결하거나, 반복 범위를 `sqrt(N)`까지로 줄여 해결했습니다.
- **오버플로우**: 정수 범위가 커질 수 있음을 간과했습니다. 파이썬은 자동으로 큰 정수를 처리하지만, 로직 상에서 모듈러 연산(`% MOD`)을 중간중간 적용해야 함을 깨달았습니다."""
        content = content.replace(troubleshooting2, "")
        
        if content != original:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Cleaned {file_path}")
            count += 1
    
    print(f"BOJ files cleaned: {count}")

if __name__ == "__main__":
    print("=== Cleaning LeetCode posts ===")
    clean_leetcode_posts()
    print()
    print("=== Cleaning BOJ posts ===")
    clean_boj_posts()
