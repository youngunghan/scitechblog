import glob
import yaml
import re

def parse_front_matter(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    
    try:
        fm = yaml.safe_load(match.group(1))
        return fm
    except:
        return None

def check_structure(file_path, category):
    with open(file_path, 'r') as f:
        content = f.read()
    
    if "algo" in file_path or "leetcode" in file_path or "boj" in file_path:
        required = ["## Problem", "## Solution", "## Complexity"]
    elif "review" in file_path:
        required = ["## Introduction", "## Conclusion"]
    else:
        required = ["## Introduction", "## Conclusion"] # Generic check
        
    missing = [req for req in required if req not in content and req.replace("## ", "# ") not in content]
    return missing

def generate_report():
    files = sorted(glob.glob("_posts/*.md"))
    
    report = """# Blog Post Quality Audit Report

## 1. Blog Post Characteristics & Standards

### Common Standards (All Posts)
- **Front Matter**: Title, Date, Categories, Tags, Image (Relative path).
- **Structure**: Clear headers, Intro/Conclusion.

### Category Standards
- **Algorithm**: Problem, Approach, Solution, Complexity.
- **Review**: Abstract, Method, Experiments.
- **Troubleshooting**: Problem, Root Cause, Solution.

---

## 2. Evaluation Results

| Date | File | Category | Image Path | Structure | Status |
|------|------|----------|------------|-----------|--------|
"""
    
    for file_path in files:
        fm = parse_front_matter(file_path)
        filename = file_path.split('/')[-1]
        date = filename[:10]
        
        if not fm:
            report += f"| {date} | `{filename}` | N/A | ❌ Invalid YAML | N/A | 🔴 Fail |\n"
            continue
            
        # Category
        cats = fm.get('categories', [])
        cat_str = ", ".join(cats) if isinstance(cats, list) else str(cats)
        
        # Image Check
        img = fm.get('image', {})
        if not img:
            img_status = "❌ Missing"
        elif isinstance(img, dict):
            path = img.get('path', '')
            if path.startswith('/'):
                img_status = "❌ Absolute Path"
            elif not path.startswith('assets/img/'):
                img_status = f"⚠️ Unusual Path (`{path}`)"
            else:
                img_status = "✅ Valid"
        else:
            img_status = "❌ Invalid Format"
            
        # Structure Check
        missing_sections = check_structure(file_path, cat_str)
        if missing_sections:
            struct_status = f"⚠️ Missing: {', '.join(missing_sections)}"
        else:
            struct_status = "✅ Valid"
            
        # Overall Status
        if "❌" in img_status:
            status = "🔴 Fail"
        elif "⚠️" in img_status or "⚠️" in struct_status:
            status = "zk Warning"
        else:
            status = "🟢 Pass"
            
        report += f"| {date} | `{filename}` | {cat_str} | {img_status} | {struct_status} | {status} |\n"

    with open("/root/.gemini/antigravity/brain/a8ec6fdd-de89-4479-8849-0cadae1999aa/blog_audit_report.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    generate_report()
