# 로컬 개발 Quickstart

> **범위:** 의존성 설치부터 로컬 실행과 production 검증까지의 happy path. 글 작성은 [write-posts.md](../how-to/write-posts.md) 참고.
> **대상:** 처음 저장소를 실행하는 개발자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

## 1. 사전 요구

| 도구 | 기준 | 용도 |
|---|---|---|
| Ruby | `3.3` | Jekyll·Bundler |
| Node.js | [.nvmrc](../../.nvmrc) 값 | Rollup·Stylelint·ESLint |
| npm | Node.js 포함 버전 | lockfile 기반 frontend 설치 |

## 2. 설치

```bash
bundle install
npm ci --ignore-scripts
```

`Gemfile.lock`과 `package-lock.json`은 로컬·CI가 같은 버전을 사용하기 위한 정본입니다. 임의로 삭제하지 않습니다.

## 3. 자산 검증과 빌드

```bash
npm test
npm run build
```

`npm test`는 JavaScript와 SCSS lint를 실행합니다. `npm run build`가 `assets/js/dist/`와 `_sass/vendors/`를 생성합니다.

## 4. 로컬 실행

```bash
bash tools/run.sh
```

브라우저에서 <http://127.0.0.1:4000/scitechblog/>를 열어 홈, 글, 테마 전환과 모바일 레이아웃을 확인합니다.

## 5. Production 검증

```bash
bash tools/test.sh
```

이 명령은 production 모드로 빌드한 뒤 HTML-Proofer로 내부 링크·이미지·스크립트 참조를 검사합니다. 외부 URL 상태는 별도 검사 대상입니다.

## 관련 문서

- [아키텍처](../explanation/architecture.md)
- [글 작성](../how-to/write-posts.md)
- [유지보수 도구](../reference/maintenance-tools.md)
