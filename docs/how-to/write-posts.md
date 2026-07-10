# 블로그 글 작성

> **범위:** 파일명, front matter, 이미지, 수식과 게시 전 검증. 글 유형별 구성은 [§6 글 유형별 가이드](#6-글-유형별-가이드) 참고.
> **대상:** 블로그 작성자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

## 1. 파일 생성

글은 `_posts/YYYY-MM-DD-kebab-case-slug.md`에 만듭니다. 날짜는 front matter의 `date`와 일치시킵니다. 기존 URL은 파일명을 바꾸면 깨질 수 있으므로 교정 목적만으로 기존 slug를 변경하지 않습니다.

## 2. Front matter

| 키 | 필수 | 형식·의미 |
|---|---:|---|
| `title` | ✅ | 화면과 SEO에 표시할 영어 제목 |
| `date` | ✅ | `YYYY-MM-DD HH:MM:SS +0900` |
| `categories` | ✅ | 대분류·소분류 최대 2개 |
| `tags` | ✅ | 기존 표기와 충돌하지 않는 태그 목록 |
| `description` | ✅ | 검색 결과용 간결한 요약 |
| `author` | 조건부 | `_data/authors.yml`의 키. 기본 저자 사용 시 생략 가능 |
| `image.path` | 권장 | `/` 없이 `assets/img/posts/...` |
| `image.alt` | 이미지 사용 시 ✅ | 이미지가 전달하는 내용을 설명 |
| `math` | 조건부 | 수식이 있을 때만 `true` |
| `mermaid` | 조건부 | Mermaid 블록이 있을 때만 `true` |

## 3. 콘텐츠와 출처

1. 기술 주장은 공식 문서, 원 논문 또는 실제 소스 코드로 검증합니다.
2. 측정값은 데이터 split, 표본수, seed, dependency 버전과 평가 프로토콜을 함께 적습니다.
3. 동일 데이터로 hyperparameter를 선택하고 성능까지 보고하지 않습니다. validation 선택과 locked test 평가를 분리합니다.
4. 외부 공개가 금지된 문제 원문·데이터·정답은 게시하지 않습니다.
5. 제3자 그림은 재사용 조건을 확인하고, 허용되지 않으면 자체 도식으로 교체합니다.

## 4. 이미지와 수식

- 대표 이미지: `image.path: assets/img/posts/<topic>/cover.png`.
- 본문 이미지: `![설명](/assets/img/posts/<topic>/figure.png)`.
- 수식: `math: true`와 `$...$` 또는 `$$...$$`.
- Mermaid: `mermaid: true`와 `mermaid` fenced block.
- 큰 PNG는 게시 크기에 맞게 축소하고 WebP 또는 최적화 PNG를 사용합니다.

## 5. 검증

```bash
npm test
npm run build
bash tools/test.sh
```

코드 예제는 글에서 그대로 추출해 실행하고, 샘플 입력·출력과 본문 수치가 일치하는지 확인합니다. `${{ ... }}`처럼 Liquid와 충돌하는 예제는 `{% raw %}`와 `{% endraw %}`로 감쌉니다.

## 6. 글 유형별 가이드

| 유형 | 문서 |
|---|---|
| 알고리즘 | [post-types/algorithm.md](post-types/algorithm.md) |
| 논문 리뷰 | [post-types/paper-review.md](post-types/paper-review.md) |
| 프로젝트·실험 | [post-types/project-engineering.md](post-types/project-engineering.md) |
| SQL | [post-types/sql.md](post-types/sql.md) |
| 트러블슈팅 | [post-types/troubleshooting.md](post-types/troubleshooting.md) |
