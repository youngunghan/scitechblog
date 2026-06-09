# 블로그 글 작성 가이드

scitechblog에 올리는 블로그 글을 **유형별로 어떤 구조/스타일로 쓰고, 게시 전 무엇을 검증하는지** 정리한 저자용 가이드 모음입니다. 파일명·front matter 같은 기계적 규칙은 [../guide/03-writing-posts.md](../guide/03-writing-posts.md)에서 이미 다루므로 여기서는 **글 내용의 구조와 문체, 그리고 사실 검증**에 집중합니다.

> 이 폴더(`docs/blog_post/`)는 `docs/`와 마찬가지로 [_config.yml](../../_config.yml)의 `exclude`에 묶여 Jekyll 사이트로 빌드되지 않는 **레포 내부 문서**입니다. 여기 적힌 내용은 블로그 페이지로 게시되지 않습니다.

## 언어 정책

> **블로그 글(`_posts/*.md`)의 본문은 전부 영어로 씁니다. 저자용 문서(`docs/guide`, `docs/blog_post`)만 한국어로 씁니다.**
>
> - 글 제목·본문·표·캡션·코드 주석 → 영어 (예: `[Paper Review] UNet++: Redesigning Skip Connections...`)
> - 이 가이드 같은 `docs/` 문서 → 한국어
> - 예외: 알고리즘 글의 한글 슬러그 파일명은 허용됩니다(백준 글 다수). 파일명은 URL일 뿐 본문은 영어입니다.
{: .prompt-warning }

## 목차

글 유형별 가이드입니다(모두 같은 폴더에 있습니다).

1. [논문 리뷰](paper-review.md) — `[Paper Review]` 글. 읽은 동기 → 방법 → 결과 표 → 인사이트 구조와 수치 대조
2. [알고리즘 풀이](algorithm.md) — LeetCode/BOJ 글. 문제 → 접근 → 풀이 코드 → 복잡도 구조와 손 추적 검증
3. [트러블슈팅](troubleshooting.md) — `[Troubleshooting]` 글. 증상 → 원인 분석 → 해결 → 결론 구조
4. [프로젝트·엔지니어링](project-engineering.md) — 프로젝트 회고/구축기. Challenge별 서술과 아키텍처 다이어그램

## 공통 하우스 스타일

