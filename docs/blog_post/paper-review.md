# 논문 리뷰 글 작성 가이드

논문 1편을 깊게 읽고 정리하는 **Paper Review** 유형 글의 콘텐츠 구조와 스타일을 다룹니다. front matter 스키마·파일명·이미지 경로 같은 공통 규칙은 [03. 글 작성 규칙](../guide/03-writing-posts.md)에 정의되어 있으니, 이 문서는 **섹션 구성**과 **표 검증**에 집중합니다.

> **언어 정책**: 이 가이드(`docs/blog_post/`, `docs/guide/`)는 한국어로 씁니다. 그러나 실제 **블로그 글(`_posts/*.md`)은 모두 영어**로 작성합니다. 논문 리뷰는 OUTTA AI Tech Blog의 한국어 원문을 영어로 옮긴 번역/재게시본인 경우가 많습니다(출처는 prompt-info로 표시).
{: .prompt-info }

## 언제 이 유형을 쓰는가

- **논문 1편**을 처음부터 끝까지 읽고 정리할 때. 서베이/비교 글이 아니라 단일 논문 deep-dive입니다.
- 실제 예시 (모두 `categories` 첫 요소가 `Paper Review`):

| 글 | 분야 | OUTTA 원문(번역 출처) |
| --- | --- | --- |
| [DreamBooth](../../_posts/2024-05-29-review-dreambooth.md) | Generative AI | [blog.outta.ai/73](https://blog.outta.ai/73) |
| [UNet++](../../_posts/2025-01-08-review-unet-plus-plus.md) | Medical AI | [blog.outta.ai/127](https://blog.outta.ai/127) |
| [KAD (Knowledge-enhanced VLM)](../../_posts/2024-12-28-review-knowledge-enhanced-vlm.md) | Medical AI | [blog.outta.ai/103](https://blog.outta.ai/103) |
| [Data Contamination](../../_posts/2025-08-23-review-data-contamination.md) | NLP | [blog.outta.ai/339](https://blog.outta.ai/339) |

- 파일명 슬러그는 `review-` 접두사를 씁니다: `2025-01-08-review-unet-plus-plus.md`.

## 권장 섹션 구조 (H2)

본문 헤더는 항상 `## `(H2)에서 시작합니다. 단일 `#`은 쓰지 않습니다(제목은 front matter `title`이 담당). 권장 흐름:

```text
> .prompt-info 블록 (논문 arXiv/DOI + OUTTA 원문 안내)
## Why I Read This Paper
## Abstract            (또는 ## Introduction)
## Context / Related Work   (강한 권장 — 기존 연구 대비 위치)
## Method(s)           (하위 항목은 ### 로)
## Experiments / Results   (수치 표 포함)
## Conclusion & Insight
###   Strengths / Limitations / Open Questions (권장)
```

각 섹션의 역할:

| 섹션 | 내용 | 비고 |
| --- | --- | --- |
| `## Why I Read This Paper` | 이 논문을 왜 읽었는지, 무엇이 인상적이었는지 1인칭으로 | 리뷰의 시그니처 도입부. 4편 모두 이 섹션으로 시작 |
| `## Abstract` / `## Introduction` | 문제 정의·배경 + **논문의 핵심 기여(contributions)를 명시**. 둘 다 두거나 하나만 (DreamBooth는 둘 다, UNet++/KAD/Contamination은 Introduction만) | 원논문 흐름에 맞춰 선택. Keshav의 "Category·Contributions"를 앞에서 짚으면 좋음 |
| `## Context / Related Work` *(강한 권장)* | 이 논문이 **기존 연구 대비 무엇이 다른지** 위치 짓기 | Keshav 3-pass의 Context/Contribution은 핵심. 아주 짧은 리뷰만 Introduction에 녹임 |
| `## Method` / `## Methods` | 핵심 아이디어. 하위 기법은 `### `로 분리 (예: UNet++의 `### 1. Nested Dense Skip Connections`) | 그림은 본문 인라인 이미지로 — **출처 표시 필수**(아래 그림 규칙) |
| `## Experiments` / `## Results` | 정량 결과 표 + 지표 설명 | **표 검증이 가장 중요한 곳** (아래 참고) |
| `## Conclusion & Insight` | 짧은 요약 + **명시적 강점·한계·열린 질문(critique)** + 후속 연구 | **리뷰는 요약이 아니라 commentary** — 한계를 한 구절로 흘리지 말 것 (아래 참고) |

> **요약 ≠ 비평.** "리뷰의 가장 중요한 요소는 단순 요약이 아니라 commentary"입니다([UNC Writing Center](https://writingcenter.unc.edu/tips-and-tools/book-reviews/)). 학회 리뷰 양식도 Summary와 **Strengths/Weaknesses·Limitations를 별도 항목으로 분리**하고([NeurIPS](https://neurips.cc/Conferences/2025/ReviewerGuidelines)·[ICLR](https://iclr.cc/Conferences/2025/ReviewerGuide)), Keshav의 3-pass도 마지막에 "강점·약점, 숨은 가정, 빠진 인용"을 짚으라고 합니다. `Conclusion & Insight`에서 **강점과 한계를 각각 또렷이** 적으세요(필요하면 `### Strengths` / `### Limitations`로 분리). 한계를 한 문장으로 흘리면 리뷰가 약해집니다.
{: .prompt-tip }

### prompt-info 블록 관례

`## Why I Read This Paper` **바로 위**에, **논문 원문(arXiv/DOI) 링크**와 OUTTA 한국어 원문 링크를 안내하는 `.prompt-info` 블록쿼트를 둡니다. 단일 논문 리뷰의 1차 출처는 OUTTA 번역이 아니라 **논문**이고, 독자가 표 수치를 원문과 대조할 수 있어야 하므로 **arXiv/DOI 링크는 필수**입니다:

```markdown
> **Note**: This is a review of **"<논문 정식 제목>"** (<학회/저널> <연도>, [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)).
>
> For a **Korean version** of this review, please visit the **[OUTTA AI Tech Blog](https://blog.outta.ai/<id>)**.
{: .prompt-info }
```

> arXiv 논문은 자동으로 DOI(`https://doi.org/10.48550/arXiv.<id>`)도 부여됩니다([arXiv 공식](https://info.arxiv.org/help/doi.html)). 학회/저널 정식판 DOI가 있으면 함께 적습니다.
>
> **신규 글은 arXiv/DOI 링크 필수.** 기존 4편(DreamBooth/UNet++/KAD/Data Contamination)은 OUTTA 링크만 있었으나, 같은 형식으로 arXiv 링크를 추가해 맞췄습니다(migration 완료).

섹션 사이의 큰 전환에는 본문에 `---`(수평선)을 넣어 시각적으로 끊어줍니다(예: prompt-info 다음, Conclusion 앞).

## front matter 예시

공통 스키마는 [03 문서](../guide/03-writing-posts.md#front-matter-스키마)를 따르되, 리뷰 글에서만 쓰는 필드가 있습니다:

```yaml
---
title: "[Paper Review] UNet++: Redesigning Skip Connections to Exploit Multiscale Features in Image Segmentation"
date: 2025-01-08 00:00:00 +0900
categories: [Paper Review, Medical AI]
tags: [Segmentation, U-Net, Deep Learning, Architecture]
description: "A review of UNet++ (IEEE TMI 2020), a powerful evolution of the U-Net architecture for medical image segmentation."
image:
  path: assets/img/posts/paper-reviews/unetpp-arch.png
  alt: UNet++ Architecture
math: true
---
```

| 필드 | 리뷰 글에서의 관례 |
| --- | --- |
| `title` | `"[Paper Review] <논문 제목>"` 형식. 대괄호 때문에 따옴표 필수 |
| `categories` | `[Paper Review, <분야>]`. 분야는 `Generative AI` / `Medical AI` / `NLP` 등 |
| `canonical_url` | **기본은 생략**(self-canonical). OUTTA를 진짜 1차로 두고 *영어 글 색인을 포기할 때만* OUTTA URL을 넣습니다. OUTTA 출처 표시는 prompt-info로 충분 — **아래 SEO 주의** |
| `image.path` | `assets/img/posts/paper-reviews/<slug>.png` (맨 앞 `/` 없음) |
| `math: true` | 수식이 하나라도 있으면 추가(LR `$10^{-5}$`, loss `$L^1$` 등). 본문은 영어 |
| `mermaid: true` | 다이어그램을 직접 그릴 때만. 리뷰는 보통 논문 그림 이미지를 쓰므로 생략 가능 (위 UNet++ 예시는 논문 그림만 쓰므로 `mermaid: true`를 일부러 넣지 않았습니다) |

> 본문 인라인 이미지는 front matter와 반대로 맨 앞에 `/`를 붙입니다: `![alt](/assets/img/posts/paper-reviews/...png)`. 자세한 배경은 [03 문서의 이미지 경로 규칙](../guide/03-writing-posts.md#이미지-경로-규칙) 참고.

> **논문 그림(figure) 사용 규칙:** 논문 figure를 가져올 때는 캡션에 **출처를 명시**합니다 — `_Figure 1: ... (from the paper / adapted from Fig. 2 of the paper)._`. `alt` 텍스트를 채우고, 재현·각색 시 **라이선스(또는 fair-use 범위)**를 확인하세요. 가능하면 핵심만 발췌하거나 직접 다시 그립니다(redraw). NeurIPS 체크리스트도 assets/license를 점검 항목으로 둡니다.
{: .prompt-tip }

> **`canonical_url` SEO 주의:** 영어 글은 한국어 OUTTA 원문의 *번역*이라 일반적 "중복 콘텐츠"가 아닙니다. 교차도메인 canonical을 **다른 언어** 원문으로 지정하면, 구글이 영어 글을 원문의 사본으로 간주해 **색인에서 누락**시킬 수 있습니다([Google: 교차포스트엔 rel=canonical 비권장](https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting)). 영어 글 자체를 검색에 노출하고 싶다면 **self-referencing canonical**(자기 URL)이 더 안전하고(John Mueller "great practice"), OUTTA 출처는 위 prompt-info 안내로 충분합니다. OUTTA를 진짜 1차 버전으로 두고 영어 글 색인을 포기할 때만 교차도메인 canonical이 의미가 있습니다.
{: .prompt-warning }

## 표 작성 규칙 (가장 중요)

리뷰 글의 신뢰도는 **수치 표의 정확성**에서 갈립니다. 다음을 반드시 지킵니다.

1. **원논문 표에서 그대로 옮긴다.** 기억·요약·반올림으로 새로 만들지 않습니다. 어느 표에서 가져왔는지 캡션에 명시합니다.
   - 예: `_Table 1: ... (numbers from the DLMIA 2018 paper, Table 3)._`
   - 예: `_Table 1: ... (numbers from the paper; see Tables 2 and 3)._`
2. **게시 전 arXiv/DOI 원문과 1:1 대조한다.** PDF 표를 옆에 띄우고 셀 단위로 비교합니다. canonical OUTTA 글이 아니라 **원논문**이 기준입니다.
3. **열을 복사-붙여넣기하다 같은 값이 중복되지 않았는지 확인한다.** 표의 한 열을 복제해 다음 열을 채울 때, 값을 갈아끼우는 걸 빠뜨리면 두 열이 통째로 같아지는 사고가 납니다.
4. **데이터셋/지표 라벨도 원문과 일치시킨다.** 행 라벨(데이터셋·병변 이름)과 열 헤더(지표명: `DINO`, `CLIP-I`, `AUC`, `IoU`, `F1`, `ROUGE-1` 등)를 원문 표기 그대로 씁니다. `Acc (%)`처럼 단위까지 맞춥니다.
5. **불확실성도 함께 옮긴다.** 점추정값뿐 아니라 원문이 제시한 **표준편차·error bar·신뢰구간·시행 횟수**(`0.696 ± 0.01`, `mean ± std`)까지 옮깁니다. 점수만 적으면 reviewer가 "불완전"으로 봅니다([NeurIPS 재현성 체크리스트](https://neurips.cc/public/guides/PaperChecklist) — error bar/통계 유의성 항목).
6. **어느 행이 핵심 주장/SOTA인지 표시한다.** 본문이 강조하는 결과 행(주 비교·SOTA)을 굵게/캡션으로 짚어, 독자가 무엇이 논문의 main claim인지 알게 합니다.

> **실제로 있었던 중복 오류 (교훈):** 몇몇 리뷰 표(그 중 **DreamBooth**의 DINO/CLIP-I 열, **KAD**의 AUC 열)에서 열을 복붙하다 값을 갈아끼우는 걸 빠뜨려, 인접한 두 열이 통째로 같은 값으로 들어간 적이 있습니다. 표를 옮긴 직후 **모든 열을 원문 PDF와 1:1로 대조**하고, 인접 열이 우연히 통째로 일치하지 않는지 눈으로 한 번 더 확인하세요.
{: .prompt-warning }

검증용 체크 (표를 옮긴 직후):

```text
[ ] 모든 셀이 원논문 표의 같은 위치 값과 일치하는가
[ ] 인접한 두 열이 우연히 통째로 동일하지 않은가 (복붙 누락 의심)
[ ] 데이터셋/병변 행 라벨이 원문과 동일한가
[ ] 지표 열 헤더(이름+단위)가 원문과 동일한가 (AUC/IoU/F1/Acc(%) 등)
[ ] 캡션에 출처 표(Table N) 또는 데이터셋이 명시돼 있는가
[ ] best 수치 강조(**굵게**) 위치가 실제 최댓값과 맞는가
```

## 복붙용 최소 템플릿

새 리뷰 글의 골격입니다. front matter는 영어, 본문도 영어로 채웁니다.

```markdown
---
title: "[Paper Review] <Full Paper Title>"
date: YYYY-MM-DD 00:00:00 +0900
categories: [Paper Review, <Field>]
tags: [<Tag1>, <Tag2>, <Tag3>]
description: "A review of <Paper> (<Venue> <Year>), <one-line summary>."
image:
  path: assets/img/posts/paper-reviews/<slug>.png
  alt: <Alt text>
math: true   # remove if the review has no equations
---

> **Note**: This is a review of **"<Full Paper Title>"** (<Venue> <Year>, [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX)).
>
> For a **Korean version** of this review, see the **[OUTTA AI Tech Blog](https://blog.outta.ai/<id>)**.
{: .prompt-info }

## Why I Read This Paper
<Why this paper matters to you; what was impressive. First person.>

---

## Introduction
<Problem definition and background.>

![<Alt>](/assets/img/posts/paper-reviews/<slug>-overview.png)
_Figure 1: <caption> (from the paper)._

## Context / Related Work
<How this paper differs from / builds on prior work — its positioning (Keshav "Context"). Strongly recommended; fold into Introduction only for very short reviews.>

---

## Method
### 1. <Core idea>
<Explanation.>

## Results
<Lead-in to the table.>

| <Dataset/Class> | <Baseline> (<Metric>) | <Proposed> (<Metric>) |
| :--- | :---: | :---: |
| <Row 1> | <val> | **<val>** |
| <Row 2> | <val> | **<val>** |

_Table 1: <caption> (numbers from the paper, Table N)._

---

## Conclusion & Insight
<A 2-3 sentence summary of the paper. A review is commentary, not just a summary.>

### Strengths
<What the paper does well.>

### Limitations
<Weaknesses, untested assumptions, missing comparisons, scope limits.>

### Open Questions / Future Work
<What you would want to see next; your own take.>
```

## 게시 전 검증 체크리스트

1. **언어**: 본문이 영어인가(`_posts`는 영어 정책). 한국어가 남아 있지 않은가.
2. **헤더**: 모든 본문 헤더가 `## `(H2) 이상인가. 단일 `#` 없음.
3. **prompt-info**: `Why I Read This Paper` 위에 안내 블록이 있는가 — **논문 arXiv/DOI 링크 + OUTTA 링크** 모두, `{: .prompt-info }` 닫힘 표기 포함.
4. **비평/한계**: `Conclusion & Insight`에 강점뿐 아니라 **명시적 한계·비평**이 있는가(요약만으로 끝나지 않음).
5. **front matter**: `categories: [Paper Review, <분야>]`, `image.path`(앞 `/` 없음), 수식 있으면 `math: true`. `canonical_url`은 **기본 생략**(self-canonical) — OUTTA를 1차로 둘 때만(SEO 주의).
6. **표 (최우선)**: 위 [표 검증 체크](#표-작성-규칙-가장-중요)를 모두 통과했는가 — **인접 열 중복**, **불확실성(±std/CI) 포함**, **SOTA 행 표시**.
7. **재현성 링크**: 논문에 **공식 코드/데이터셋/프로젝트 페이지**가 있으면 본문이나 prompt-info에 링크했는가([NeurIPS 체크리스트](https://neurips.cc/public/guides/PaperChecklist)의 code/data 항목).
8. **이미지/그림**: 인라인 이미지가 `/assets/...`로 시작하고 파일이 `assets/img/posts/paper-reviews/`에 실제로 존재하는가. **논문 figure는 캡션에 출처(가능하면 `from Fig. N of the paper`)를 명시**했는가.
9. **수식**: `$...$` / `$$...$$`가 깨지지 않고 렌더링되는가(`math: true` 필요).
10. **로컬 미리보기**: `bash tools/run.sh`로 표·이미지·수식 렌더링 확인.
11. **링크 검사**: (선택) `bash tools/test.sh`로 arXiv/이미지/내부 링크(있으면 `canonical_url`)를 점검 후 커밋.
