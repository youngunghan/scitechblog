# 04. 테마 커스터마이징

이 블로그는 Chirpy 테마 **소스 전체**를 기반으로 합니다. 따라서 `_javascript`, `_sass`, `_layouts`, `_includes`, `_plugins` 대부분은 업스트림 Chirpy 코드입니다. 이 문서는 (1) 각 프런트엔드 서브시스템이 무엇을 하는지와 (2) 이 레포에서 실제로 손댄 지점을 구분해 설명합니다.

> 테마 자체의 동작 원리·업그레이드 방법은 [Chirpy Wiki](https://github.com/cotes2020/jekyll-theme-chirpy/wiki)가 1차 출처입니다. 여기서는 이 레포 맥락에 필요한 만큼만 정리합니다.

## 이 블로그의 실제 커스텀 지점

| 위치 | 변경 내용 |
| --- | --- |
| [_config.yml](../../_config.yml) | 사이트 정체성(`title: CSMAIR`, tagline, description), `url`/`baseurl`, `lang: en`, `timezone: Asia/Seoul`, `pwa.enabled: true`, 아바타 경로 |
| [_data/authors.yml](../../_data/authors.yml) | 글쓴이 항목 `seoultech` 추가 (`name: Seoultech`, url: github.com/youngunghan — 실제 저자 Youngung Han) |
| [_tabs/about.md](../../_tabs/about.md) | 개인 소개 페이지 내용 |
| [_tabs/challenge.md](../../_tabs/challenge.md) | **신규 커스텀 탭** — "AI Challenge" 페이지(인라인 CSS + `<details>` 접이식 목록) |
| `_posts/`, `assets/img/posts/` | 글 본문과 이미지(콘텐츠) |
| 루트 `*.py` | 글 생성/정리/감사 스크립트([05 문서](05-python-scripts.md)) |

나머지(`_layouts`, `_includes`, `_sass`, `_javascript`, `_plugins`, `tools`, `_data/locales`)는 사실상 Chirpy 기본값입니다. 업그레이드 시 충돌을 줄이려면 이 영역은 가급적 수정하지 않는 것이 좋습니다.

## JavaScript 커스텀

소스는 [_javascript/](../../_javascript/)에 있고 Rollup이 `assets/js/dist/`로 번들합니다([빌드 흐름](01-architecture.md#빌드-산출물-흐름) 참고).

### 페이지별 엔트리

각 레이아웃이 자기 페이지에 맞는 번들을 로드합니다.

| 엔트리 | 적재 페이지 | 주요 동작 |
| --- | --- | --- |
| `commons.js` | 전 페이지 공통 | 사이드바·탑바·기본 컴포넌트 초기화 |
| `home.js` | 홈 | 홈 목록 관련 초기화 |
| `categories.js` | 카테고리 | 카테고리 접기/펼치기 |
| `post.js` | 글 | TOC, 이미지 팝업 등 글 전용 동작 |
| `page.js` | 일반 페이지 | 페이지 공통 동작 |
| `misc.js` | 기타 | 보조 동작 |
| `theme.js` | 전역(`Theme`) | 다크/라이트 테마 토글 |
| `pwa/app.js`, `pwa/sw.js` | PWA | 서비스 워커 등록·오프라인 캐시 |

### 모듈 구성

[_javascript/modules/](../../_javascript/modules/) 아래에 재사용 모듈이 있습니다.

- `modules/components/` — `toc`(목차, 데스크톱/모바일 분리), `clipboard`(코드 복사), `img-popup`·`img-loading`(이미지 라이트박스·지연 로딩), `mermaid`(다이어그램), `mode-toggle`(테마 토글 UI), `category-collapse`, `back-to-top`, `locale-datetime`, `search-display`, `tooltip-loader`
- `modules/layouts/` — `basic`, `sidebar`, `topbar`

### 테마 토글 동작 ([theme.js](../../_javascript/theme.js))

`Theme` 클래스가 다크/라이트 모드를 관리합니다.

- `<html data-mode>` 속성으로 현재 모드를 표현하고 `sessionStorage`에 저장합니다.
- `_config.yml`의 `theme_mode`가 비어 있으면(현재 설정) 시스템 설정(`prefers-color-scheme`)을 따르며 사이드바의 토글로 전환할 수 있습니다.
- 토글 시 `window.postMessage`로 다른 플러그인(예: Mermaid, 댓글)에 변경을 알려 색상을 동기화합니다.

## 스타일(SCSS) 구조

소스는 [_sass/](../../_sass/)이며 Bootstrap 5 + Chirpy 변수 위에 구성됩니다.

| 디렉터리 | 역할 |
| --- | --- |
| `abstracts/` | 변수·믹스인·브레이크포인트(사이드바 폭, 폰트, 색 등) |
| `base/` | 리셋·타이포그래피·신택스 하이라이트 |
| `components/` | 버튼·팝업 등 컴포넌트 스타일 |
| `layout/` | 사이드바·탑바·푸터·패널 레이아웃 |
| `pages/` | 홈·글·아카이브·카테고리·태그·검색 페이지 |
| `themes/` | 다크(`dark.scss`)·라이트(`light.scss`) 색 스킴 |

`_config.yml`의 `sass.style: compressed`로 출력 CSS가 압축됩니다. 스타일을 바꿀 때는 `npm run lint:scss`(Stylelint)를 통과하는지 확인하세요.

## 레이아웃·인클루드

- [_layouts/](../../_layouts/): `default`(기본 골격) 위에 `home`, `post`, `page`, `archives`, `categories`/`category`, `tags`/`tag`, `compress`(HTML 압축)가 있습니다.
- [_includes/](../../_includes/): `sidebar.html`, `topbar.html`, `head.html`, `footer.html`, `trending-tags.html`, `post-nav.html`, `post-sharing.html`, `read-time.html`, `related-posts.html`, `comment.html`, 검색 관련(`search-loader.html`, `search-results.html`) 등 재사용 HTML 조각.

모두 Chirpy 기본 구성입니다. 디자인을 바꾸려면 이 파일을 직접 수정하기보다, 같은 경로의 파일을 오버라이드하는 방식과 업그레이드 영향을 함께 고려하세요.

## Jekyll 플러그인

[_plugins/posts-lastmod-hook.rb](../../_plugins/posts-lastmod-hook.rb): `posts` 컬렉션의 `post_init` 훅에서 각 글의 git 커밋 수를 확인하고, 커밋이 2회 이상이면(`commit_num.to_i > 1`) 마지막 커밋 날짜를 `last_modified_at`으로 설정합니다. 덕분에 글에 "수정일"이 자동 표시됩니다(GitHub Actions 빌드에서는 전체 git 히스토리가 필요).

## 데이터 파일

[_data/](../../_data/):

| 파일 | 역할 |
| --- | --- |
| `authors.yml` | 글쓴이 매핑(`author:` 키 → 이름·URL). `seoultech` 추가됨 |
| `contact.yml` | 사이드바 연락처 아이콘(GitHub, Email, RSS 등) |
| `share.yml` | 글 하단 공유 버튼 대상(Twitter/Facebook/Telegram 등) |
| `media.yml` | 임베드 미디어 확장자 → MIME 매핑 |
| `locales/` | UI 다국어 문자열(업스트림, 현재 사이트 언어는 `en`) |
| `origin/` | 에셋 origin(CDN vs self-host) 설정 |

## 내비게이션 탭

[_tabs/](../../_tabs/)는 상단/사이드바 메뉴를 구성하며 `order` 값으로 정렬됩니다.

| 탭 | 레이아웃 | order | 비고 |
| --- | --- | --- | --- |
| `about.md` | page(기본) | 1 | 개인 소개(커스텀 내용) |
| `challenge.md` | page(기본) | 2 | **커스텀 페이지**: AI Challenge(마크다운 로드맵) |
| `categories.md` | categories | 3 | 카테고리(자동) |
| `tags.md` | tags | 4 | 태그(자동) |
| `archives.md` | archives | 5 | 글 아카이브(자동) |

`challenge.md`는 Scott Young의 MIT Challenge에서 착안한 학습 트래킹 페이지로, Chirpy 기본 문서 톤에 맞춘 마크다운 표와 섹션 구조를 사용합니다.

## 주요 사이트 설정 ([_config.yml](../../_config.yml))

| 항목 | 값/의미 |
| --- | --- |
| `title` / `tagline` / `description` | 사이트 정체성(CSMAIR) |
| `url` / `baseurl` | `https://youngunghan.github.io` + `/scitechblog` |
| `lang` / `timezone` | `en` / `Asia/Seoul` |
| `theme_mode` | 비움 → 시스템 설정 따름 + 토글 제공 |
| `pwa.enabled` / `pwa.cache.enabled` | PWA 설치·오프라인 캐시 활성 |
| `paginate` | 홈 페이지당 글 10개 |
| `defaults` | 글: `layout: post`, `comments`/`toc` 활성, `permalink: /posts/:title/` |
| `collections.tabs` | 탭 컬렉션을 `order`로 정렬해 출력 |
| `jekyll-archives` | 카테고리/태그 아카이브 자동 생성 |
| `compress_html` | 프로덕션 HTML 압축(개발 환경 제외) |
| `comments.provider` | `utterances` 활성(`youngunghan/scitechblog`, `pathname`) |
| `analytics` | 슬롯만 있고 현재 미설정(측정 ID 필요) |

> 댓글은 GitHub Issues 기반 `utterances`로 활성화되어 있습니다. 웹 애널리틱스는 Google Analytics의 `G-...` 측정 ID나 GoatCounter/Umami 같은 provider별 site ID가 필요하므로, 실제 ID를 발급받은 뒤 `_config.yml`의 해당 provider를 채웁니다.
