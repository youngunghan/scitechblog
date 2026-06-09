# Blog Post Review - Round 3 (2026-06-09)

업데이트된 `_posts` 42개를 다시 검토했다. 원문은 수정하지 않았고, 이번 파일은 재검토 리포트다.

## 결론

이전 round2에서 지적한 치명적/중요 이슈는 대부분 해결되었다. 현재 상태는 게시해도 큰 사실 오류가 눈에 띄지는 않지만, 몇몇 글은 표현을 더 조심스럽게 다듬으면 신뢰도가 올라간다.

특히 좋아진 점:

- 모든 글에 `description`이 들어갔다.
- 코드 펜스 불균형은 발견되지 않았다.
- 렌더링되는 로컬 이미지 asset 누락은 발견되지 않았다.
- Tauri 글에 공식 `npm create tauri-app@latest` 경로와 `npx tauri init` 수동 경로가 추가되었다.
- Jekyll 이미지 경로 글이 `relative_url`의 공식 역할과 fork-specific workaround를 분리했다.
- FastAPI CI/CD 글이 zero-downtime 주장을 철회하고 short-downtime 배포로 고쳤다.
- Let’s Encrypt rate limit 글이 “도메인 변경만 가능”에서 staging/wait/우회책 구분으로 좋아졌다.
- Protein ESM2 글이 pathogenic/benign 태스크와 GOF/LOF 태스크를 분리했다.
- Skull mask 글에 OpenCV Otsu dtype, normalization guard, validation limit caveat가 들어갔다.
- Mermaid/PDF 글이 한글 우회보다 HTML entity escaping을 먼저 권장하게 바뀌었다.

## 실행한 검사

- `_posts` 파일 수: 42개.
- Markdown 코드 펜스 검사: 이상 없음.
- front matter `description`: 누락 없음.
- 렌더링되는 로컬 이미지 asset 존재 검사: 누락 없음.
- Jekyll 빌드: 실행하지 못함. 현재 환경에 `ruby`, `bundle`, `jekyll` 명령이 없다.

## 남은 수정 권장 사항

### 1. Skull mask 글: 제목/도입부의 일반화만 조금 더 낮추기

파일: `_posts/2025-12-29-skull-mask-generation-mri.md`

본문 하단에 검증 한계 문단이 들어가서 훨씬 좋아졌다. 다만 제목과 도입부는 아직 “5 labeled images - no deep learning required”, “IoU 0.98”이 강하게 보인다.

추천:

- “not enough to train anything” -> “not enough to train a robust model from scratch”
- title 또는 description에 “internal 5-slice experiment”를 더 선명히 넣기
- “Current Accuracy | IoU 0.98” -> “Internal 5-slice IoU 0.98”
- “Simple can be powerful” 문장은 좋지만, 의료 영상에서는 “simple can be a strong baseline” 정도가 더 안전하다.

공식 근거: OpenCV는 Otsu가 `CV_8UC1`/`CV_16UC1`에서 구현된다고 설명한다. 지금 본문은 이 기준에 맞게 많이 고쳐졌다.

### 2. Matplotlib 글: `plt.ylim()` 순서 표현 완화

파일: `_posts/2024-11-14-matplotlib-yaxis-stability.md`

imports, `sorted(glob...)`, regex guard, `pd.to_numeric(..., errors="coerce")`는 좋아졌다. 다만 “Set y-axis limits before plotting”, “Use `plt.ylim()` before creating plots”는 살짝 강하다.

추천:

- “before plotting”이 아니라 “consistently set a fixed y-axis range, e.g. before or after plotting”으로 변경.
- 더 일반적인 Matplotlib 스타일로는 `fig, ax = plt.subplots()` 후 `ax.set_ylim(0, 100)`을 보여주면 객체지향 API 기준으로 더 깔끔하다.

### 3. DreamBooth 글: “starting point of this entire trend”는 조금 과함

파일: `_posts/2024-05-29-review-dreambooth.md`

