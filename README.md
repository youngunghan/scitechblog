# CSMAIR — scitechblog

> Computer Science × Medical AI × Railroad Science

[Jekyll](https://jekyllrb.com/) + [Chirpy 테마](https://github.com/cotes2020/jekyll-theme-chirpy) 기반의 기술 블로그입니다. 알고리즘 문제 풀이(LeetCode·백준), 논문 리뷰, 개발/트러블슈팅 노트를 다룹니다.

- **라이브 사이트**: <https://youngunghan.github.io/scitechblog>
- **저자**: Youngung Han ([@youngunghan](https://github.com/youngunghan))

---

## 빠른 시작

사전 요구: Ruby + Bundler, Node.js + npm.

```bash
# 1) 의존성 설치
bundle install
npm install

# 2) 프런트엔드 에셋 빌드 (JS 번들 + CSS 최적화)
npm run build

# 3) 로컬 서버 실행 (http://127.0.0.1:4000/scitechblog)
bash tools/run.sh
```

> 이 레포는 Chirpy **스타터**가 아니라 **테마 소스 전체**를 기반으로 하므로, 서버 실행 전에 `npm run build`로 `assets/js/dist/`의 JS 번들을 한 번 생성해야 합니다. 자세한 내용은 [개발 시작 가이드](docs/guide/02-getting-started.md)를 참고하세요.

새 글 작성은 [글 작성 규칙](docs/guide/03-writing-posts.md)을 따르세요.

---

## 디렉터리 한눈에 보기

| 경로 | 역할 |
| --- | --- |
| [_posts/](_posts/) | 블로그 글(Markdown). 파일명 `YYYY-MM-DD-제목.md` |
| [_tabs/](_tabs/) | 상단 내비게이션 페이지(about, archives, categories, tags, challenge) |
| [_data/](_data/) | 사이트 데이터(authors, contact, share, media, locales) |
| [_layouts/](_layouts/) · [_includes/](_includes/) | 페이지 레이아웃 / 재사용 HTML 조각 (Chirpy 기본) |
| [_sass/](_sass/) | SCSS 스타일 소스 |
| [_javascript/](_javascript/) | 프런트엔드 JS 소스 (Rollup으로 번들) |
| [_plugins/](_plugins/) | 커스텀 Jekyll 플러그인 (git 기반 수정일 표시) |
| [assets/](assets/) | 정적 에셋 및 빌드 산출물(`js/dist/`, 이미지 등) |
| [tools/](tools/) | 실행/빌드/배포 셸 스크립트 |
| `*.py` (루트) | 글 생성·정리·감사용 Python 유틸리티 스크립트 |
| [_config.yml](_config.yml) | Jekyll 사이트 전역 설정 |

---

## 문서

상세 문서는 [`docs/guide/`](docs/guide/)에 있습니다.

| 문서 | 내용 |
| --- | --- |
| [01. 아키텍처](docs/guide/01-architecture.md) | 프로젝트 정체성, 기술 스택, 디렉터리 구조, 빌드 흐름 |
| [02. 개발 시작](docs/guide/02-getting-started.md) | 환경 준비, 빌드/실행/테스트/배포, CI/CD |
| [03. 글 작성 규칙](docs/guide/03-writing-posts.md) | 파일명, front matter, 카테고리/태그, 이미지, 수식/다이어그램 |
| [04. 테마 커스터마이징](docs/guide/04-theme-customization.md) | `_javascript` · `_sass` · `_layouts` · `_plugins` 등 커스텀 지점 |
| [05. Python 스크립트](docs/guide/05-python-scripts.md) | 루트 유틸리티 스크립트 레퍼런스 및 주의사항 |

---

## 크레딧 · 라이선스

이 블로그는 Cotes Chung의 [Chirpy Jekyll Theme](https://github.com/cotes2020/jekyll-theme-chirpy)를 기반으로 합니다. 테마 자체의 사용·개발·업그레이드 방법은 [Chirpy Wiki](https://github.com/cotes2020/jekyll-theme-chirpy/wiki)를 참고하세요.

본 프로젝트는 [MIT License](LICENSE)로 배포됩니다.
