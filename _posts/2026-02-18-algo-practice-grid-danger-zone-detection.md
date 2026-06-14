---
title: "Grid Adjacent Danger Zone Detection"
date: 2026-02-18 15:50:00 +0900
categories: ['Algorithm', 'Practice']
tags: ['Algorithm', 'Practice', 'Implementation', 'Simulation', '2D Array']
description: "Solution to Grid Adjacent Danger Zone Detection"
image:
  path: assets/img/posts/algo/math.png
  alt: "Grid Adjacent Danger Zone Detection"
author: seoultech
math: true
mermaid: true
---

## Problem

You are given an $N \times M$ grid. Each cell of the grid is either marked as a **danger zone** or is empty.

- `0`: a safe, empty cell.
- `-1`: a danger zone.
- A **warning sign** can be placed on an empty cell, and the number on the sign equals the count of danger zones among the cell's **8 neighbors** (up, down, left, right, and the diagonals).

After placing warning signs on every empty cell, compute the **total sum of the numbers on all the signs**.

- $1 \le N, M \le 1{,}000$

```
Input:
4 4
0 0 0 0
0 0 -1 0
0 0 0 0
-1 0 0 0

Output:
11
```

---

## Approach

There are two equivalent ways to count the answer:

1. **Cell-centered counting**: for each empty cell, scan its 8 neighbors and count danger zones.
2. **Danger-centered counting**: for each danger zone, add +1 to every adjacent empty cell.

Both approaches must read the whole $N \times M$ grid, so their input cost is $O(NM)$. The difference is the number of 8-directional neighbor scans after the grid has been read:

- cell-centered counting scans around empty cells,
- danger-centered counting scans around danger zones.

That constant factor matters when one class is rare. A quick $1000 \times 1000$ benchmark illustrates the gap:

| Case | Cell-centered | Danger-centered |
|---|---:|---:|
| 100 danger cells | 0.87s | 0.03s |
| Checkerboard danger cells | 0.48s | 0.53s |

These are local CPython measurements, so the absolute seconds depend on hardware and Python version. The useful signal is the relative cost: sparse danger zones favor the danger-centered scan.

So the best production choice depends on the input distribution. If danger zones are sparse, danger-centered counting is usually faster. In this post, I use the cell-centered solution because it directly matches the problem statement and is easier to explain. The same boundary-check pattern applies to both.

In the all-empty worst case, the cell-centered Python solution still performs about $8 \times 10^6$ neighbor checks for a $1000 \times 1000$ grid. On a slower judge, the margin can be tight, so fast input and avoiding extra per-cell work are worth keeping.

---

## Key Insight

The core of this problem is the **8-directional search pattern on a 2D grid**.

> If you predefine **direction vectors**, you can handle all 8 directions cleanly with a single loop.

```python
directions = (
    (-1, 0), (1, 0), (0, -1), (0, 1),
    (-1, -1), (-1, 1), (1, -1), (1, 1),
)
```

For each cell $(r, c)$:
1.  If it is a danger zone (`-1`), **skip it**.
2.  Otherwise, check the 8 neighboring cells.
3.  Add +1 to the total for each neighboring danger zone (`-1`).

---

## Step-by-Step Analysis

A $4 \times 4$ grid:

| | C0 | C1 | C2 | C3 |
|---|---|---|---|---|
| **R0** | 0 | 0 | 0 | 0 |
| **R1** | 0 | 0 | -1 | 0 |
| **R2** | 0 | 0 | 0 | 0 |
| **R3** | -1 | 0 | 0 | 0 |

```mermaid
flowchart TD
    A["Iterate all N x M cells"] --> B{"Danger zone?"}
    B -->|Yes| Skip["Skip this cell"]
    B -->|No| C["Check adjacent cells in 8 dirs"]
    C --> D["Add +1 for each adjacent danger"]
    D --> E["Next cell"]
    Skip --> E
    E --> F["All cells done"]
    F --> G["Output total sum"]
    style G fill:#90EE90
    style Skip fill:#ffaaaa
```

After filling in the warning sign numbers:

| | C0 | C1 | C2 | C3 |
|---|---|---|---|---|
| **R0** | 0 | 1 | 1 | 1 |
| **R1** | 0 | 1 | **-1** | 1 |
| **R2** | 1 | 2 | 1 | 1 |
| **R3** | **-1** | 1 | 0 | 0 |

- For example, (R2, C1) = 2 because among its 8 neighbors are (R1, C2)=-1 and (R3, C0)=-1, for a total of 2 danger zones.

Total sum = $0+1+1+1 + 0+1+1 + 1+2+1+1 + 1+0+0 = 11$

---

## Solution

```python
import sys


def main() -> None:
    """Read the input, compute the total sum of the warning sign numbers, and print it."""

    # Step 1: read the input with fast IO
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])

    board: list[list[int]] = []
    index = 2
    for _ in range(n):
        row: list[int] = [int(value) for value in data[index:index + m]]
        board.append(row)
        index += m

    # Step 2: define the direction vectors for the 8-directional search
    directions: tuple[tuple[int, int], ...] = (
        (-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1),
    )

    # Step 3: iterate over each cell to compute the warning sign numbers
    total_warning_count: int = 0

    for row_index in range(n):
        current_row = board[row_index]
        for col_index in range(m):
            # Skip danger zones (-1).
            if current_row[col_index] == -1:
                continue

            # Count the danger zones among the current cell's 8 neighbors.
            for d_row, d_col in directions:
                neighbor_row: int = row_index + d_row
                neighbor_col: int = col_index + d_col

                # If the neighboring cell is in bounds and dangerous, increment the total.
                if 0 <= neighbor_row < n and 0 <= neighbor_col < m and board[neighbor_row][neighbor_col] == -1:
                    total_warning_count += 1

    print(total_warning_count)


if __name__ == "__main__":
    main()
```

---

## Complexity

- **Time Complexity**: $O(N \times M)$
    - The cell-centered solution iterates over every cell, performing at most 8 constant-time operations for each empty cell.
    - More precisely, $O(8 \times N \times M) = O(NM)$.
    - With danger-centered counting, the input read is still $O(NM)$, but the neighbor scan cost becomes proportional to the number of danger zones.
- **Space Complexity**: $O(NM)$
    - This implementation stores the whole grid for clear neighbor lookup.
    - A streaming cell-centered variant can reduce auxiliary storage to $O(M)$ because each cell only needs the previous, current, and next rows.

---

## Key Takeaways

| Point | Description |
|-------|-------------|
| **Direction Vector** | Predefining direction vectors keeps the code concise for 8-directional (or 4-directional) searches |
| **Boundary Check** | Index range checks are essential in grid problems; master the `0 <= r < n` and `0 <= c < m` pattern |
| **Dual Perspective** | Cell-centered and danger-centered counting are equivalent, but danger-centered counting is faster when danger zones are sparse |
