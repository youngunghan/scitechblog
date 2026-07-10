# scitechblog 아키텍처

> **범위:** Jekyll 빌드, Chirpy 소스, 콘텐츠와 GitHub Pages 배포 흐름. 글 작성 절차는 [write-posts.md](../how-to/write-posts.md) 참고.
> **대상:** 개발자 · 운영자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

## 0. 한눈에 보기

```text
_posts/ + _tabs/ + _config.yml
              │
              ▼
     Jekyll 4.4.1 + Chirpy 7.4.1 ◀── npm build ── _javascript/ + _sass/
              │
              ▼
       _site/scitechblog/
              │
       HTML-Proofer 검증
              │
              ▼
         GitHub Pages
```

## 1. 컴포넌트

| 컴포넌트 | 책임 | 구현 위치 |
|---|---|---|
| Jekyll 설정 | URL, 컬렉션, 플러그인, 게시 제외 경로 | [_config.yml](../../_config.yml) |
| 콘텐츠 | 날짜 기반 글과 고정 탭 | [_posts/](../../_posts/) · [_tabs/](../../_tabs/) |
| 테마 소스 | 레이아웃, include, SCSS, 브라우저 JavaScript | [_layouts/](../../_layouts/) · [_includes/](../../_includes/) · [_sass/](../../_sass/) · [_javascript/](../../_javascript/) |
| 자산 빌드 | Rollup과 PurgeCSS로 JS/CSS 산출물 생성 | [package.json](../../package.json) `scripts` |
| 사이트 검증 | production 빌드와 내부 링크 검사 | [tools/test.sh](../../tools/test.sh) `main()` |
| 배포 | Node 자산 빌드 후 Jekyll 빌드·검증·Pages 업로드 | [pages-deploy.yml](../../.github/workflows/pages-deploy.yml) `jobs.build` |

## 2. 빌드 흐름

### 2.1 프런트엔드 자산

`npm run build`는 `_javascript/`를 `assets/js/dist/`로 번들하고, Bootstrap/SCSS vendor 파일을 `_sass/vendors/`에 생성합니다. 두 디렉터리는 생성 산출물이므로 Git에 커밋하지 않고 로컬과 CI에서 동일한 lockfile로 재생성합니다.

### 2.2 Jekyll 사이트

Jekyll은 콘텐츠와 테마 소스를 결합해 정적 HTML을 만듭니다. 프로젝트 사이트의 `baseurl`이 `/scitechblog`이므로 production 검증은 `_site/scitechblog/` 하위까지 포함해 수행합니다.

### 2.3 배포

`master` 또는 `main`의 사이트 관련 변경은 GitHub Actions를 실행합니다. 순서는 `npm ci` → frontend lint/build → `bundle install` cache → Jekyll production build → HTML-Proofer → GitHub Pages artifact 배포입니다. 테스트가 실패하면 배포 job은 실행되지 않습니다.

## 3. 설계 결정

- **[검증 반영 #1] Chirpy 7.4.1 단일 소스 기준** (2026-07-10): Chirpy gem과 vendored 테마 소스를 `7.4.1`에 맞춥니다. npm package는 블로그 전용 `scitechblog`이며 frontend 의존성 재현을 위해 별도 lockfile을 추적합니다. 상태: 구현 ✅.
- **[검증 반영 #2] 생성 자산은 CI에서 빌드** (2026-07-10): `assets/js/dist/`와 `_sass/vendors/`를 커밋하지 않습니다. 상태: 구현 ✅.
- **[검증 반영 #3] 외부 댓글·방문자 스크립트 비활성** (2026-07-10): 설정 또는 저장소 기능이 준비되지 않은 third-party runtime은 로드하지 않습니다. 상태: 구현 ✅.

## 관련 문서

- [Quickstart](../tutorials/quickstart.md)
- [테마 소스 관리](theme-customization.md)
- [설정 레퍼런스](../reference/configuration.md)
