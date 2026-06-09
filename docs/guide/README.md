# scitechblog 개발 문서

CSMAIR(scitechblog) 블로그의 개발자용 문서 모음입니다. 프로젝트 구조, 빌드/배포 방법, 글 작성 규칙, 테마 커스터마이징, 부가 스크립트를 다룹니다.

> 이 폴더(`docs/`)는 [_config.yml](../../_config.yml)의 `exclude` 목록에 포함되어 있어 Jekyll 사이트로 빌드되지 않습니다. 즉, 여기 있는 문서는 블로그 페이지로 게시되지 않는 **레포 내부 문서**입니다.

## 목차

1. [아키텍처](01-architecture.md) — 프로젝트가 무엇이고 어떻게 구성되는가
   - 정체성과 기술 스택, 전체 디렉터리 구조 지도, 빌드 산출물 흐름
2. [개발 시작](02-getting-started.md) — 어떻게 돌리고 배포하는가
   - 환경 준비, `tools/` 셸 스크립트, npm 스크립트, CI/CD 파이프라인
3. [글 작성 규칙](03-writing-posts.md) — 새 글을 어떻게 쓰는가
   - 파일명 규칙, front matter 스키마, 카테고리/태그 체계, 이미지·수식·다이어그램
4. [테마 커스터마이징](04-theme-customization.md) — Chirpy 대비 무엇을 바꿨는가
   - `_javascript`, `_sass`, `_layouts`/`_includes`, `_plugins`, `_data`, `_tabs`
5. [Python 스크립트](05-python-scripts.md) — 루트의 부가 유틸리티
   - 스크립트별 목적·입출력·실행법과 주의사항

## 빠르게 찾기

| 하고 싶은 일 | 참고 문서 |
| --- | --- |
| 로컬에서 블로그 띄우기 | [02. 개발 시작](02-getting-started.md#로컬-실행) |
| 새 알고리즘/리뷰 글 추가 | [03. 글 작성 규칙](03-writing-posts.md) |
| 수식(LaTeX)·다이어그램 켜기 | [03. 글 작성 규칙](03-writing-posts.md#수식과-다이어그램) |
| 다크/라이트 테마 동작 이해 | [04. 테마 커스터마이징](04-theme-customization.md#javascript-커스텀) |
| 썸네일 이미지 생성 | [05. Python 스크립트](05-python-scripts.md#썸네일-생성) |
| 배포가 어떻게 되는지 | [02. 개발 시작](02-getting-started.md#cicd와-배포) |
