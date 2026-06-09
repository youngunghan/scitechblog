# 트러블슈팅 / 개발노트 글 작성 가이드

트러블슈팅 글(겪은 문제와 해결 과정을 기록하는 개발노트)을 쓸 때의 **내용 구조**와 **스타일**을 정리합니다. 파일명·front matter 필드의 일반 규칙은 중복하지 않고 [03. 글 작성 규칙](../guide/03-writing-posts.md)을 참고하세요. 이 문서는 그 위에 트러블슈팅 글 특유의 구성만 다룹니다.

> **언어 정책**: 블로그 글(`_posts/*.md`)은 **모두 영어**로 씁니다. 작성자용 내부 문서(`docs/guide`, `docs/blog_post`)만 한국어입니다. 즉 이 가이드는 한국어지만, 여기서 만드는 결과물(글 본문)은 영어로 작성합니다. 아래 템플릿·예시도 영어로 둡니다.

이 문서가 본보기로 삼는 실제 글:

| 글 | 다루는 문제 | 비고 |
| --- | --- | --- |
| [troubleshooting-image-paths](../../_posts/2025-11-30-troubleshooting-image-paths.md) | Jekyll 이미지 경로(double baseurl) | 단일 문제형 |
| [troubleshooting-latex-rendering](../../_posts/2025-12-01-troubleshooting-latex-rendering.md) | LaTeX 미렌더링(`math: true` 누락) | 단일 문제 + 자동화 |
| [troubleshooting-mermaid-diagram-syntax](../../_posts/2025-12-24-troubleshooting-mermaid-diagram-syntax.md) | Mermaid PDF 내보내기 구문 오류 | 다중 문제형 |
| [cicd-pipeline-fastapi](../../_posts/2025-11-25-cicd-pipeline-fastapi.md) | CI/CD 파이프라인 구축 중 발생한 5개 이슈 | 다중 문제형(긴 글) |
| [troubleshooting-visitor-counter](../../_posts/2025-11-26-troubleshooting-visitor-counter.md) | 방문자 카운터 통합 | **반면교사**(아래 참고) |

## 섹션 구조 (H2 기준)

본문 헤더는 항상 `## `(H2)에서 시작합니다. `#`(H1) 단독 사용 금지 — 제목은 front matter `title`이 담당합니다. 기본 골격은 다음과 같습니다.

```text
## Introduction
## Problem 1: <짧고 구체적인 제목>
### Symptom
### Root Cause       (필요 시 ### Root Cause Analysis)
### Analysis         (선택: 스택 트레이스/표로 더 파고들 때)
### Solution
## Problem 2: <...>
### Symptom
### Root Cause
### Solution
## Conclusion        (또는 ## Key Takeaways)
```

각 섹션의 역할:

| 섹션 | 레벨 | 무엇을 담나 | 분량 감각 |
| --- | --- | --- | --- |
| `Introduction` | H2 | 맥락(언제·어디서) + 한 줄 증상 미리보기. "왜 이 글인가" | 2~4문장 |
| `Problem N: 제목` | H2 | 문제 하나를 캡슐화. 제목은 증상이 보이게 구체적으로 | 헤더만 |
| `Symptom` | H3 | **실제로 본** 에러 메시지·깨진 화면·재현 코드 | 코드/text 블록 위주 |
| `Root Cause` | H3 | 왜 그 증상이 났는지. Symptom의 에러와 1:1로 맞물려야 함 | 핵심 1문단 |
| `Analysis` | H3(선택) | 스택 트레이스, 비교 표, 조사 과정. Root Cause를 뒷받침 | 표/코드 |
| `Solution` | H3 | Before/After 코드 + 한 줄 교훈 | 코드 + Lesson |
| `Conclusion` / `Key Takeaways` | H2 | 재사용 가능한 일반 규칙 1~5개로 압축 | 번호 리스트 |

> 단일 문제 글(예: image-paths, latex-rendering)은 `## Problem N` 대신 `## The Problem` → `## Root Cause Analysis` → `## The Solution` → `## Conclusion`의 평탄한 H2 구조를 써도 됩니다. 문제가 2개 이상이면 `## Problem N` + 하위 `### Symptom/Root Cause/Solution` 패턴으로 가는 것이 스캔하기 좋습니다.