유형과 무관하게 모든 글에 적용됩니다. 자세한 front matter 필드 설명은 [../guide/03-writing-posts.md](../guide/03-writing-posts.md#front-matter-스키마)를 참조하세요.

| 항목 | 규칙 | 예시 |
| --- | --- | --- |
| 본문 언어 | 영어 | `## Why I Read This Paper` |
| 본문 헤더 | **`## `(H2)부터** 시작. 단일 `#`(H1)는 절대 쓰지 않음(제목은 front matter `title`이 담당) | `## Methods` → `### 1. Deep Supervision` |
| 수식 | 수식이 있으면 front matter에 `math: true`. 인라인 `$...$`, 블록 `$$...$$` | `$O(N \log N)$` |
| 다이어그램 | 다이어그램이 있으면 `mermaid: true` + ```` ```mermaid ```` 코드블록 | sliding-window 흐름도 |
| front matter 대표 이미지 | `image.path`는 **맨 앞 `/` 없이** | `assets/img/posts/algo/leetcode_new.png` |
| 본문 인라인 이미지 | **맨 앞 `/` 붙임** + 이탤릭 캡션 | `![alt](/assets/img/posts/protein-classifier/architecture.png)` |
| 이미지 폴더 | 주제별 하위 폴더 | `assets/img/posts/<주제>/` |
| Python 코드 | 저자 하우스 스타일 블록 종료 마커 유지 | `# end def`, `# end for`, `# end if`, `# end while` |
| 캡션 | 그림/표 바로 아래 이탤릭 한 줄 | `_Figure 1: The UNet++ architecture..._` |

> `# end def` 등의 마커는 의도된 하우스 스타일입니다. 코드 정리 도구나 린터가 "불필요한 주석"이라며 지우지 않도록 주의하세요. 실제 적용 예는 [algorithm.md](algorithm.md)와 [project-engineering.md](project-engineering.md)의 코드 블록을 보세요.

## 게시 전 검증 체크리스트

글을 올리기 전에 **사실 검증**을 통과시킵니다. 문체보다 수치/주장 검증이 우선입니다.

- [ ] **논문 표 수치 1:1 대조** — 리뷰 글의 모든 표 수치는 arXiv/원문 PDF의 해당 표와 한 칸씩 직접 대조합니다. 어느 표에서 가져왔는지 캡션에 명시합니다(예: UNet++ 글 Table 1 캡션의 `numbers from the DLMIA 2018 paper, Table 3`). 출처가 다른 두 표(DLMIA 2018 vs IEEE TMI 2020)를 섞지 않습니다.
- [ ] **알고리즘 손 추적 일치** — 본문의 샘플 입력(예: `s = "abca"`)을 **손으로 추적한 결과**와 코드의 실제 출력이 일치하는지 확인합니다. 가능하면 코드를 직접 실행해 출력을 맞춰봅니다. Mermaid 흐름도/Step-by-Step 설명과 코드 동작이 어긋나면 안 됩니다.
- [ ] **복잡도 표기 검증** — Time/Space Complexity가 실제 코드와 맞는지 재확인합니다(예: sliding window는 각 문자가 최대 2회 방문 → `$O(N)$`, set 공간 `$O(\min(N, \Sigma))$`). Big-O 안의 로그 밑/상수는 생략하되 표기는 일관되게.
- [ ] **초안/혼잣말 제거** — `wait`, `Oops`, `Correction:`, `Let me reconsider`, `Actually,` 같은 사고 흔적·자기수정 문구를 본문에서 전부 제거합니다. 최종 글은 결론만 깔끔히 남깁니다.
- [ ] **기술 주장 교차검증** — API/플래그/동작에 대한 주장은 공식 문서로 확인합니다(예: Chirpy `math: true` 트리거, PyTorch DDP `gloo` 백엔드, `torchrun --nproc_per_node`). 기억에 의존하지 말고 1차 출처를 확인합니다.
- [ ] **H1 없음 확인** — 본문에 단일 `#`(H1)이 없는지 확인합니다. 모든 섹션 헤더는 `## ` 이상이어야 합니다. 빠른 점검:

  ```bash
  # 본문(front matter 이후)에 H1이 있으면 출력됨 — 결과가 없어야 정상
  grep -nE '^# [^#]' _posts/<파일>.md
  ```

- [ ] **링크/이미지 경로** — front matter `image.path`는 `/` 없이, 본문 인라인 이미지는 `/`로 시작하는지 확인합니다. 마지막으로 `bash tools/run.sh` 로컬 미리보기와 `bash tools/test.sh` 링크 검사를 돌립니다.

## 참고 문서

| 무엇이 궁금할 때 | 문서 |
| --- | --- |
| 파일명·날짜 접두사·permalink 규칙 | [../guide/03-writing-posts.md](../guide/03-writing-posts.md#파일명-규칙) |
| front matter 필드 의미·카테고리/태그 체계 | [../guide/03-writing-posts.md](../guide/03-writing-posts.md#front-matter-스키마) |
| 이미지 경로·수식/다이어그램 켜기 | [../guide/03-writing-posts.md](../guide/03-writing-posts.md#이미지-경로-규칙) |
| `math: true` 일괄 주입 등 보조 스크립트 | [../guide/05-python-scripts.md](../guide/05-python-scripts.md#수식다이어그램-정리) |
| 썸네일 생성 스크립트 | [../guide/05-python-scripts.md](../guide/05-python-scripts.md#썸네일-생성) |
