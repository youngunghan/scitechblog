# 02. 개발 시작

## 환경 준비

| 도구 | 버전(권장) | 용도 |
| --- | --- | --- |
| Ruby + Bundler | 3.1–3.3 (CI 배포는 3.3) | Jekyll 사이트 빌드/실행 |
| Node.js + npm | LTS (`lts/*`) | JS 번들·CSS 최적화·린트 |
| (선택) html-proofer | — | 빌드 결과 링크 검사 (`tools/test.sh`) |

권장 버전은 CI 워크플로 기준입니다(`.github/workflows/`의 `ruby-version`, `node-version`). Jekyll·테마 버전 제약은 [Gemfile](../../Gemfile)(`jekyll ~> 4.3`, `jekyll-theme-chirpy ~> 7.4`)에 있습니다.

처음 한 번 의존성을 설치합니다.

```bash
bundle install   # Gemfile 기준 Ruby 의존성
npm install      # package.json 기준 Node 의존성
```

> 테마 정적 에셋(폰트·아이콘 등)은 **CDN(jsDelivr)** 으로 로드됩니다 — `_config.yml`의 `assets.self_host.enabled`가 비어 있어(=false) self-host를 쓰지 않으므로, 이 레포는 `assets/lib` 서브모듈을 두지 않습니다. 별도 `git submodule` 단계가 필요 없습니다.

## 프런트엔드 에셋 빌드

이 레포는 Chirpy 테마 소스 기반이라 `assets/js/dist/`의 JS 번들이 git에 포함되지 않습니다. 따라서 **로컬 실행 전에 한 번 빌드**해야 스크립트(테마 토글, TOC, 클립보드 등)가 동작합니다.

```bash
npm run build         # build:css + build:js 동시 실행
# 개별 실행
npm run build:css     # purgecss.js — Bootstrap 미사용 클래스 제거
npm run build:js      # Rollup 프로덕션 번들 → assets/js/dist/
npm run watch:js      # JS 소스 변경 감지 후 자동 재번들(개발용)
```

JS를 자주 수정한다면 `npm run watch:js`를 띄워 두고 아래의 Jekyll 서버를 별도 터미널에서 실행하면 편합니다.

## 로컬 실행

```bash
bash tools/run.sh                 # http://127.0.0.1:4000/scitechblog
bash tools/run.sh -H 0.0.0.0      # 다른 기기에서 접속 허용
bash tools/run.sh -p              # production 환경으로 실행
```

[tools/run.sh](../../tools/run.sh)는 내부적으로 `bundle exec jekyll s -l`(LiveReload 포함)을 실행합니다. `-p`를 주면 `JEKYLL_ENV=production`으로 동작해 HTML 압축·애널리틱스 등 프로덕션 설정이 적용됩니다.

> 직접 실행하려면 `bundle exec jekyll serve -l` 도 동일합니다.

## 테스트 / 린트

```bash
npm test            # lint:js + lint:scss
npm run lint:js     # ESLint (eslint.config.js)
npm run lint:scss   # Stylelint (_sass/**/*.scss)
npm run lint:fix:scss   # Stylelint 자동 수정
```

빌드 결과의 링크 무결성까지 확인하려면:

```bash
bash tools/test.sh                       # 빌드 후 html-proofer 검사
bash tools/test.sh -c "_config.yml,_config.prod.yml"   # 다중 config
```

[tools/test.sh](../../tools/test.sh)는 사이트를 `_site/`로 빌드한 뒤 html-proofer로 내부 링크·이미지를 검사합니다.

## tools 스크립트 요약

| 스크립트 | 역할 |
| --- | --- |
| [tools/init.sh](../../tools/init.sh) | **(파괴적) 새 Chirpy 스타터 부트스트랩용.** 아래 경고 참고 |
| [tools/run.sh](../../tools/run.sh) | Jekyll 개발 서버 실행 (`-H` 호스트, `-p` 프로덕션) |
| [tools/test.sh](../../tools/test.sh) | 빌드 + html-proofer 링크 검사 (`-c` 다중 config) |
| [tools/release.sh](../../tools/release.sh) | Chirpy gem 릴리스용(버전 범프·패키지·배포). `production` 브랜치 CD에서 자동 호출됨 |

