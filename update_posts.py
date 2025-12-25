import glob
import re

def add_author_to_new_posts():
    """Add author: seoultech to posts missing it."""
    files = glob.glob("_posts/2025-12-24*.md")
    count = 0
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if "author:" in content:
            continue
        
        # Find the closing --- of front matter and insert author before it
        match = re.search(r'^---\s*$', content, re.MULTILINE)
        if match:
            # Find second ---
            second_match = re.search(r'^---\s*$', content[match.end():], re.MULTILINE)
            if second_match:
                insert_pos = match.end() + second_match.start()
                new_content = content[:insert_pos] + "author: seoultech\n" + content[insert_pos:]
                
                with open(file_path, 'w') as f:
                    f.write(new_content)
                print(f"Added author to {file_path}")
                count += 1
    
    print(f"Total files with author added: {count}")

def update_algorithm_thumbnails():
    """Update algorithm post thumbnails to new logos."""
    files = glob.glob("_posts/*algo*.md")
    baekjoon_count = 0
    leetcode_count = 0
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original = content
        
        # Update Baekjoon posts
        if "boj" in file_path.lower() or "Baekjoon" in content:
            content = re.sub(
                r'path:\s*assets/img/posts/algo/baekjoon\.png',
                'path: assets/img/posts/algo/baekjoon_new.png',
                content
            )
            if content != original:
                baekjoon_count += 1
        
        # Update LeetCode posts
        if "leetcode" in file_path.lower() or "LeetCode" in content:
            content = re.sub(
                r'path:\s*assets/img/posts/algo/leetcode\.png',
                'path: assets/img/posts/algo/leetcode_new.png',
                content
            )
            if content != original:
                leetcode_count += 1
        
        if content != original:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Updated thumbnail in {file_path}")
    
    print(f"Baekjoon thumbnails updated: {baekjoon_count}")
    print(f"LeetCode thumbnails updated: {leetcode_count}")

def remove_leetcode_duplicate_links():
    """Remove duplicate problem links from LeetCode posts."""
    files = glob.glob("_posts/*leetcode*.md")
    count = 0
    
    for file_path in files:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        modified = False
        
        for line in lines:
            # Check for the specific pattern: > [문제 링크](...) or similar blockquote link
            if line.strip().startswith("> [") and ("leetcode.com" in line or "문제 링크" in line):
                modified = True
                continue
            new_lines.append(line)
        
        if modified:
            with open(file_path, 'w') as f:
                f.writelines(new_lines)
            print(f"Removed duplicate link from {file_path}")
            count += 1
    
    print(f"LeetCode files cleaned: {count}")

if __name__ == "__main__":
    print("=== Adding author to new posts ===")
    add_author_to_new_posts()
    print()
    print("=== Updating algorithm thumbnails ===")
    update_algorithm_thumbnails()
    print()
    print("=== Removing LeetCode duplicate links ===")
    remove_leetcode_duplicate_links()
