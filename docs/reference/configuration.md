# 사이트 설정 레퍼런스

> **범위:** 공개 가능한 Jekyll·사이트 설정 키. 정본은 [_config.yml](../../_config.yml)이며 시크릿 값은 다루지 않음.
> **대상:** 개발자 · 운영자.
> **상태:** 구현 반영 — 기준일 2026-07-14.

## 1. 사이트 식별

| 설정 | 타입 | 현재 값 | 의미 |
|---|---|---|---|
| `title` | string | `CSMAIR` | 사이트 제목 |
| `url` | URL | `https://youngunghan.github.io` | origin |
| `baseurl` | path | `/scitechblog` | GitHub Pages 프로젝트 경로 |
| `lang` | language tag | `en` | UI 기본 언어 |
| `timezone` | IANA zone | `Asia/Seoul` | 글 날짜 기준 |
| `paginate` | integer | `10` | 홈 페이지 글 수 |

## 2. 콘텐츠 기본값

| 설정 | 타입 | 현재 값 | 의미 |
|---|---|---|---|
| `defaults.posts.layout` | string | `post` | 글 레이아웃 |
| `defaults.posts.permalink` | pattern | `/posts/:title/` | 글 URL |
| `defaults.posts.toc` | boolean | `true` | 글 목차 |
| `comments.provider` | string/null | 비활성 | 외부 댓글 provider |
| `pwa.enabled` | boolean | `true` | PWA manifest·service worker |

## 3. 빌드 제외

`exclude`는 내부 문서, 개발 도구, 패키지 메타데이터와 테스트 fixture가 사이트 artifact로 복사되는 것을 막습니다. 새 루트 도구를 추가할 때 [_config.yml](../../_config.yml)의 `exclude`도 갱신합니다.

## 4. 변경 검증