### Introduction 작성 요령

- 마이그레이션·신규 기능 추가 등 **언제 어디서** 문제를 만났는지로 시작합니다.
- 마지막에 한 줄 증상을 미리 보여 독자를 끌어당깁니다.

cicd-pipeline-fastapi의 도입부가 좋은 예입니다(영문 그대로 인용):

> What seemed straightforward turned into a multi-hour debugging session that taught me valuable lessons about Docker, async/sync database drivers, and SSH authentication.

### Symptom 작성 요령

- **실제로 재현되는 것만** 적습니다. 본 적 없는 에러를 "이럴 수도 있다"며 지어내지 않습니다.
- 에러는 ```` ```text ```` 또는 ```` ```python ````(스택 트레이스) 블록에 원문 그대로 붙입니다.

```text
internal image /scitechblog/scitechblog/assets/img/posts/algo/leetcode.png does not exist
```

위처럼 **double baseurl** 같은 결정적 단서가 보이도록 자릅니다.

### Solution 작성 요령

- Before/After를 나란히 보여 줍니다. 주석으로 `<!-- Before -->`, `<!-- After -->`를 답니다.

```html
<!-- Before -->
<script src="//busuanzi.ibruce.info/..."></script>

<!-- After -->
<script src="https://busuanzi.ibruce.info/..."></script>
```

- 문제마다 `**Lesson:**` 또는 `**Key Takeaway:**` 한 줄로 일반화합니다. cicd-pipeline-fastapi가 문제마다 `**Lesson:**`을 붙인 방식이 모범입니다.

## 핵심 원칙: Symptom과 Root Cause를 맞물리게 하라

트러블슈팅 글의 신뢰도는 "보인 에러(Symptom)"와 "설명한 원인(Root Cause)"이 **정확히 같은 대상을 가리키는가**에서 갈립니다.

> **반면교사 — visitor-counter 글**: 초안에서 Problem 2의 Symptom에는 두 에러(① `#busuanzi_value_site_pv` 내부 해시 링크 깨짐, ② protocol-relative `//` URL)가 함께 나열됐는데, Root Cause는 사실상 ②(`//` 접두사)만 설명하고 ①은 거의 묻혀 버렸습니다. 독자는 "그래서 해시 에러는 왜 났는데?"를 알 수 없었습니다. (게시된 글은 이후 ①·②를 모두 설명하도록 수정됐으므로, 이 사례는 초안 단계의 반면교사입니다.) 교훈: **Symptom에 두 에러를 보였으면 Root Cause도 둘 다 설명**하거나, 아예 Problem을 둘로 쪼개세요.

체크 질문:

- Symptom에 보인 모든 에러 줄이 Root Cause에서 한 번씩 설명되는가?
- Root Cause가 Symptom에 없던 새 현상을 끌어오지 않는가?
- 에러 메시지의 결정적 토큰(예: `scitechblog/scitechblog`, `MissingGreenlet`, `attempted methods [none]`)이 원인 설명과 단어 수준에서 연결되는가?

문제가 서로 다른 두 원인을 가진다면 억지로 한 Problem에 묶지 말고 `## Problem N`을 추가로 나눕니다. mermaid 글이 `AND/OR`, `<english>`, `<meta>`를 각각 Problem 1·2·3으로 분리한 것이 좋은 예입니다.

## 기술 주장은 공식 문서로 교차검증

트러블슈팅 글은 사실 주장이 많습니다. **추측을 단정처럼 쓰지 마세요.** 검증된 사실과 경험적 관찰을 명확히 구분합니다.

- **검증된 사실**은 단정해도 좋지만 가능하면 출처를 답니다. 예: Mermaid 플로차트에서 공식 예약어는 소문자 `end` 하나뿐입니다(Mermaid 공식 문서 flowchart "Keywords" 항목 기준). 따라서 `AND`/`OR`가 깨지는 현상을 "예약어라서"라고 단정하면 **틀린 설명**입니다.
- **경험적 관찰**(공식 문서에 없는 동작)은 그렇게 명시합니다. mermaid 글의 표현을 그대로 본보기로 삼으세요:

