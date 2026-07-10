# Contributing to scitechblog

This repository contains the CSMAIR blog, its Jekyll/Chirpy integration, and authoring documentation.

## Before Opening a Change

1. Read the [developer documentation](../docs/README.md).
2. Update from the `master` branch and keep the change focused.
3. Do not copy problem statements, paywalled material, datasets, or third-party figures without redistribution permission.
4. Preserve source attribution and separate measured results from interpretation.

## Validation

Run the checks that match the change:

```bash
npm ci
npm test
npm run build
bash tools/test.sh
```

For post changes, also follow [write-posts.md](../docs/how-to/write-posts.md) and the applicable [post-type guide](../docs/how-to/post-types/algorithm.md). Include the dataset split, seed, dependency versions, and evaluation protocol when reporting experimental results.

## Pull Requests

- Explain the problem, the chosen correction, and how it was verified.
- Link primary sources for factual or technical claims.
- Do not include secrets, personal data, generated caches, or local build output.
- Use a Conventional Commit subject such as `fix(posts): correct FID protocol`.

Repository-specific defects belong in this repository. Upstream Chirpy defects should be reproduced against the upstream theme before being reported to [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy/issues).
