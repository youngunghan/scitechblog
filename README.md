# CSMAIR — scitechblog

> Computer Science × Medical AI × Railroad Science

[Jekyll](https://jekyllrb.com/) + [Chirpy 테마](https://github.com/cotes2020/jekyll-theme-chirpy) 기반의 기술 블로그입니다. 알고리즘 문제 풀이(LeetCode·백준), 논문 리뷰, 개발/트러블슈팅 노트를 다룹니다.

- **라이브 사이트**: <https://youngunghan.github.io/scitechblog>
- **저자**: Youngung Han ([@youngunghan](https://github.com/youngunghan))

---

## 빠른 시작

사전 요구: Ruby 3.3 + Bundler, [.nvmrc](.nvmrc)의 Node.js + npm.

```bash
# 1) 의존성 설치
bundle install
npm ci --ignore-scripts

# 2) 프런트엔드 검사·빌드
npm test
npm run build

# 3) 로컬 서버 실행 (http://127.0.0.1:4000/scitechblog)
bash tools/run.sh
```

> 이 저장소는 Chirpy 7.4.1 소스 전체를 추적합니다. Chirpy Ruby gem과 vendored 테마 소스를 같은 릴리스로 유지하고, npm 빌드 의존성은 별도 lockfile로 고정해 생성 자산을 로컬과 CI에서 빌드합니다. 자세한 내용은 [Quickstart](docs/tutorials/quickstart.md)와 [테마 소스 관리](docs/explanation/theme-customization.md)를 참고하세요.

새 글 작성은 [글 작성 규칙](docs/how-to/write-posts.md)을 따르세요.

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
| `*.py` (루트) | 글 정리·감사용 Python 유틸리티 스크립트(사이트 배포 제외) |
| [_config.yml](_config.yml) | Jekyll 사이트 전역 설정 |

---

## 문서

상세 문서는 Diátaxis 구조의 [개발자 문서 허브](docs/README.md)에 있습니다.

| 문서 | 내용 |
| --- | --- |
| [Quickstart](docs/tutorials/quickstart.md) | 설치, 자산 빌드, 로컬 실행과 production 검증 |
| [아키텍처](docs/explanation/architecture.md) | Jekyll·Chirpy 빌드와 GitHub Pages 배포 흐름 |
| [글 작성](docs/how-to/write-posts.md) | front matter, 출처, 이미지와 재현성 검증 |
| [설정 레퍼런스](docs/reference/configuration.md) | 공개 가능한 Jekyll·사이트 설정 |
| [유지보수 도구](docs/reference/maintenance-tools.md) | 콘텐츠 감사와 썸네일 생성 도구 |

---

## 크레딧 · 라이선스

이 블로그는 Cotes Chung의 [Chirpy Jekyll Theme](https://github.com/cotes2020/jekyll-theme-chirpy)를 기반으로 합니다. 테마 자체의 사용·개발·업그레이드 방법은 [Chirpy Wiki](https://github.com/cotes2020/jekyll-theme-chirpy/wiki)를 참고하세요.

자체 코드·설정·개발 문서는 [MIT License](LICENSE), 저자가 만든 글은 별도 표시가 없으면 [CC BY 4.0](CONTENT_LICENSE.md)입니다. 논문 그림과 기타 제3자 자료는 이 라이선스에 포함되지 않으며 [제3자 고지](THIRD_PARTY_NOTICES.md)의 원 권리자 조건을 따릅니다.