> This isn't a documented Mermaid feature, so treat the following as an empirical observation rather than a rule.

```markdown
> Note: the only officially reserved keyword in Mermaid flowcharts is the lowercase `end`.
> `AND` and `OR` are *not* documented reserved operators; this is just a workaround.
{: .prompt-info }
```

- **버전·포트·명령** 같은 사실은 직접 확인합니다. 추측 금지.
  - 도구 버전은 실제 실행 환경에서 확인해 적습니다(예: mermaid 글의 `mermaid version 11.12.2`는 에러 메시지에 찍힌 실제 값).
  - Docker Compose 호출은 v2 플러그인 `docker compose`가 표준이고 최상위 `version:` 키는 obsolete입니다(Docker 공식 문서 확인). cicd 글이 이를 `.prompt-tip`으로 정확히 짚었습니다.
  - 포트 매핑(`"8000:8080"`)이나 EC2 보안 그룹 포트(22/SSH, 8000/app) 같은 값은 실제 설정 파일과 일치시킵니다.

> Chirpy의 `.prompt-info` / `.prompt-tip` / `.prompt-warning` 블록은 "이건 검증된 보충 사실"임을 시각적으로 알리기에 좋습니다. 경험적 관찰과 공식 사실을 구분해 표시할 때 활용하세요.

## front matter 예시