LoRA와의 관계는 이전보다 좋아졌지만, 결론의 “DreamBooth was at the starting point of this entire trend”는 텍스트-이미지 개인화 전체 흐름을 너무 넓게 대표하는 표현이다.

추천:

- “one of the landmark papers that accelerated subject-driven personalization” 정도로 조정.
- LoRA는 DreamBooth에서 나온 기법이 아니라, DreamBooth식 fine-tuning을 더 가볍게 만들 때 자주 결합되는 PEFT 방법이라고 유지하면 정확하다.

### 4. KAD 글: expert radiologist 비교는 더 좋아졌지만 headline에도 metric 조건 추가

파일: `_posts/2024-12-28-review-knowledge-enhanced-vlm.md`

본문에는 CheXpert benchmark와 five competition pathologies 조건이 들어갔다. 그래도 21행의 “reached the level of expert radiologists”가 눈에 띄는 문장이라, 같은 문장에 “by F1/MCC on the five CheXpert competition pathologies”까지 넣으면 더 안전하다.

추천:

- “zero-shot performance reached the level of expert radiologists on the CheXpert benchmark” -> “matched/exceeded the average of three radiologists by F1/MCC on the five CheXpert competition pathologies”

### 5. CI/CD 글: 운영 품질 보강 가능

파일: `_posts/2025-11-25-cicd-pipeline-fastapi.md`

zero downtime/Alembic/Compose v2 표현은 잘 수정되었다. 남은 건 “운영용 best practice” 수준이다.

추천:

- `latest` 태그만 쓰는 배포는 rollback이 어렵다. commit SHA 태그를 같이 push하는 예를 추가하면 좋다.
- `docker image prune -af`는 rollback 후보 이미지를 지울 수 있으니 주의 문구를 넣기.
- `docker compose down`은 DB 컨테이너까지 내릴 수 있다. app만 재생성하려면 `docker compose up -d --pull always app` 같은 방향을 설명할 수 있다.

### 6. HTTPS 글: 본문 Architecture Overview에 이미지가 빠진 듯함

파일: `_posts/2025-12-02-secure-https-cicd-fastapi.md`

front matter에는 `architecture_overview.png`가 있지만, `## Architecture Overview` 아래에는 빈 줄만 있고 본문 이미지가 없다. 의도라면 괜찮지만, 독자 입장에서는 다이어그램이 하나 빠진 느낌이다.

추천:

```markdown
![Architecture Overview](/assets/img/posts/fastapi-https/architecture_overview.png)
```

또 `docker-compose up -d`라는 표현은 파일명 `docker-compose.yaml`과 명령 `docker compose up -d`를 구분해서 쓰면 Docker Compose v2 기준과 더 잘 맞는다.

### 7. Markdown PDF/Mermaid 글: “always fail”은 exporter-dependent로 좁히기

파일:

- `_posts/2025-12-24-vscode-markdown-pdf-tips.md`
- `_posts/2025-12-24-troubleshooting-mermaid-diagram-syntax.md`

escaping 우선으로 바뀐 것은 좋다. 다만 `<meta>`, `<div>`가 “always fail”이라고 되어 있는데, 이는 VS Code Markdown PDF/Puppeteer/HTML 렌더링 조합에서의 경험으로 좁히는 편이 더 안전하다.

추천:

- “will always fail” -> “consistently failed in my Markdown PDF export pipeline”

### 8. Chirpy/Jekyll 관련 글: 공식 방식과 fork workaround 분리는 좋음

파일:

- `_posts/2025-11-30-troubleshooting-image-paths.md`
- `_posts/2025-11-26-blog-migration-wenivlog-to-chirpy.md`
- `_posts/2025-11-26-polishing-jekyll-chirpy.md`
- `_posts/2025-11-26-troubleshooting-visitor-counter.md`

Jekyll `relative_url` 설명은 이제 공식 문서와 맞다. Chirpy는 기술 블로그용으로 널리 쓰이는 테마라 방향도 좋다. 남은 개선은 문체 쪽이다.

