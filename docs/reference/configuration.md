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

사이드바 하단(`_includes/sidebar.html`)의 "Total Views" 카운터는 [Busuanzi](https://busuanzi.ibruce.info/)라는 외부 스크립트로 동작하며, 별도 설정 없이 계속 활성 상태입니다. Chirpy 테마에 내장된 GoatCounter 연동도 **2026-07-14부로 활성화**되었습니다 — 사이트 코드는 `scitechblog`이며, 대시보드는 https://scitechblog.goatcounter.com/ 입니다. 대시보드의 "Allow adding visitor counts on your website" 옵션도 켜져 있음을 확인했습니다(`curl https://scitechblog.goatcounter.com/counter/TOTAL.json` → HTTP 200). 아래에서 설명하듯 **Busuanzi는 의도적으로 계속 유지**합니다.

| 설정 | 타입 | 현재 값 | 의미 |
|---|---|---|---|
| `analytics.goatcounter.id` | string | `scitechblog` | GoatCounter 사이트 코드(`https://<id>.goatcounter.com`의 `<id>`). 사이트 전역 추적 스크립트(`_includes/analytics/goatcounter.html`)가 `_includes/head.html`을 통해 모든 페이지에 삽입됨 |
| `pageviews.provider` | string | `goatcounter` | 글별 조회수 표시 provider. 현재 `goatcounter`만 지원 |

### 활성화 내역 (참고: 활성화 당시 확인한 동작 경로)

두 설정 모두 채워져 있어야 아래 두 기능이 함께 켜집니다. 실제로 코드를 읽어 확인한 경로는 다음과 같습니다.

1. `analytics.goatcounter.id`가 채워져 있으면 → `_includes/head.html`의 `{% if jekyll.environment == 'production' %}` 블록 안에서 `site.analytics` 순회 중 `goatcounter.id`가 비어 있지 않으므로 `_includes/analytics/goatcounter.html`(전역 추적 스크립트, `gc.zgo.at/count.js`)이 삽입됩니다. **production 빌드에서만** 삽입되므로, 평범한 `bundle exec jekyll s` 로컬 서버에서는 트래커가 나타나지 않는 것이 정상입니다 — 확인하려면 `JEKYLL_ENV=production`으로 빌드해야 합니다.
2. `analytics.goatcounter.id`와 `pageviews.provider: goatcounter`가 둘 다 채워져 있으면 → `_includes/js-selector.html`과 `_layouts/post.html`의 `{% if site.pageviews.provider and site.analytics[site.pageviews.provider].id %}` 가드가 통과해 글 페이지에 조회수(`_includes/pageviews/goatcounter.html`)가 표시됩니다.
3. 같은 두 설정을 보고 `assets/js/data/swconf.js`가 서비스워커의 `interceptor.urlPrefixes`에 `https://scitechblog.goatcounter.com/counter/`를 추가합니다. 이 목록은 캐시 **제외** 목록(`_javascript/pwa/sw.js`가 여기 매칭되는 URL은 캐시하지 않고 항상 네트워크로 통과시킴)이므로 기존 PWA 캐시 동작에는 영향이 없고, 조회수 API 응답이 오래된 캐시로 굳어버리는 것만 막아줍니다.

`_includes/pageviews/goatcounter.html`은 카운터 엔드포인트를 `https://<id>.goatcounter.com/counter/...`로 하드코딩합니다. 자체 호스팅 인스턴스나 커스텀 도메인은 지원하지 않으며, `analytics.goatcounter.id` 하나의 값이 전역 추적 스크립트와 글별 카운터 엔드포인트 양쪽에 그대로 쓰입니다.

**당분간 모든 글이 조회수 "1"로 표시되는 것은 정상입니다.** `_includes/pageviews/goatcounter.html`의 fetch `.catch()`는 실패 원인을 구분하지 않고 항상 `1`을 써넣습니다(에러가 화면에 드러나지 않음). 트래커 설치 직후에는 아직 어떤 글에도 방문 기록이 쌓이지 않았으므로(`curl .../counter/%2Fscitechblog%2Fposts%2F<slug>.json` → HTTP 404, "아직 데이터 없음"을 뜻함), 실제 방문이 쌓이기 전까지는 모든 글이 "1"로 보이는 것이 버그가 아니라 예상된 초기 상태입니다. 게다가 **GoatCounter는 `/counter` 응답을 최대 4시간까지 캐시**하므로, 새로 발생한 트래픽도 즉시 반영되지 않고 최대 4시간 지연될 수 있습니다. 이 "1"의 원인은 하나가 아니므로 단정하지 말고, 먼저 브라우저 개발자 도구 Network 탭에서 `/counter/*.json` 요청의 상태 코드를 확인하세요.
- **403** — 대시보드의 "Allow adding visitor counts on your website" 설정이 꺼져 있음. 현재는 켜져 있는 것을 확인했으므로 다시 403이 뜬다면 설정이 되돌아간 것입니다.
- **404** — 아직 조회 기록이 없는 경로. **새로 게시한 글, 또는 트래커 설치 직후에는 첫 방문 전까지 "1"이 정상**이며 설정 문제가 아닙니다.
- 상태 코드가 정상(200)인데도 "1"이면 광고 차단기가 `*.goatcounter.com` 요청을 막고 있는지([jekyll-theme-chirpy#2412](https://github.com/cotes2020/jekyll-theme-chirpy/discussions/2412) 참고), 또는 위 4시간 캐시 지연 때문인지 확인합니다.

### Busuanzi를 함께 유지하는 이유

- **Busuanzi는 제거하지 않고 GoatCounter와 나란히 계속 운영합니다.** 이유: Busuanzi가 그동안 누적해 온 사이드바 "Total Views" 총계는 GoatCounter 도입 이전 트래픽을 포함하고 있고, GoatCounter는 이 과거 데이터를 소급(backfill)할 방법이 없습니다. Busuanzi를 끄면 그 누적치가 사라지므로, 사이드바의 누적 총계는 Busuanzi가 계속 담당하고 GoatCounter는 글별 조회수 + 대시보드 통계를 새로 추가하는 역할로 둡니다.
- 두 카운터는 서로 다른 위치에 독립적으로 표시되어 충돌하지 않습니다: Busuanzi는 사이드바 전역 "Total Views"(`#busuanzi_value_site_pv`), GoatCounter pageviews는 글 페이지 내 개별 조회수(`#pageviews`)입니다.
- (참고, 현재는 적용하지 않음) 만약 향후 Busuanzi를 끄기로 결정한다면 `_includes/sidebar.html`에서 `<!-- #busuanzi_container_site_pv 관련 블록 -->`(nav의 `</nav>` 직후, `.sidebar-bottom` 직전)을 제거하면 됩니다. 제거 시 스크립트 태그(`https://` 절대경로 유지)와 `#busuanzi_value_site_pv` span을 가리키는 앵커 링크를 추가하지 않도록 주의합니다 — 과거 html-proofer 실패 이력은 [2025-11-26 트러블슈팅 글](../../_posts/2025-11-26-troubleshooting-visitor-counter.md)에 기록되어 있습니다.
- `THIRD_PARTY_NOTICES.md`는 번들/vendored 코드(Chirpy 테마, 논문 그림, npm/gem 의존성) 범위만 다룹니다. Busuanzi·GoatCounter는 둘 다 외부 호스팅 스크립트를 브라우저가 직접 불러오는 방식(런타임 원격 호출)이라 이 범위 밖이며 별도 고지 항목을 추가하지 않았습니다.