> ⚠️ **`tools/init.sh`는 이 블로그에서 절대 실행하지 마세요.** 이 스크립트는 새 사용자용 1회성 부트스트랩으로, 마지막 릴리스 커밋으로 `git reset --hard` 후 `git clean -fd`를 하고 `_posts/*`(현재 글 54개 전부), `tools/init.sh`, `tools/release.sh`, 대부분의 `.github/`를 삭제한 뒤 커밋합니다(init.sh:68·69·89). 실행하면 기존 글이 모두 사라집니다.
>
> `tools/release.sh`는 Chirpy **테마 자체**를 RubyGems에 배포하기 위한 스크립트(테마 메인테이너용)입니다. 이 블로그에선 쓰지 않으며, 과거 이를 자동 호출하던 `cd.yml` 워크플로도 제거됐습니다. 글만 운영한다면 신경 쓸 필요가 없습니다.

## CI/CD와 배포

CI/CD는 GitHub Actions([.github/workflows/](../../.github/workflows/))로 구성됩니다. 대표 워크플로:

`.github/workflows/`에는 워크플로가 **2개**입니다(Chirpy 테마 기본 구성을 이 블로그에 맞게 정리한 결과):

| 워크플로 | 트리거 | 역할 |
| --- | --- | --- |
| `pages-deploy.yml` | `main`/`master` push, 수동 실행 (`docs/**`·README·LICENSE만 바뀐 push는 제외) | Jekyll 프로덕션 빌드 → html-proofer 검사 → GitHub Pages 배포 |
| `commitlint.yml` | `master`/`hotfix/*` push, PR | Conventional Commits 형식 검사(헤더 ≤100자) |

> 테마 기본 구성에 있던 나머지 워크플로(`ci.yml`·`lint-js`/`lint-scss`·`codeql`·`cd.yml`·`stale`·`publish`·`pr-filter`)는 블로그 운영에 불필요해 제거했습니다. 빌드·링크 검사(html-proofer)는 `pages-deploy.yml`이 직접 수행합니다.

**사이트 배포 흐름**(`pages-deploy.yml`):

1. `main`(또는 `master`) 브랜치에 push → `pages-deploy.yml` 실행
2. Ruby 셋업 후 Jekyll 프로덕션 빌드(`bundle exec jekyll b`, `JEKYLL_ENV=production`) + html-proofer 검사. **이 워크플로에는 Node/`npm run build` 단계가 없습니다** — JS/CSS 에셋 번들은 여기서 만들지 않습니다.
3. 결과를 GitHub Pages로 게시 → `https://youngunghan.github.io/scitechblog`

사이트 URL은 [_config.yml](../../_config.yml)의 `url`(27행)과 `baseurl`(154행)로 결정되므로, 배포 도메인이 바뀌면 이 두 값을 함께 수정해야 합니다.

**릴리스(gem) 흐름**: 이 레포에는 별도 gem 릴리스 파이프라인이 **없습니다** — 테마 배포용 `cd.yml`(semantic-release)을 제거했습니다. [tools/release.sh](../../tools/release.sh)는 파일로만 남아 있고 자동 호출되지 않으므로, 블로그는 오직 `pages-deploy.yml`로만 빌드·배포됩니다.

> **브랜치 모델**: 사이트는 `main`/`master` push로 배포(`pages-deploy.yml`)되고, commitlint는 `master`/`hotfix/*` push·PR에서 동작합니다. (테마 기본 구성의 `production` gem-릴리스 브랜치 흐름은 `cd.yml` 제거와 함께 더 이상 쓰지 않습니다.)

> 커밋 메시지는 commitlint(Conventional Commits)를 따릅니다. 예: `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`. Husky([.husky/](../../.husky/))가 커밋 시점에 검사합니다.
