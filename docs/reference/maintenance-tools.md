# 유지보수 도구 레퍼런스

> **범위:** 콘텐츠 감사, MathJax 설정과 썸네일 생성 도구. 사이트 실행은 [Quickstart](../tutorials/quickstart.md) 참고.
> **대상:** 블로그 작성자 · 유지보수자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

모든 명령은 저장소 루트에서 실행합니다. 루트 Python 도구와 `tools/`는 [_config.yml](../../_config.yml)의 `exclude`에 포함되어 배포되지 않습니다.

## 1. 도구 목록

| 도구 | 입력 | 출력·변경 | 의존성 |
|---|---|---|---|
| [enable_math.py](../../enable_math.py) `main()` | `_posts/*.md` | 수식이 있는 글에 `math: true` 추가 | Python 표준 라이브러리 |
| [generate_audit_report.py](../../generate_audit_report.py) `main()` | `_posts/*.md` | stdout 또는 `--output` Markdown | PyYAML |
| [generate_thumbnail.py](../../tools/thumbnails/generate_thumbnail.py) | 글·스타일 상수 | 트러블슈팅 대표 이미지 | matplotlib |
| [generate_latex_thumbnail.py](../../tools/thumbnails/generate_latex_thumbnail.py) | 글·스타일 상수 | LaTeX 대표 이미지 | matplotlib |
| [generate_eval_thumbnails.py](../../tools/thumbnails/generate_eval_thumbnails.py) | 글·스타일 상수 | FID 글 대표 이미지 | matplotlib |

## 2. MathJax 설정

```bash
python enable_math.py --check
python enable_math.py
```

`--check`는 파일을 바꾸지 않고 누락만 보고하며, 누락이 있으면 exit 1을 반환합니다. fenced/inline code의 shell 변수 `$NAME`은 수식으로 판정하지 않습니다. 실제 변경 전에는 작업 트리를 확인하고 실행 후 `git diff`를 검토합니다.

## 3. 콘텐츠 감사

```bash
python generate_audit_report.py
python generate_audit_report.py --output /tmp/blog-audit.md
```

기본 출력은 stdout입니다. 보고서는 front matter, 대표 이미지 경로와 글 유형별 기본 섹션을 점검하는 보조 신호이며 사실 검증을 대체하지 않습니다.

## 4. 썸네일 생성

```bash
python tools/thumbnails/generate_thumbnail.py
python tools/thumbnails/generate_latex_thumbnail.py
python tools/thumbnails/generate_eval_thumbnails.py
```

생성 후 이미지 크기, 텍스트 잘림, 라이선스와 실제 글 참조 여부를 확인합니다. 대형 PNG는 게시 크기로 축소합니다.

## 5. Python 의존성

```bash
python -m pip install matplotlib pyyaml
```

별도 Python lockfile은 없습니다. 재현 가능한 자동화에 편입할 때는 requirements 또는 `pyproject.toml` 도입이 필요합니다. 상태: 미구현(목표).
