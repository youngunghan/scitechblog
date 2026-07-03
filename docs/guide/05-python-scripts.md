# 05. Python 스크립트

레포의 Python 스크립트들은 **블로그 운영을 돕는 부가 유틸리티**입니다. Jekyll 사이트 콘텐츠와는 무관하며(페이지로 렌더링되지 않음), 썸네일을 만들거나 글의 수식 설정을 정리하거나 품질을 점검할 때 손으로 실행하는 도구입니다.

> 참고: `tools/` 아래 스크립트는 [_config.yml](../../_config.yml)의 `exclude` 목록에 들어 있어 사이트 산출물로 복사되지 않습니다. 레포 루트의 남은 `*.py` 유틸리티는 front matter가 없어 페이지로 렌더링되진 않지만, Jekyll이 `_site/`로 그대로 복사할 수 있습니다. 게시 산출물에 포함되면 안 되는 새 유틸리티는 `tools/` 아래에 둡니다.

## 한눈에 보기

현재 레포에 있는 스크립트는 5개입니다.

| 스크립트 | 분류 | 대상 | 성격 |
| --- | --- | --- | --- |
| `tools/thumbnails/generate_thumbnail.py` | 썸네일 생성 | `assets/img/.../thumbnail.png` | 재사용 가능 |
| `tools/thumbnails/generate_latex_thumbnail.py` | 썸네일 생성 | `assets/img/.../latex_thumbnail.png` | 재사용 가능 |
| `tools/thumbnails/generate_eval_thumbnails.py` | 썸네일 생성 | `assets/img/posts/{fid-checklist,numbers-eat-pipelines}/cover.png` | 재사용 가능 |
| `enable_math.py` | 수식/콘텐츠 정리 | `_posts/*.md` | 재사용 가능 |
| `generate_audit_report.py` | 감사/유지보수 | `_posts/*.md` | 재사용 가능(경로 수정 필요) |

> 공통 전제: 루트 상대 경로(`_posts/*.md`, `assets/...`)를 쓰므로 **레포 루트에서 실행**해야 합니다(`cd .../scitechblog && python <script>.py`).

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

### `tools/thumbnails/generate_eval_thumbnails.py`

- **목적**: 평가 엄밀성(evaluation-rigor) 글용 라이트 박스 다이어그램 커버 생성 — FID 재현성 체크리스트 글과 교차 프로젝트 "numbers eat pipelines" 캡스톤 글. **라이선스 안전**: 데이터셋 파생 이미지 없이 순수 도식만 그립니다(`matplotlib` Agg 백엔드).
- **출력**: `assets/img/posts/fid-checklist/cover.png`, `assets/img/posts/numbers-eat-pipelines/cover.png` (폴더 없으면 생성).
- **실행**: `python tools/thumbnails/generate_eval_thumbnails.py`
- **의존성**: `matplotlib`.

## 수식/콘텐츠 정리

### `enable_math.py`

- **목적**: 수식 구분자(`$`, `\(`, `\[`)를 포함한 글에 front matter `math: true`를 일괄 주입.
- **입력/출력**: `_posts/*.md`를 읽어 조건에 맞는 파일을 in-place 수정. 이미 `math: true`가 있으면 건너뜀.
- **실행**: `python enable_math.py`
- **의존성**: 표준 라이브러리(`glob`, `re`).

## 감사 / 유지보수

### `generate_audit_report.py`

- **목적**: 모든 글의 front matter·이미지 경로·필수 섹션 구조를 점검해 Markdown 표 형태의 품질 감사 리포트 생성(🟢/⚠️/🔴 상태).
- **입력**: `_posts/*.md`.
- **출력**: `/root/.gemini/antigravity/brain/<uuid>/blog_audit_report.md` — **레포 외부의 하드코딩 절대 경로**라 이 환경에서는 그대로 동작하지 않습니다. 재사용하려면 코드의 출력 경로를 레포 내부(예: `docs/blog_audit_report.md`)로 바꾸세요.
- **실행**: `python generate_audit_report.py`
- **의존성**: `glob`, `re`, **`PyYAML`**(`import yaml`).

## 의존성 정리

별도 `requirements.txt`는 없습니다. 외부 패키지가 필요한 스크립트는 두 종류뿐입니다.

```bash
pip install matplotlib   # tools/thumbnails/*.py (썸네일 3종)
pip install pyyaml       # generate_audit_report.py
```

나머지(`enable_math.py`)는 Python 표준 라이브러리(`glob`, `re`)만 사용합니다.

## 주의사항

- **실행 위치**: 루트 상대 경로를 쓰므로 반드시 레포 루트에서 실행합니다.
- **in-place 수정**: `enable_math.py`는 글 파일을 직접 덮어씁니다. 실행 전 git 상태가 깨끗한지 확인하고, 결과는 `git diff`로 검토하세요.
- **하드코딩 경로**: `generate_audit_report.py`의 출력 경로는 레포 외부 절대 경로라 그대로는 현재 환경과 맞지 않습니다. 재사용하려면 경로를 먼저 수정하세요.

> **과거 1회용 스크립트(제거됨)**: 초기 마이그레이션·정리에 쓰였던 `migrate_algos.py`·`clean_generic_content.py`·`clean_mathjax.py`·`remove_redundant_links.py`·`remove_leetcode_headers.py`·`update_posts.py`는 역할을 다해 레포에서 제거됐습니다. git 히스토리에만 남아 있으니, 옛 문서/커밋에서 이 이름을 보면 이 항목을 참고하세요.