일반 규칙은 [03. 글 작성 규칙 — Front matter 스키마](../guide/03-writing-posts.md#front-matter-스키마)를 따릅니다. 트러블슈팅 글에서 주의할 점만:

- `categories`는 **`Troubleshooting`을 항상 보조(2번째) 분류**로 둡니다. 대분류는 주제 도메인입니다.
  - 실제 사용 예: `[Blogging, Troubleshooting]`, `[Development, Troubleshooting]`, `[Development, Jekyll]`, `[DevOps, CI/CD]`
- 수식이 있으면 `math: true`, Mermaid 다이어그램이 있으면 `mermaid: true`를 켭니다(둘 다 없으면 넣지 않습니다).
- 대표 이미지는 `assets/img/posts/troubleshooting/`에 모으는 관례입니다. front matter `image.path`는 **맨 앞 슬래시 없이** 씁니다.

```yaml
---
title: "[Troubleshooting] <Concise, Symptom-Visible Title>"
date: 2026-06-09 10:00:00 +0900
categories: [Development, Troubleshooting]   # Troubleshooting은 항상 2번째
tags: [jekyll, chirpy, ci-cd, htmlproofer]
description: "One-line summary of the symptom and the fix."
image:
  path: assets/img/posts/troubleshooting/thumbnail.png   # 슬래시 없음
  alt: Troubleshooting Log
author: seoultech
math: true       # 수식 있을 때만
mermaid: true    # 다이어그램 있을 때만
---
```

> 본문 인라인 이미지는 front matter와 반대로 **맨 앞에 `/`**를 붙입니다: `![alt](/assets/img/posts/troubleshooting/foo.png)`. 배경은 [03 문서 이미지 경로 규칙](../guide/03-writing-posts.md#이미지-경로-규칙) 참고.

## 영어 복붙 템플릿

새 다중 문제형 트러블슈팅 글의 시작점입니다. **본문은 영어**로 채웁니다. Python 코드를 넣을 때는 author house-style 블록 종료 마커(`# end def`, `# end for`, `# end if`)를 유지합니다.

````markdown
---
title: "[Troubleshooting] <Concise, Symptom-Visible Title>"
date: YYYY-MM-DD HH:MM:SS +0900
categories: [Development, Troubleshooting]
tags: [tag1, tag2, troubleshooting]
description: "One-line summary of the symptom and the fix."
image:
  path: assets/img/posts/troubleshooting/thumbnail.png
  alt: Troubleshooting Log
author: seoultech
math: true
mermaid: true
---

## Introduction

While <doing X>, I ran into <problem>. It looked simple, but it took
<time/iterations> to fix. This post documents the symptoms, the root
causes, and the solutions.

## Problem 1: <Specific, symptom-visible title>

### Symptom

I saw this error (reproduced exactly):

```text
<paste the real error message here>
```

### Root Cause

<Explain why the exact tokens in the Symptom appear. Every error line
shown above must be accounted for here.>

### Solution

```diff
- <before>
+ <after>
```

**Lesson:** <one-line generalizable takeaway>

## Problem 2: <Specific title>

### Symptom

<...>

### Root Cause Analysis

| Pattern | Result | Reason |
|---------|--------|--------|
| `<case A>` | Error | <why> |
| `<case B>` | Works | <why> |

### Solution

<before/after>

## Conclusion

**Key Takeaways:**
1. <reusable rule 1>
2. <reusable rule 2>
3. <reusable rule 3>
````

Python 자동화 스크립트를 본문에 넣는 경우의 house-style 예(블록 종료 마커 유지):

```python
def enable_math_in_files():
    for file_path in glob.glob("_posts/*.md"):
        content = open(file_path).read()
        if "math: true" in content:
            continue
        # end if
        # ... insert math: true ...
    # end for
# end def
```

## 게시 후 검증 체크리스트

글을 올리기 전/직후에 확인합니다.

- [ ] **언어**: 본문이 전부 영어인가? (작성자 메모가 한국어로 새지 않았는지)
- [ ] **헤더 레벨**: 본문 헤더가 `## `에서 시작하는가? `#`(H1) 단독 사용은 없는가?
- [ ] **Symptom ↔ Root Cause 정합성**: Symptom에 보인 모든 에러 줄이 Root Cause에서 설명되는가? (visitor-counter 사례 재발 방지)
- [ ] **재현성**: 붙여 넣은 에러 메시지·명령이 실제로 발생/실행되는 것인가? 지어낸 출력은 없는가?
- [ ] **사실 검증**: 버전·포트·예약어 등 단정한 사실을 공식 문서로 확인했는가? 추측은 "empirical observation"으로 명시했는가?
- [ ] **front matter**: `categories`에서 `Troubleshooting`이 2번째인가? 수식/다이어그램이 있으면 `math: true`/`mermaid: true`를 켰는가?
- [ ] **이미지 경로**: front matter `image.path`는 슬래시 없이, 본문 인라인 이미지는 `/assets/...`로 시작하는가? 파일이 `assets/img/posts/troubleshooting/`에 실제로 있는가?
- [ ] **Mermaid 렌더링**: 다이어그램이 GitHub Pages에서 깨지지 않는가? (PDF 전용 회피책인 `<한글>`·`_AND_`가 블로그 본문에 불필요하게 남지 않았는지)
- [ ] **수식 렌더링**: `$...$` / `$$...$$`가 raw text로 나오지 않는가? (`math: true` 확인)
- [ ] **링크 무결성(로컬)**: 빌드 + html-proofer로 내부 링크·이미지를 검사했는가?

링크 검사 명령(레포 표준):

```bash
bash tools/test.sh
# 내부적으로: bundle exec jekyll b (production) 후
#   bundle exec htmlproofer _site --disable-external ...
```

> CI에서도 같은 검사를 돕니다(`.github/workflows/ci.yml` → `tools/test.sh`, `pages-deploy.yml` → `htmlproofer _site --disable-external`). 로컬에서 통과시키면 배포 단계 실패를 미리 막을 수 있습니다. 빌드·배포 흐름 전반은 [02. 개발 시작 — CI/CD와 배포](../guide/02-getting-started.md#cicd와-배포) 참고.

## 요약

| 원칙 | 한 줄 |
| --- | --- |
| 구조 | `## Introduction` → `## Problem N`(+`### Symptom/Root Cause/Solution`) → `## Conclusion` |
| 정합성 | Symptom의 에러와 Root Cause 설명을 1:1로 맞물리게 |
| 재현성 | 실제로 본/돌아가는 에러·명령만 기록 |
| 정직성 | 검증된 사실은 출처와 함께 단정, 관찰은 관찰이라고 표시 |
| 일관성 | 본문 영어 · 헤더 `## ` · `Troubleshooting`은 2번째 카테고리 |
