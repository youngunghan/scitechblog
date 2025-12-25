import glob
import re

def remove_redundant_links():
    # Find all markdown files in _posts
    files = glob.glob("_posts/*.md")
    count = 0
    
    for file_path in files:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        new_lines = []
        modified = False
        
        for line in lines:
            # Check for the specific pattern: > [문제 링크](...)
            if line.strip().startswith("> [문제 링크](") and line.strip().endswith(")"):
                modified = True
                continue
            new_lines.append(line)
            
        if modified:
            with open(file_path, 'w') as f:
                f.writelines(new_lines)
            print(f"Removed redundant link from {file_path}")
            count += 1
            
    print(f"Total files modified: {count}")

if __name__ == "__main__":
    remove_redundant_links()
