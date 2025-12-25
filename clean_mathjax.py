import re

def clean_mathjax_html(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Regex to find mjx-container and extract the content inside mjx-copytext span
    # Pattern looks for: <mjx-container ...> ... <span ... mjx-copytext ...>(TARGET)</span> ... </mjx-container>
    # We use dotall=True to handle multi-line if necessary, though these seem inline.
    
    pattern = r'<mjx-container[^>]*>.*?<span[^>]*class="[^"]*mjx-copytext[^"]*"[^>]*>(.*?)</span>.*?</mjx-container>'
    
    def replacement(match):
        return match.group(1)
        
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Also clean up any standalone <mjx-assistive-mml> tags if they exist outside container (unlikely but good to be safe)
    # But the pattern above should catch the whole container.
    
    if content != new_content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Cleaned MathJax HTML in {file_path}")
    else:
        print(f"No MathJax HTML found in {file_path}")

if __name__ == "__main__":
    clean_mathjax_html("_posts/2024-10-10-algo-boj-23832-서로소-그래프.md")
