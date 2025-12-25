import glob
import re

def remove_leetcode_duplicate_headers():
    """Remove duplicate <h2><a>Problem Title</a></h2> headers from LeetCode posts."""
    files = glob.glob("_posts/*leetcode*.md")
    count = 0
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
        
        original = content
        
        # Pattern: <h2><a href="...">123. Problem Title</a></h2><h3>Difficulty</h3><hr>
        # This removes the entire <h2>...</h2><h3>...</h3><hr> block at the start of Problem Description
        pattern = r'<h2><a href="[^"]*">[^<]*</a></h2>(<h3>[^<]*</h3>)?(<hr>)?'
        content = re.sub(pattern, '', content)
        
        if content != original:
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"Removed duplicate header from {file_path}")
            count += 1
    
    print(f"Total files modified: {count}")

if __name__ == "__main__":
    remove_leetcode_duplicate_headers()
