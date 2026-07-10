# Chirpy 소스 관리

> **범위:** 이 저장소가 소유하는 Chirpy 소스와 업그레이드 규칙. 일반 사이트 설정은 [configuration.md](../reference/configuration.md) 참고.
> **대상:** 테마·프런트엔드 개발자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

## 1. 소유 모델

이 저장소는 Chirpy Starter처럼 일부 파일만 override하지 않고, 레이아웃·include·SCSS·JavaScript 소스 전체를 추적합니다. 따라서 Ruby gem만 올리는 방식으로 업그레이드하면 브라우저 bundle과 템플릿 API가 어긋날 수 있습니다.

| 계층 | 버전 정본 | 정책 |
|---|---|---|
| Ruby theme | [Gemfile.lock](../../Gemfile.lock) | `jekyll-theme-chirpy 7.4.1` 고정 |
| npm source/dependencies | [package-lock.json](../../package-lock.json) | `npm ci`로 재현 |
| 추적 소스 | `_layouts`, `_includes`, `_sass`, `_javascript` | 같은 Chirpy 릴리스 계열 유지 |
| 생성 자산 | `_sass/vendors`, `assets/js/dist` | Git 제외, CI에서 생성 |

## 2. 프로젝트별 변경점

| 위치 | 변경 책임 |
|---|---|
| [_config.yml](../../_config.yml) | CSMAIR 메타데이터, `/scitechblog` baseurl, PWA·컬렉션 설정 |
| [_data/authors.yml](../../_data/authors.yml) | `seoultech` 저자 매핑 |
| [_tabs/about.md](../../_tabs/about.md) | 저자·연구 소개 |
| [_tabs/challenge.md](../../_tabs/challenge.md) | 학습 진행 탭과 반응형 스타일 |
| [_includes/sidebar.html](../../_includes/sidebar.html) | 프로젝트 내비게이션과 외부 스크립트 정책 |
| [_plugins/posts-lastmod-hook.rb](../../_plugins/posts-lastmod-hook.rb) `Jekyll::Hooks.register` | Git 이력 기반 수정일 계산 |

## 3. 런타임 계약

### 3.1 테마 전환

7.4.1 소스는 `<html data-mode>`와 `Theme` 메시지 API를 함께 사용합니다. JavaScript와 SCSS에서 사용하는 attribute 또는 event API를 한쪽만 변경하지 않습니다.

### 3.2 페이지별 bundle

`commons.js`는 모든 페이지의 공통 컨트롤을 초기화하고, `home.js`, `post.js`, `page.js` 등은 레이아웃별 기능을 담당합니다. include가 요구하는 DOM 구조를 변경할 때 해당 JavaScript selector도 같은 변경에서 검증합니다.

### 3.3 외부 runtime

댓글, 방문자 집계, analytics처럼 제3자 코드를 실행하는 기능은 provider와 개인정보 처리 조건이 실제로 준비됐을 때만 켭니다. 설정이 비어 있거나 저장소 기능이 꺼져 있으면 script를 삽입하지 않습니다.

## 4. 업그레이드 절차

1. 목표 Chirpy tag를 정하고 Ruby gem과 추적 theme source를 같은 버전으로 갱신합니다. `package.json`은 블로그 전용 metadata를 유지합니다.
2. `bundle update jekyll-theme-chirpy`와 필요한 npm dependency 갱신으로 두 lockfile을 갱신합니다.
3. upstream 대비 프로젝트별 변경점을 다시 적용합니다.
4. `npm test`, `npm run build`, `bash tools/test.sh`를 실행합니다.
5. 데스크톱·모바일에서 테마 전환, TOC, back-to-top, 검색, PWA와 댓글 provider를 smoke test합니다.

버전 일부만 올리는 변경은 허용하지 않습니다.

## 관련 문서

- [아키텍처](architecture.md)
- [Quickstart](../tutorials/quickstart.md)
- [설정 레퍼런스](../reference/configuration.md)
