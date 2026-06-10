---
title: "Resolving Python Import Issues in a Frequency Analysis Project"
date: 2024-11-15 00:00:00 +0900
categories: [Python, Development]
tags: [python, import, pythonpath, module, project-structure]
description: "Resolving ModuleNotFoundError in a src-layout Python project using PYTHONPATH, python -m, and editable installs."
author: seoultech
image:
  path: assets/img/posts/python-import/path_problem.png
  alt: Python Import Path Problem
---

## Project Structure

```
vision-ml-project/
├── src/
│   └── vision_utils/
│       ├── __init__.py
│       ├── preprocessing/
│       │   ├── __init__.py
│       │   ├── augmentation.py
│       │   └── transforms.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── network.py
│       └── train.py
├── tests/
├── setup.py
└── README.md
```

## The Challenge

When trying to run the training script directly:

```bash
python /path/to/vision-ml-project/src/vision_utils/train.py --data-dir /path/to/dataset
```

We encounter this error:
```python
Traceback (most recent call last):
  File "train.py", line 3, in <module>
    from vision_utils.preprocessing import transforms
ModuleNotFoundError: No module named 'vision_utils'
```

## Root Cause Analysis

**Python's Module Search Behavior:**
- Python first looks in the directory containing the executed script
- Then searches through PYTHONPATH directories
- Finally checks installed packages

When running the script directly, Python cannot find the `vision_utils` package because the `src` directory is not in its search path.

## Solution Implementation

### Method 1: Using PYTHONPATH
```bash
export PYTHONPATH="/path/to/vision-ml-project/src:$PYTHONPATH"
python src/vision_utils/train.py --data-dir /path/to/dataset
```

### Method 2: Module-style Execution
```bash
python -m vision_utils.train --data-dir /path/to/dataset
```

> **Caveat:** `-m` only works when `src/` is on the path. Since the package lives under `src/`, running this from the project root raises the same `ModuleNotFoundError`. Run it from inside `src/`, or—better—after `pip install -e .` (see Method 3), so that `vision_utils` is importable from anywhere.
{: .prompt-warning }

### Method 3: Development Installation
```bash
# From project root
pip install -e .
```

## Best Practices

1. **Project Structure**
   - Keep all source code under `src/`
   - Use meaningful package names
   - Include `__init__.py` files

2. **Import Style**
   ```python
   # Preferred
   from vision_utils.preprocessing import transforms
   
   # Avoid
   from ..preprocessing import transforms
   ```

3. **Development Setup**
   - Use virtual environments
   - Install package in editable mode
   - Document dependencies properly

## Key Learnings

1. **Understanding Python's import system is crucial**
   - The directory from which you run a script matters
   - PYTHONPATH affects module resolution
   - Package structure should be well-planned

2. **Project structure affects import behavior**
   - Proper `__init__.py` usage is essential
   - Absolute imports are more maintainable
   - src layout helps avoid import conflicts

3. **Development workflow optimization**
   - Editable installs (`pip install -e .`) simplify development
   - Virtual environments prevent dependency conflicts
   - Consistent import patterns improve code maintainability

## Recommended Solution

For most projects, **Method 3 (Development Installation)** is the best approach:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Now you can run from anywhere
python -m vision_utils.train
```

Even cleaner: declare a `console_scripts` entry point in `setup.py` (e.g. `vision-train = vision_utils.train:main`), so after `pip install -e .` you can simply run `vision-train` directly from any directory.

This method:
-  Works from any directory
-  Doesn't require environment variable manipulation
-  Matches production installation behavior
-  Simplifies testing and development
