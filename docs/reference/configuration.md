# 사이트 설정 레퍼런스

> **범위:** 공개 가능한 Jekyll·사이트 설정 키. 정본은 [_config.yml](../../_config.yml)이며 시크릿 값은 다루지 않음.
> **대상:** 개발자 · 운영자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

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