설정을 바꾼 뒤 [Quickstart §5 Production 검증](../tutorials/quickstart.md#5-production-검증)을 실행합니다. `url`과 `baseurl` 변경은 canonical URL, feed, sitemap, PWA scope까지 함께 확인합니다.

## 5. 방문자 카운터 / 웹 분석 (Busuanzi · GoatCounter)

사이드바 하단(`_includes/sidebar.html`)의 "Total Views" 카운터는 [Busuanzi](https://busuanzi.ibruce.info/)라는 외부 스크립트로 동작하며, 별도 설정 없이 현재 활성 상태입니다. Chirpy 테마에 내장된 GoatCounter 연동은 계정을 만든 뒤 ID만 채우면 되도록 준비만 되어 있고, 기본값은 비어 있어 비활성입니다.

| 설정 | 타입 | 현재 값 | 의미 |
|---|---|---|---|
| `analytics.goatcounter.id` | string | 비어 있음 | GoatCounter 사이트 코드(`https://<id>.goatcounter.com`의 `<id>`). 채우면 사이트 전역 추적 스크립트(`_includes/analytics/goatcounter.html`)가 `_includes/head.html`을 통해 모든 페이지에 삽입됨 |
| `pageviews.provider` | string | 비어 있음 | 글별 조회수 표시 provider. 현재 `goatcounter`만 지원 |

### GoatCounter 활성화 절차

1. [goatcounter.com](https://www.goatcounter.com/)에서 계정과 사이트를 만들고 사이트 코드(서브도메인)를 확보합니다.
2. GoatCounter 대시보드의 **Settings → Site settings**에서 "Allow adding visitor counts on your website" 옵션을 켭니다. 이 옵션이 꺼져 있으면 공개 `/counter/<path>.json` 엔드포인트가 막혀 있어 글 페이지의 조회수 fetch가 항상 실패합니다 (아래 문제 해결 참고). ID를 채우기 전에 미리 켜 두는 것을 권장합니다. GoatCounter는 이 엔드포인트 응답을 최대 4시간까지 캐시하므로, 설정을 켠 직후 바로 확인해도 반영이 지연될 수 있습니다.
3. `_config.yml`의 `analytics.goatcounter.id`에 사이트 코드를 채웁니다. → 사이트 전역 추적 스크립트가 켜집니다(단, `jekyll.environment == 'production'`일 때만 — `_includes/head.html`의 분석 스크립트 블록이 production 빌드에서만 삽입되므로 평범한 `bundle exec jekyll s` 로컬 서버에서는 트래커가 나타나지 않는 것이 정상입니다).
4. `pageviews.provider`를 `goatcounter`로 채웁니다. → `_layouts/post.html`의 `{% if site.pageviews.provider and site.analytics[site.pageviews.provider].id %}` 가드가 통과하며 글 페이지에 조회수(`_includes/pageviews/goatcounter.html`)가 표시됩니다. **두 값이 모두 채워져야** 글별 조회수가 렌더링됩니다. 하나만 채우면 전역 추적은 되어도 글별 카운터는 나타나지 않습니다.
5. [Quickstart §5 Production 검증](../tutorials/quickstart.md#5-production-검증)으로 빌드·HTML-Proofer를 재실행해 확인합니다.

`_includes/pageviews/goatcounter.html`은 카운터 엔드포인트를 `https://<id>.goatcounter.com/counter/...`로 하드코딩합니다. 자체 호스팅 인스턴스나 커스텀 도메인은 지원하지 않으며, `analytics.goatcounter.id` 하나의 값이 전역 추적 스크립트와 글별 카운터 엔드포인트 양쪽에 그대로 쓰입니다.

**문제 해결 — 모든 글이 조회수 "1"로만 표시됨:** `_includes/pageviews/goatcounter.html`의 fetch `.catch()`는 실패 원인을 구분하지 않고 항상 `1`을 써넣습니다(에러가 화면에 드러나지 않음). 이 "1"의 원인은 하나가 아니므로 단정하지 말고, 먼저 브라우저 개발자 도구 Network 탭에서 `/counter/*.json` 요청의 상태 코드를 확인하세요.
- **403** — 2단계의 "Allow adding visitor counts on your website" 설정이 꺼져 있음. 가장 흔한 원인입니다.
- **404** — 아직 조회 기록이 없는 경로. **새로 게시한 글은 첫 방문 전까지 "1"이 정상**이며 설정 문제가 아닙니다.
- 상태 코드가 정상인데도 "1"이면 광고 차단기가 `*.goatcounter.com` 요청을 막고 있는지([jekyll-theme-chirpy#2412](https://github.com/cotes2020/jekyll-theme-chirpy/discussions/2412) 참고), 또는 위 4시간 캐시 지연 때문인지 확인합니다.

### Busuanzi와의 공존 · 정리

- 두 카운터는 서로 다른 위치에 독립적으로 표시됩니다: Busuanzi는 사이드바 전역 "Total Views"(`#busuanzi_value_site_pv`), GoatCounter pageviews는 글 페이지 내 개별 조회수(`#pageviews`)입니다. 둘 다 켜져 있어도 충돌하지 않습니다.
- GoatCounter로 전환해 Busuanzi를 끄려면 `_includes/sidebar.html`에서 `<!-- #busuanzi_container_site_pv 관련 블록 -->`(nav의 `</nav>` 직후, `.sidebar-bottom` 직전)을 제거합니다. 제거 시 스크립트 태그(`https://` 절대경로 유지)와 `#busuanzi_value_site_pv` span을 가리키는 앵커 링크를 추가하지 않도록 주의합니다 — 과거 html-proofer 실패 이력은 [2025-11-26 트러블슈팅 글](../../_posts/2025-11-26-troubleshooting-visitor-counter.md)에 기록되어 있습니다.
- `THIRD_PARTY_NOTICES.md`는 번들/vendored 코드(Chirpy 테마, 논문 그림, npm/gem 의존성) 범위만 다룹니다. Busuanzi·GoatCounter는 둘 다 외부 호스팅 스크립트를 브라우저가 직접 불러오는 방식(런타임 원격 호출)이라 이 범위 밖이며 별도 고지 항목을 추가하지 않았습니다.