추천:

- “CI/CD passes with 0 errors” 같은 결과 문장에는 가능하면 “at the time of this fix”를 붙이기.
- visitor counter는 외부 스크립트 의존이므로 privacy/availability caveat를 한 문단 넣기.
- badge 간격은 `&nbsp;`보다 CSS flex/gap 예시가 더 일반적이다.

## 글별 판정

| File | 현재 판정 | 메모 |
|---|---|---|
| `2024-02-04-algo-boj-1920-수-찾기.md` | 양호 | 알고리즘 글 구조 무난. |
| `2024-04-16-algo-boj-17436-소수의-배수.md` | 양호 | 포함-배제 설명 무난. |
| `2024-05-29-review-dreambooth.md` | 소폭 수정 | 결론의 trend/foundation 표현만 완화. |
| `2024-10-09-algo-boj-11401-이항-계수-3.md` | 양호 | 수식/구조 무난. |
| `2024-10-10-algo-boj-23832-서로소-그래프.md` | 양호 | 이전 샘플 오류 해결. |
| `2024-10-18-algo-boj-10422-괄호.md` | 양호 | Catalan DP 설명 자연스러움. |
| `2024-10-18-algo-boj-20443-배드민턴-대회.md` | 양호 | 예시/구조 무난. |
| `2024-11-12-tauri-m1-mac-setup.md` | 개선됨 | 공식 scaffolder와 수동 init 흐름 반영. |
| `2024-11-14-matplotlib-yaxis-stability.md` | 소폭 수정 | y-axis 설정 순서 표현만 완화. |
| `2024-11-15-python-import-issues.md` | 양호 | editable install/`python -m` caveat 잘 반영. |
| `2024-12-28-review-knowledge-enhanced-vlm.md` | 소폭 수정 | radiologist 비교에 metric 조건을 더 선명히. |
| `2025-01-08-review-unet-plus-plus.md` | 양호 | 연도 표기도 좋아짐. |
| `2025-08-23-review-data-contamination.md` | 양호 | GT/SST-2 예외 설명 개선됨. |
| `2025-09-12-algo-leetcode-0003-longest-substring-without-repeating-characters.md` | 양호 | 구조 무난. |
| `2025-09-12-algo-leetcode-0104-maximum-depth-of-binary-tree.md` | 양호 | local run용 `Optional`/TreeNode 보강됨. |
| `2025-09-12-algo-leetcode-0125-valid-palindrome.md` | 양호 | trace/설명 무난. |
| `2025-09-12-algo-leetcode-0217-contains-duplicate.md` | 양호 | `List` import 반영. |
| `2025-09-12-algo-leetcode-0680-valid-palindrome-ii.md` | 양호 | two-pointer 설명 무난. |
| `2025-09-12-algo-leetcode-0704-binary-search.md` | 양호 | `List` import 반영. |
| `2025-09-13-algo-leetcode-0009-palindrome-number.md` | 양호 | 숫자 palindrome 설명 무난. |
| `2025-09-17-algo-boj-1018-체스판-다시-칠하기.md` | 양호 | brute force 구조 무난. |
| `2025-09-26-algo-leetcode-0678-valid-parenthesis-string.md` | 양호 | greedy range 설명 무난. |
| `2025-10-16-algo-boj-11866-요세푸스-문제-0.md` | 양호 | queue 풀이 자연스러움. |
| `2025-10-16-algo-boj-9012-괄호.md` | 양호 | stack/count 설명 무난. |
| `2025-11-25-cicd-pipeline-fastapi.md` | 개선됨 | 운영 best practice만 추가 가능. |
| `2025-11-26-blog-migration-wenivlog-to-chirpy.md` | 양호 | 긴 글이지만 migration log 구조는 자연스러움. |
| `2025-11-26-polishing-jekyll-chirpy.md` | 소폭 수정 | badge spacing은 CSS/flex 예시 추천. |
| `2025-11-26-troubleshooting-visitor-counter.md` | 소폭 수정 | 외부 script/privacy caveat 추가 추천. |
| `2025-11-27-algo-leetcode-0001-two-sum.md` | 양호 | `List` import 반영. |
| `2025-11-29-algo-leetcode-0241-different-ways-to-add-parentheses.md` | 양호 | output-sensitive complexity 보강됨. |
| `2025-11-30-protein-variant-classification-esm2.md` | 개선됨 | 태스크 분리, import, DDP backend caveat 반영. |
| `2025-11-30-troubleshooting-image-paths.md` | 개선됨 | `relative_url` 공식 동작 설명이 정확해짐. |
| `2025-12-01-troubleshooting-latex-rendering.md` | 양호 | troubleshooting 구조 무난. |
| `2025-12-02-secure-https-cicd-fastapi.md` | 소폭 수정 | architecture image 본문 삽입 검토. |
| `2025-12-24-pytest-fixture-patterns.md` | 양호 | fixture scope/`os` import/성능 caveat 반영. |
| `2025-12-24-test-scenario-documentation-best-practices.md` | 양호 | 문서화 글 구조 자연스러움. |
| `2025-12-24-troubleshooting-mermaid-diagram-syntax.md` | 개선됨 | escaping 우선으로 수정됨. |
| `2025-12-24-uml-communication-vs-sequence-diagram.md` | 양호 | 비교 구조 무난. |
| `2025-12-24-vscode-markdown-pdf-tips.md` | 소폭 수정 | “always fail” 표현만 exporter-specific으로. |
| `2025-12-29-skull-mask-generation-mri.md` | 수정 권장 | 내부 5-slice 결과임을 제목/도입부에서도 강조. |
| `2026-01-07-plantuml-layout-optimization.md` | 양호 | “for this star-topology diagram”으로 한정되어 좋아짐. |
| `2026-02-18-algo-practice-grid-danger-zone-detection.md` | 양호 | 풀이 글 구조 무난. |

