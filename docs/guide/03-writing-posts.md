# 03. 글 작성 규칙

새 글은 [_posts/](../../_posts/)에 Markdown 파일로 추가합니다. Chirpy의 글 작성 규칙을 따르되, 이 블로그에서 실제로 쓰는 관례를 정리합니다.

## 파일명 규칙

```text
YYYY-MM-DD-<주제 슬러그>.md
```

- 날짜 접두사는 게시일이며 정렬·permalink에 사용됩니다.
- 슬러그는 카테고리/소분류를 앞에 두는 관례를 씁니다. 예:
  - `2025-09-12-algo-leetcode-0003-longest-substring-without-repeating-characters.md`
  - `2024-10-10-algo-boj-23832-서로소-그래프.md`
  - `2025-11-30-protein-variant-classification-esm2.md`
  - `2025-12-01-troubleshooting-latex-rendering.md`
- 한글 슬러그도 허용됩니다(백준 글 다수). 영문/숫자 슬러그가 URL상 안전합니다.

글의 최종 URL은 [_config.yml](../../_config.yml)의 `defaults`에 정의된 `permalink: /posts/:title/`를 따릅니다. 여기서 `:title`은 파일명에서 날짜를 뗀 슬러그를 가리킵니다(예: `2025-09-12-algo-leetcode-0003-...md` → `/posts/algo-leetcode-0003-.../`).

## Front matter 스키마

글 맨 위 `---` 사이에 YAML front matter를 둡니다. 실제 사용 예:

```yaml
---
title: "[LeetCode] 3. Longest Substring Without Repeating Characters"
date: 2025-09-12 18:16:57 +0900
categories: ['Algorithm', 'LeetCode']
tags: ['Algorithm', 'LeetCode', 'Medium', 'Sliding Window', 'Hash Table']
description: "Solution for LeetCode 3: Longest Substring Without Repeating Characters"
image:
  path: assets/img/posts/algo/leetcode_new.png
  alt: "[LeetCode] 3. Longest Substring Without Repeating Characters"
author: seoultech
math: true
mermaid: true
---
```

필드별 의미:

| 필드 | 필수 | 설명 |
| --- | --- | --- |
| `title` | 권장 | 글 제목. 대괄호를 포함하면 따옴표로 감쌉니다. |
| `date` | 권장 | `YYYY-MM-DD HH:MM:SS +0900`(KST). 정렬·표시에 사용 |
| `categories` | 권장 | 계층 카테고리. 보통 2단계 리스트(`[대분류, 소분류]`) |
| `tags` | 권장 | 자유 태그 리스트. 소문자/혼합 모두 사용됨 |
| `description` | 선택 | 목록·SEO·피드에 쓰이는 요약 |
| `image.path` / `image.alt` | 선택 | 대표(썸네일) 이미지 경로와 대체 텍스트 |
| `author` | 선택 | `_data/authors.yml`의 키. 보통 `seoultech` |
| `math` | 선택 | `true`면 MathJax 수식 렌더링 활성화 |
| `mermaid` | 선택 | `true`면 Mermaid 다이어그램 활성화 |

> `layout`, `comments`, `toc`, `permalink`는 [_config.yml](../../_config.yml)의 `defaults`에서 글 전체에 자동 적용되므로 보통 생략합니다(레이아웃 `post`, 댓글·TOC 활성).

`last_modified_at`은 직접 적지 않습니다. [_plugins/posts-lastmod-hook.rb](../../_plugins/posts-lastmod-hook.rb)가 git 커밋 기록을 보고(커밋이 2회 이상인 글) 자동으로 채웁니다.

## 카테고리·태그 체계

블로그에서 실제로 쓰이는 대분류(`categories`의 첫 요소) 예시입니다. 전수 목록은 아닙니다:

| 주제 | categories 예 | 비고 |
| --- | --- | --- |
| 알고리즘 | `['Algorithm', 'LeetCode']`, `['Algorithm', 'Baekjoon']`, `['Algorithm', 'Practice']` | 소분류 LeetCode/Baekjoon/Practice. 난이도·기법은 tags로 |
| 논문 리뷰 | `[Paper Review, Medical AI]`, `[Paper Review, NLP]`, `[Paper Review, Generative AI]` | 리뷰 글 |
| AI/프로젝트 | `[AI, Bioinformatics]`, `[AI, Medical Imaging]` | 프로젝트 글 |
| 개발 | `[Development, Jekyll]`, `[Development, Testing]`, `[Python, Development]` | Jekyll, 테스트, Python 등 |
| DevOps/트러블슈팅 | `[DevOps, CI/CD]`, `[Blogging, Troubleshooting]`, `[Development, Troubleshooting]` | `Troubleshooting`은 항상 **보조(2번째)** 분류로만 쓰임 |

