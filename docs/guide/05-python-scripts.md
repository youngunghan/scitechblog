# 05. Python 스크립트

레포의 Python 스크립트들은 **블로그 운영을 돕는 부가 유틸리티**입니다. Jekyll 사이트 콘텐츠와는 무관하며(페이지로 렌더링되지 않음), 글을 대량 생성·정리하거나 썸네일을 만들거나 품질을 점검할 때 손으로 실행하는 도구입니다. 상당수는 **1회용 마이그레이션/정리 스크립트**라 그대로 재실행하면 의도와 다르게 동작할 수 있으니, 아래 [주의사항](#주의사항)을 먼저 읽으세요.

> 참고: `tools/` 아래 스크립트는 [_config.yml](../../_config.yml)의 `exclude` 목록에 들어 있어 사이트 산출물로 복사되지 않습니다. 레포 루트의 남은 `*.py` 유틸리티는 front matter가 없어 페이지로 렌더링되진 않지만, Jekyll이 `_site/`로 그대로 복사할 수 있습니다. 게시 산출물에 포함되면 안 되는 새 유틸리티는 `tools/` 아래에 둡니다.

## 한눈에 보기

| 스크립트 | 분류 | 대상 | 성격 |
| --- | --- | --- | --- |
| `tools/thumbnails/generate_thumbnail.py` | 썸네일 생성 | `assets/img/.../thumbnail.png` | 재사용 가능 |
| `tools/thumbnails/generate_latex_thumbnail.py` | 썸네일 생성 | `assets/img/.../latex_thumbnail.png` | 재사용 가능 |
| `enable_math.py` | 수식/콘텐츠 정리 | `_posts/*.md` | 재사용 가능 |
| `clean_mathjax.py` | 수식/콘텐츠 정리 | 단일 파일(하드코딩) | 1회용 |
| `remove_redundant_links.py` | 링크/헤더 정리 | `_posts/*.md` | 재사용 가능 |
| `remove_leetcode_headers.py` | 링크/헤더 정리 | `_posts/*leetcode*.md` | 재사용 가능 |
| `migrate_algos.py` | 마이그레이션/생성 | 외부 레포 → `_posts/` | 1회용 |
| `clean_generic_content.py` | 마이그레이션/생성 | 생성된 알고리즘 글 | 1회용 |
| `generate_audit_report.py` | 감사/유지보수 | `_posts/*.md` | 재사용 가능(경로 수정 필요) |
| `update_posts.py` | 감사/유지보수 | `_posts/` 일부 | 1회용 성격 |

> 공통 전제: 대부분 상대 경로(`_posts/*.md`)를 쓰므로 **레포 루트에서 실행**해야 합니다(`cd .../scitechblog && python <script>.py`).

## 썸네일 생성

matplotlib으로 글 대표 이미지를 그립니다.

### `tools/thumbnails/generate_thumbnail.py`

- **목적**: html-proofer 출력처럼 보이는 터미널 스타일 썸네일 생성(트러블슈팅 글용).
- **출력**: `assets/img/posts/troubleshooting/thumbnail.png` (폴더 없으면 생성).
- **실행**: `python tools/thumbnails/generate_thumbnail.py`
- **의존성**: `matplotlib`.

### `tools/thumbnails/generate_latex_thumbnail.py`

- **목적**: LaTeX 렌더링 전/후를 보여주는 다크 테마 썸네일 생성.
- **출력**: `assets/img/posts/troubleshooting/latex_thumbnail.png`.
- **실행**: `python tools/thumbnails/generate_latex_thumbnail.py`
- **의존성**: `matplotlib`.

## 수식/다이어그램 정리

### `enable_math.py`

- **목적**: 수식 구분자(`$`, `\(`, `\[`)를 포함한 글에 front matter `math: true`를 일괄 주입.
- **입력/출력**: `_posts/*.md`를 읽어 조건에 맞는 파일을 in-place 수정. 이미 `math: true`가 있으면 건너뜀.
- **실행**: `python enable_math.py`
- **의존성**: 표준 라이브러리(`glob`, `re`).

### `clean_mathjax.py`

- **목적**: 과거에 본문에 박혀 있던 MathJax HTML 래퍼(`<mjx-container>` 등)를 제거하고 일반 텍스트로 복원.
- **입력/출력**: `__main__`에 **단일 파일 경로가 하드코딩**되어 있음(`_posts/2024-10-10-algo-boj-23832-서로소-그래프.md`). 다른 파일에 쓰려면 코드의 경로를 바꿔야 함.
- **실행**: `python clean_mathjax.py`
- **의존성**: 표준 라이브러리(`re`).

## 링크/헤더 정리

### `remove_redundant_links.py`

- **목적**: 본문에 중복으로 들어간 한국어 문제 링크 블록(`> [문제 링크](...)`) 제거.
- **입력/출력**: `_posts/*.md` in-place 수정, 수정 건수 출력.
- **실행**: `python remove_redundant_links.py`
- **의존성**: `glob`. (`re`도 import되어 있으나 실제로는 사용되지 않는 잔여 import이며, 매칭은 `str.strip()`/`startswith()`/`endswith()`로만 처리합니다.)

### `remove_leetcode_headers.py`

- **목적**: LeetCode 글에 중복된 문제 제목 헤더(`<h2><a>...` 블록) 제거.
- **입력/출력**: `_posts/*leetcode*.md` in-place 수정.
- **실행**: `python remove_leetcode_headers.py`
- **의존성**: `glob`, `re`.

## 마이그레이션 / 생성

### `migrate_algos.py`

- **목적**: 외부 알고리즘 풀이 레포(백준·LeetCode)를 읽어 구조화된 Jekyll 글을 대량 생성. 문제 메타데이터(ID·제목·날짜·태그) 추출, 유형별(DP/그래프/수학/그리디/탐색) 접근 섹션 템플릿 삽입, 코드 패턴 분석 후 트러블슈팅 섹션 생성까지 수행.
- **입력**: `temp_repos/Algorithm-and-Problem-Solving/백준`, `temp_repos/LeetCodeHub` (레포에 포함되지 않은 외부 클론). git 로그로 작성일 추정.
- **출력**: `_posts/`에 새 `.md` 글 생성.
- **실행**: `python migrate_algos.py` → `process_baekjoon()` + `process_leetcode()` 호출.
- **의존성**: 표준 라이브러리(`os`, `re`, `datetime`, `subprocess`).
- **주의**: 상단에 `REPO_ROOT = "/home/yuhan/repo/scitechblog"`가 **하드코딩**되어 있어 현재 레포 경로(`.../vision_ai_detection_enhancement/scitechblog`)와 다릅니다. 또한 `temp_repos/` 외부 소스에 의존하므로 그대로는 재현되지 않습니다. 글 생성이 끝난 1회용 마이그레이션 도구로 보면 됩니다.

### `clean_generic_content.py`

- **목적**: `migrate_algos.py`가 만든 글에서 지나치게 일반적인 템플릿 섹션(예: 정형화된 "Problem Analysis", 수학 성질 접근/트러블슈팅)을 제거.
- **입력/출력**: `_posts/*leetcode*.md` + 하드코딩된 백준 파일 목록을 in-place 수정.
- **실행**: `python clean_generic_content.py` → `clean_leetcode_posts()` + `clean_boj_posts()`.
- **의존성**: `glob`, `re`.
- **주의**: `migrate_algos.py`의 후처리 1회용 스크립트. 제거 대상 텍스트가 하드코딩되어 있어 현재 글과 일치하지 않으면 아무 것도 바꾸지 않습니다.

## 감사 / 유지보수

### `generate_audit_report.py`

- **목적**: 모든 글의 front matter·이미지 경로·필수 섹션 구조를 점검해 Markdown 표 형태의 품질 감사 리포트 생성(🟢/⚠️/🔴 상태).
- **입력**: `_posts/*.md`.
- **출력**: `/root/.gemini/antigravity/brain/<uuid>/blog_audit_report.md` — **레포 외부의 하드코딩 절대 경로**라 이 환경에서는 그대로 동작하지 않습니다. 재사용하려면 코드의 출력 경로를 레포 내부(예: `docs/blog_audit_report.md`)로 바꾸세요.
- **실행**: `python generate_audit_report.py`
- **의존성**: `glob`, `re`, **`PyYAML`**(`import yaml`).

### `update_posts.py`

- **목적**: 글에 대한 세 가지 일괄 보정 작업을 묶어 실행.
  1. `add_author_to_new_posts()` — `_posts/2025-12-24*.md`에 `author: seoultech` 추가
  2. `update_algorithm_thumbnails()` — `_posts/*algo*.md`의 썸네일 경로를 신버전으로 교체(예: `baekjoon.png` → `baekjoon_new.png`)
  3. `remove_leetcode_duplicate_links()` — `_posts/*leetcode*.md`의 중복 링크 제거
- **입력/출력**: 위 패턴에 맞는 글을 in-place 수정, 작업별 건수 출력.
- **실행**: `python update_posts.py`
- **의존성**: `glob`, `re`.
- **주의**: 특정 날짜/패턴에 묶인 1회성 보정 작업이라, 지금 다시 돌리면 대상이 없거나 이미 적용된 상태일 수 있습니다.

## 의존성 정리

별도 `requirements.txt`는 없습니다. 외부 패키지가 필요한 스크립트는 두 개뿐입니다.

```bash
pip install matplotlib   # tools/thumbnails/generate_thumbnail.py, tools/thumbnails/generate_latex_thumbnail.py
pip install pyyaml       # generate_audit_report.py
```

나머지는 모두 Python 표준 라이브러리(`glob`, `re`, `os`, `datetime`, `subprocess`)만 사용합니다.

## 주의사항

- **실행 위치**: 상대 경로(`_posts/*.md`)를 쓰므로 반드시 레포 루트에서 실행합니다.
- **in-place 수정**: 다수 스크립트가 파일을 직접 덮어씁니다. 실행 전 git 상태가 깨끗한지 확인하고, 결과는 `git diff`로 검토하세요.
- **하드코딩 경로**: `migrate_algos.py`(`REPO_ROOT`), `generate_audit_report.py`(출력 경로), `clean_mathjax.py`(단일 파일)는 경로가 박혀 있어 그대로는 현재 환경과 맞지 않습니다. 재사용하려면 경로를 먼저 수정하세요.
- **외부 의존**: `migrate_algos.py`는 레포에 없는 `temp_repos/` 클론이 있어야 동작합니다.
- **1회용 성격**: `clean_*`, `migrate_*`, `update_posts.py`는 특정 시점의 정리 작업을 위해 만들어졌습니다. 본 문서는 "무엇을 했던 스크립트인지" 기록 목적이며, 재실행 시에는 동작을 코드로 다시 확인하는 편이 안전합니다.

> 이 스크립트들은 대체로 주석이 적고, 일부 함수에만 짧은 docstring이 달려 있습니다(예: `update_posts.py`, `remove_leetcode_headers.py`, `clean_generic_content.py`). 본 문서가 사실상의 레퍼런스 역할을 합니다.