## 문체/구조 총평

- 알고리즘 글은 문제 -> 실패한 접근 -> 핵심 아이디어 -> 풀이 -> 복잡도 흐름이라 일반적인 기술 블로그 구조에 잘 맞는다.
- Troubleshooting 글은 Problem/Symptom/Root Cause/Solution 구조가 반복되어 읽기 쉽다.
- Paper Review 글은 이제 수치와 조건을 많이 보강했지만, 의료/연구 성능 주장은 headline 문장에서도 dataset/metric/scope를 함께 붙이는 습관을 추천한다.
- DevOps 글은 “내가 겪은 해결책”과 “일반 권장 방식”을 분리하기 시작해서 좋아졌다. 운영 글에서는 rollback, idempotency, secret rotation, healthcheck를 짧게라도 언급하면 더 프로답게 보인다.

## 참고 문서/저장소

- Tauri Create Project: https://v2.tauri.app/start/create-project/
- Docker Compose `version` top-level element: https://docs.docker.com/reference/compose-file/version-and-name/
- Docker Compose CLI: https://docs.docker.com/reference/cli/docker/compose/
- Alembic asyncio cookbook: https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
- Jekyll Liquid `relative_url`: https://jekyllrb.com/docs/liquid/filters/
- Chirpy theme GitHub: https://github.com/cotes2020/jekyll-theme-chirpy
- Let's Encrypt Rate Limits: https://letsencrypt.org/docs/rate-limits/
- pytest fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
- OpenCV threshold/Otsu: https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html
- PyTorch DistributedDataParallel: https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html
- Mermaid flowchart syntax: https://mermaid.js.org/syntax/flowchart.html
- Hugging Face ESM docs: https://huggingface.co/docs/transformers/model_doc/esm
- Meta ESM GitHub: https://github.com/facebookresearch/esm
- DreamBooth paper: https://arxiv.org/abs/2208.12242
- KAD paper: https://www.nature.com/articles/s41467-023-40260-7
- UNet++ paper: https://arxiv.org/abs/1912.05074
