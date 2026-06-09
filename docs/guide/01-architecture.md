# 01. 아키텍처

## 프로젝트 정체성

- **이름**: CSMAIR (`scitechblog`)
- **슬로건**: Computer Science × Medical AI × Railroad Science
- **성격**: 알고리즘 풀이(LeetCode·백준), AI/의료 AI 논문 리뷰, 개발·트러블슈팅 노트를 모은 1인 기술 블로그
- **호스팅**: GitHub Pages — `url: https://youngunghan.github.io`, `baseurl: /scitechblog` ([_config.yml](../../_config.yml) 27·154행)
- **기반 테마**: [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) v7.4.x

> 참고: 이 레포는 Chirpy **스타터 템플릿**이 아니라 **테마 소스 전체**(`package.json`·빌드 설정 포함)를 그대로 가져와 사이트로 쓰는 형태입니다. 그래서 글만 쓰는 일반 블로그보다 빌드 도구(Node 기반)가 함께 들어 있고, 로컬 실행 전에 JS 에셋을 직접 빌드해야 합니다. (테마 배포용 `.gemspec`은 사용자 레포에서 제거되어 있고, [Gemfile](../../Gemfile)이 Chirpy를 gem으로 가져옵니다.)

## 기술 스택

| 영역 | 사용 기술 |
| --- | --- |
| 정적 사이트 생성 | Jekyll 4 (Ruby), Kramdown + Rouge 신택스 하이라이트 |
| 테마 | `jekyll-theme-chirpy` (gem) |
| 스타일 | SCSS(Sass), Bootstrap 5.3 |
| 프런트엔드 빌드 | Rollup + Babel(JS 번들), PurgeCSS(미사용 CSS 제거) |
| 코드 품질 | ESLint(JS), Stylelint(SCSS), html-proofer(링크 검사) |
| 커밋/릴리스 | Husky + commitlint(Conventional Commits), semantic-release |
| 배포 | GitHub Actions → GitHub Pages |
| 부가 도구 | 루트의 Python 스크립트(글 생성·정리·감사) |

JS 의존성은 [package.json](../../package.json), Ruby 의존성은 [Gemfile](../../Gemfile)에 선언되어 있습니다.

## 전체 디렉터리 구조

```text
scitechblog/
├── _config.yml            # Jekyll 사이트 전역 설정
├── _posts/                # 블로그 글(Markdown), 42개
├── _tabs/                 # 상단 내비게이션 페이지
├── _data/                 # 사이트 데이터(yml)
│   ├── authors.yml        #   글쓴이 정보(author 키 매핑)
│   ├── contact.yml        #   사이드바 연락처 아이콘
│   ├── share.yml          #   글 하단 공유 버튼
│   ├── media.yml          #   임베드 미디어 MIME 매핑
│   ├── locales/           #   UI 다국어 문자열(업스트림)
│   └── origin/            #   에셋 origin(CDN/self-host) 설정
├── _layouts/              # 페이지 레이아웃 템플릿(Chirpy 기본)
├── _includes/             # 재사용 HTML 조각(Chirpy 기본)
├── _sass/                 # SCSS 스타일 소스
│   ├── abstracts/ base/ components/ layout/ pages/ themes/
├── _javascript/           # 프런트엔드 JS 소스(Rollup 입력)
│   ├── commons/home/categories/page/post/misc/theme.js  # 페이지별 엔트리
│   ├── modules/           #   컴포넌트·레이아웃 모듈
│   └── pwa/               #   PWA 서비스 워커(app.js, sw.js)
├── _plugins/              # 커스텀 Jekyll 플러그인(Ruby)
│   └── posts-lastmod-hook.rb   # git 기록으로 last_modified_at 설정
├── assets/                # 정적 에셋 + 빌드 산출물
│   ├── js/dist/           #   Rollup 번들 출력(빌드 시 생성)
│   └── img/posts/<주제>/  #   글 이미지
├── tools/                 # 실행/빌드/배포 셸 스크립트
├── docs/                  # 문서(이 폴더 포함, 빌드 제외)
└── *.py                   # 루트 Python 유틸리티 스크립트
```

각 폴더의 역할 요약:

| 폴더 | 역할 | 출처 |
| --- | --- | --- |
| `_posts/` | 글 본문. 파일명·front matter 규칙은 [03 문서](03-writing-posts.md) | 직접 작성 |
| `_tabs/` | About/Archives/Categories/Tags/Challenge 페이지 | 일부 커스텀 |
| `_data/` | 글쓴이·연락처·공유·미디어·다국어 데이터 | 일부 커스텀 |
| `_layouts/`, `_includes/` | 레이아웃·HTML 조각 | Chirpy 기본 |
| `_sass/` | 스타일. Bootstrap + Chirpy 변수 | Chirpy 기본 |
| `_javascript/` | 테마 동작 JS(테마 토글, TOC, 클립보드 등) | Chirpy 기본 |
| `_plugins/` | git 기반 수정일 훅 | Chirpy 기본 |
| `assets/` | 이미지·아이콘·번들 JS·피드 | 혼합 |
| `tools/` | 개발·배포 명령 래퍼 | Chirpy 기본 |
| `*.py` | 글 생성/정리/감사 스크립트 | 직접 작성 |

> `_layouts`, `_includes`, `_sass`, `_javascript`, `tools`는 대부분 Chirpy 업스트림 코드입니다. 커스텀이 들어간 지점은 [04. 테마 커스터마이징](04-theme-customization.md)에서 따로 짚습니다.

## 빌드 산출물 흐름

`_javascript`와 `_sass`는 소스이고, 실제 사이트가 쓰는 결과물은 빌드로 생성됩니다.

```text
_javascript/*.js  ──(Rollup + Babel + terser)──▶  assets/js/dist/*.min.js
_sass/**/*.scss   ──(Jekyll/Sass, compressed)──▶  사이트 CSS
Bootstrap CSS     ──(PurgeCSS, build:css)─────▶  미사용 클래스 제거
```

- **JS**: [rollup.config.js](../../rollup.config.js)가 7개 페이지 엔트리(`commons`, `home`, `categories`, `page`, `post`, `misc`, `theme`)와 PWA 2개(`app`, `sw`)를 각각 `assets/js/dist/<name>.min.js`로 번들합니다. `theme`은 전역 `Theme` 객체로, PWA 번들은 Jekyll front matter(`permalink: /:basename`)가 주입됩니다.
- **CSS**: `_sass`는 Jekyll이 컴파일하며 `_config.yml`의 `sass.style: compressed`로 압축됩니다. [purgecss.js](../../purgecss.js)(`npm run build:css`)는 Bootstrap에서 실제 사용되는 클래스만 남깁니다.
- **HTML**: `_config.yml`의 `compress_html` 설정으로 프로덕션 빌드 시 주석·공백이 제거됩니다(`development` 환경은 제외).

빌드에서 제외되는 항목은 [_config.yml](../../_config.yml)의 `exclude` 목록에 있습니다: `docs`, `tools`, `README.md`, `LICENSE`, `purgecss.js`, `*.config.js`, `package*.json`, `*.gem`, `*.gemspec`. 단, 루트의 `*.py` 스크립트는 이 목록에 없어 빌드 시 `_site/`로 그대로 복사됩니다(페이지로 렌더링되진 않음). 자세한 내용은 [05. Python 스크립트](05-python-scripts.md) 참고.

빌드/실행 명령의 구체적인 사용법은 [02. 개발 시작](02-getting-started.md)을 참고하세요.
