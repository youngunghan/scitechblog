import glob
import re

def enable_math_in_files():
    # Find all markdown files in _posts
    files = glob.glob("_posts/*.md")
    
    for file_path in files:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Check if file contains math delimiters
        if not ("$" in content or "\\(" in content or "\\[" in content):
            continue
            
        # Check if math: true is already present
        if "math: true" in content:
            continue
            
        # Insert math: true before the second ---
        # Regex to find the end of front matter
        match = re.search(r'^---\s*$', content, re.MULTILINE) # First ---
        if match:
            end_match = re.search(r'^---\s*$', content[match.end():], re.MULTILINE) # Second ---
            if end_match:
                insert_pos = match.end() + end_match.start()
                
                # Check if the line before is empty or has content
                # We want to append "math: true\n" before the closing ---
                
                new_content = content[:insert_pos] + "math: true\n" + content[insert_pos:]
                
                with open(file_path, 'w') as f:
                    f.write(new_content)
                print(f"Enabled math in {file_path}")
            else:
                print(f"Skipping {file_path}: No closing front matter found")
        else:
            print(f"Skipping {file_path}: No front matter found")

if __name__ == "__main__":
    enable_math_in_files()