- 리스트 표기는 따옴표 유무가 혼용됩니다(`['Algorithm', 'LeetCode']` / `[AI, Bioinformatics]`). 한 글 안에서는 일관되게 적습니다.
- 카테고리·태그 페이지는 `jekyll-archives`가 자동 생성합니다(`/categories/:name/`, `/tags/:name/`). 새 카테고리/태그를 쓰면 해당 아카이브 페이지도 자동 생깁니다.
- **태그 표기 규칙 — 한 개념엔 한 표기.** 새 글의 태그는 **소문자-하이픈(kebab-case)** 을 권장합니다(예: `github-actions`, `object-detection`, `ci-cd`). 이유: `jekyll-archives`는 태그를 *원본 문자열* 단위로 페이지를 만들지만 URL은 `:name`을 slugify(소문자화·공백→하이픈)하므로, **같은 개념을 두 표기로 쓰면**(`FastAPI`+`fastapi`, `GitHub Actions`+`github-actions`) 둘 다 같은 `/tags/fastapi/` 주소를 노려 **destination 충돌**(빌드 경고, 한쪽 글이 누락될 수 있음)이 납니다. (기존 알고리즘·리뷰 글의 `Algorithm`·`LeetCode` 같은 TitleCase 태그는 *각자 일관되게* 쓰여 충돌이 없고 URL도 이미 소문자라 그대로 둡니다 — 충돌은 오직 **혼용**일 때만.) 새 태그를 더할 땐 `/tags/`에 같은 개념이 다른 표기로 이미 있는지 확인하세요.

## 글쓴이(author)

`author: seoultech`는 [_data/authors.yml](../../_data/authors.yml)의 항목과 연결됩니다.

```yaml
seoultech:
  name: Seoultech
  url: https://github.com/youngunghan
```

새 글쓴이를 추가하려면 `authors.yml`에 키를 만들고 front matter에서 그 키를 참조합니다. 생략하면 `_config.yml`의 `social.name`(기본 저자)이 쓰입니다.

## 이미지 경로 규칙

- 글 이미지는 주제별 하위 폴더에 둡니다: `assets/img/posts/<주제>/`.
  - 예: `assets/img/posts/algo/`, `assets/img/posts/troubleshooting/`, `assets/img/posts/protein-classifier/`
- **front matter `image.path`는 맨 앞 `/` 없이** 쓰는 것이 관례입니다(예: `assets/img/posts/algo/leetcode_new.png`). Chirpy 테마가 `media_subpath`/사이트 루트 기준으로 경로를 보정하므로 슬래시가 없어도 올바르게 렌더링됩니다(`_layouts/home.html`·`_layouts/post.html`).
- **본문 인라인 이미지는 반대로 맨 앞에 `/`를 붙입니다**(예: `![alt](/assets/img/posts/protein-classifier/architecture.png)`). 본문에는 위 보정 로직이 없어 `/`로 시작해야 `baseurl: /scitechblog` 환경에서 올바르게 해석됩니다. (현재 모든 글의 본문 이미지가 이 규칙을 따릅니다 — `/assets/img` 22건, 슬래시 없는 본문 이미지 0건.) 배경 설명은 [troubleshooting-image-paths](../../_posts/2025-11-30-troubleshooting-image-paths.md) 글 참고.
- 알고리즘 글은 공용 대표 이미지를 재사용합니다(예: `assets/img/posts/algo/leetcode_new.png`, `.../baekjoon_new.png`).

## 수식과 다이어그램

- **수식(LaTeX)**: front matter에 `math: true`를 넣으면 MathJax가 로드됩니다. 인라인 `$...$`, 블록 `$$...$$` 또는 `\(...\)`, `\[...\]` 사용.
  - 기존 글에 수식이 있는데 `math: true`가 빠졌다면 [enable_math.py](../../enable_math.py)로 일괄 추가할 수 있습니다([05 문서](05-python-scripts.md#수식다이어그램-정리) 참고).
- **다이어그램**: `mermaid: true`를 넣고 ```` ```mermaid ```` 코드블록에 다이어그램을 작성합니다.

## 새 글 추가 체크리스트

1. `_posts/`에 `YYYY-MM-DD-슬러그.md` 생성
2. front matter 작성(`title`, `date`, `categories`, `tags`, 필요 시 `image`/`math`/`mermaid`)
3. 이미지가 있으면 `assets/img/posts/<주제>/`에 넣고 상대 경로로 참조
4. `bash tools/run.sh`로 로컬 미리보기 확인
5. (선택) `bash tools/test.sh`로 링크 검사 후 커밋
