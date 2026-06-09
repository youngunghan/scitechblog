# Blog Post Review - Round 2 (2026-06-09)

업데이트된 `_posts` 42개를 다시 검토했다. 원문 파일은 수정하지 않았고, 공식 문서와 대표 저장소 기준으로 사실성, 실행 가능성, 문체/구조를 확인했다.

## 요약

- 좋아진 점: BOJ 23832 예시 출력, KAD/CheXNet 비교표, 데이터 오염 리뷰의 예외 처리, HTTPS 글의 제목 계층/오타, Tauri `devUrl`, PlantUML 중복 결론은 이전보다 좋아졌다.
- 자동 검사: 코드 펜스 균형, 렌더링되는 로컬 이미지/링크, Mermaid/math front matter는 큰 문제 없음.
- 계속 남은 핵심 문제: Tauri 글은 `src-tauri` 생성 단계가 빠져 그대로 따라 하면 실행이 막힌다. Jekyll 이미지 경로 글은 `relative_url` 설명이 공식 동작과 맞지 않는다. FastAPI CI/CD 글은 `docker-compose down/up`을 쓰면서 zero downtime이라고 말한다. HTTPS 글은 Let's Encrypt rate limit 대응을 “도메인 변경만 가능”으로 너무 단정한다.
- 연구/AI 글에서 가장 조심할 부분: Skull mask 글은 5장 내부 검증 결과를 일반화하는 표현이 강하고, Protein ESM2 글은 pathogenic/benign 평가와 GOF/LOF 분류 태스크가 한 글 안에서 섞인다.
- 메타데이터: `description`이 없는 글이 10개 남아 있다. Chirpy/Jekyll 카드, 검색, SEO 품질을 위해 채우는 편이 좋다.

## 자동 검사 결과

### 좋음

- `_posts` 총 42개.
- 코드 블록 펜스 불균형은 발견하지 못했다.
- 렌더링되는 로컬 이미지/링크는 현재 파일 시스템 기준으로 깨진 항목을 발견하지 못했다.
- Mermaid 또는 수식이 들어간 글의 `mermaid: true`, `math: true` 누락은 발견하지 못했다.

### 수정 권장

`description`이 없는 글:

- `2024-11-12-tauri-m1-mac-setup.md`
- `2024-11-14-matplotlib-yaxis-stability.md`
- `2024-11-15-python-import-issues.md`
- `2025-11-25-cicd-pipeline-fastapi.md`
- `2025-11-26-blog-migration-wenivlog-to-chirpy.md`
- `2025-11-26-polishing-jekyll-chirpy.md`
- `2025-11-26-troubleshooting-visitor-counter.md`
- `2025-11-30-protein-variant-classification-esm2.md`
- `2025-12-02-secure-https-cicd-fastapi.md`
- `2026-01-07-plantuml-layout-optimization.md`

로컬 재현용 코드에서 import가 부족한 글:

- `matplotlib-yaxis-stability`: `os`, `glob`, `re`, `pandas as pd`, `numpy as np`, `matplotlib.pyplot as plt`
- LeetCode 104/217/704/1: `Optional`, `List` 등 typing import. LeetCode 환경에서는 제공되지만 로컬 실행 글이면 명시하는 편이 낫다.
- `protein-variant-classification-esm2`: `torch`, `torch.nn as nn`, `EsmModel`
- `pytest-fixture-patterns`: `os`
- `skull-mask-generation-mri`: `numpy as np`, `cv2`, `scipy.ndimage`

## 높은 우선순위

### 1. Tauri 글: 프로젝트 생성 흐름이 아직 불완전함

파일: `_posts/2024-11-12-tauri-m1-mac-setup.md`

- 현재 흐름은 `npm init -y` -> `@tauri-apps/cli` 설치 -> Vite 생성 -> 갑자기 `src-tauri/` 구조를 전제로 한다.
- 공식 Tauri v2 문서는 새 프로젝트라면 `npm create tauri-app@latest`, 수동 구성이라면 Vite 생성 후 `npx tauri init`으로 `src-tauri`를 만들라고 안내한다.
- 따라서 “Complete Guide”라면 `npx tauri init` 또는 `npm create tauri-app@latest`가 반드시 들어가야 한다.
- `rustup target add aarch64-apple-darwin`은 Apple Silicon Mac에서 기본 로컬 빌드만 할 때 필수라기보다 명시 타깃/크로스 빌드용에 가깝다. “M1 Mac에서 항상 필요”처럼 읽히지 않게 조정하는 것이 좋다.
- 추천 구조: “빠른 공식 방식(create-tauri-app)”을 먼저 제시하고, “기존 Vite 앱에 붙이는 수동 방식”을 별도 섹션으로 분리.

참고: Tauri 공식 Create Project 문서.

### 2. Jekyll 이미지 경로 글: `relative_url` 설명이 공식 동작과 충돌

파일: `_posts/2025-11-30-troubleshooting-image-paths.md`

- 글에서는 `_layouts/home.html`에서 `relative_url` 없이 `/assets/...`로 만들면 테마 내부 로직이 `/scitechblog`를 자동으로 붙인다고 설명한다.
- 그러나 Jekyll 공식 문서에서 `relative_url`은 입력 경로 앞에 `baseurl`을 붙이는 필터다. 즉 GitHub Pages subpath 배포에서는 보통 `{{ path | relative_url }}`이 정석이다.
- 현재 로컬 `_layouts/home.html`도 `<img src="{{ src }}">` 형태라면, “테마 내부가 자동으로 prepend한다”는 설명은 확인 근거가 약하다.
- 추천 수정: “내 fork의 특정 레이아웃/플러그인 조합에서는 이렇게 해결했다”로 좁히고, 일반 Jekyll 원칙은 `relative_url` 사용이라고 분리해서 설명.

참고: Jekyll Liquid Filters 공식 문서.

### 3. FastAPI CI/CD 글: zero downtime 주장이 현재 배포 스크립트와 맞지 않음

파일: `_posts/2025-11-25-cicd-pipeline-fastapi.md`

- 배포 스크립트가 `docker-compose down` 후 `docker-compose up -d`를 실행한다.
- 이 방식은 컨테이너를 내렸다가 올리므로 일반적으로 downtime이 생긴다. 그런데 결과 섹션에는 “Zero downtime deployments via Docker container orchestration”이라고 되어 있다.
- 수정 추천: “simple automated deployment” 또는 “short downtime deployment”로 낮추거나, 진짜 zero downtime을 원하면 blue-green, reverse proxy upstream switching, rolling update, healthcheck 기반 전환으로 별도 설계를 소개.
- Docker Compose v2에서는 `version` top-level property가 obsolete라 글에서 v2 기준 명령도 `docker compose`로 통일하는 편이 좋다. 현재 일부 예시는 `docker-compose`가 남아 있다.
- Alembic 설명도 “Alembic은 항상 sync driver가 필요”보다 “현재 sync 방식의 `env.py`에서는 sync URL이 필요했고, Alembic은 async cookbook도 제공한다”가 정확하다.

참고: Docker Compose 파일 `version` 공식 문서, Alembic asyncio cookbook.

### 4. HTTPS/Certbot 글: Let's Encrypt rate limit 대응이 너무 단정적

파일: `_posts/2025-12-02-secure-https-cicd-fastapi.md`

- “기다릴 수 없어서 도메인을 바꾸는 것이 유일한 해결책”이라고 쓰였지만, 공식 문서는 staging 환경 사용, 재발급/재시도 억제, rate limit refill 대기, 기존 계정/설정 보존 등을 안내한다.
- 도메인 변경은 가능한 우회책 중 하나지만, 권장 일반 해법처럼 보이면 독자가 불필요하게 도메인을 바꿀 수 있다.
- 추천 표현: “내 상황에서는 과제 일정 때문에 새 DuckDNS 도메인으로 우회했다. 일반적으로는 staging으로 검증하고, 실패 루프를 멈춘 뒤 limit 회복을 기다리는 것이 정석이다.”

참고: Let's Encrypt Rate Limits 공식 문서.

### 5. Protein ESM2 글: 태스크 정의가 섞임

파일: `_posts/2025-11-30-protein-variant-classification-esm2.md`

- 도입부는 pathogenic/benign 예측을 말하다가, 같은 문장에서 GOF/LOF 분류 모델로 넘어간다.
- Challenge 1은 pathogenicity predictor 평가이고, Challenge 3은 LOF/GOF 9:1 불균형이다. 독자가 하나의 label space로 오해할 수 있다.
- 추천 구조: “Task A: pathogenic variant prioritization metric selection”과 “Task B: GOF/LOF classifier training”을 분리.
- ESM2 코드에는 import가 빠져 있고, CLS pooling만 제시한다. Hugging Face ESM류에서는 CLS 토큰 접근이 가능하지만, 단백질 sequence representation에서는 non-special token mean pooling도 흔한 선택지라 비교 근거를 한 문장 넣으면 좋다.
- 4x A100 DDP 문맥에서는 PyTorch 공식 권장처럼 GPU 학습에는 `nccl`을 기본으로 두고, `gloo`는 CPU/로컬 smoke test용이라고 분명히 쓰는 편이 좋다.

참고: PyTorch DDP 공식 문서, Meta ESM GitHub 저장소, Hugging Face ESM2 모델 카드.

### 6. Skull mask 글: 5장 내부 튜닝 결과를 일반화하는 표현이 강함

파일: `_posts/2025-12-29-skull-mask-generation-mri.md`

- description과 본문에서 “5 labeled images로 IoU 0.98”을 매우 강하게 제시한다. 실제로는 5 slices에서 dilation 26px를 튜닝한 내부 결과로 읽힌다.
- `Otsu consistently found threshold = 23`, `perfectly captures`, `Deep Learning: 500-1,000+ images minimum`, `10,000+ labeled images` 같은 표현은 과도하게 일반화되어 있다.
- OpenCV 전체가 0-255 `uint8`만 기대한다고 쓰였지만, 공식 문서상 Otsu는 `CV_8UC1`/`CV_16UC1`에서 구현되어 있고 threshold 자체는 여러 dtype을 받는다. “이번 Otsu 파이프라인에서는 8-bit grayscale로 정규화했다”가 정확하다.
- `normalize_image`는 `img_max == img_min`일 때 division by zero가 난다. 예제 코드라도 guard를 넣는 편이 좋다.
- IoU 설명은 “ground truth와 97.94% overlap”보다 “intersection이 union의 97.94%”가 정확하다.
- 의료 영상 글이므로 외부 검증, 3D volume 단위 split, scanner/protocol 차이, slice leakage 가능성을 한 문단 넣으면 신뢰도가 크게 올라간다.

참고: OpenCV threshold/Otsu 공식 문서.

### 7. Mermaid/PDF 글: “한글을 넣으면 해결”보다 escaping을 정석으로

파일:

- `_posts/2025-12-24-troubleshooting-mermaid-diagram-syntax.md`
- `_posts/2025-12-24-vscode-markdown-pdf-tips.md`

이전보다 `AND`/`OR`을 공식 reserved keyword로 단정하지 않는 점은 좋아졌다. 다만 `<row>`, `<meta>`류 문제는 한글/숫자를 끼워 넣는 우회보다 `&lt;row&gt;`처럼 HTML entity escaping, 따옴표, 또는 angle bracket 제거를 먼저 권장하는 편이 더 일반적이다.

참고: Mermaid flowchart 공식 문서.

## 중간 우선순위

- `2025-12-24-pytest-fixture-patterns.md`: fixture scope 표에서 session fixture를 “pytest 시작 시 생성”으로 쓰면 미묘하게 틀리다. 공식 문서 기준 fixture는 처음 요청될 때 생성되고 scope에 따라 파괴된다. 성능 예시 `600s -> 15s`는 측정값이면 조건을 적고, 아니면 illustrative라고 표시.
- `2024-11-15-python-import-issues.md`: “run from anywhere”라고 한 뒤 `python src/vision_utils/train.py`를 추천하면 현재 작업 디렉터리에 의존한다. editable install 후 `python -m vision_utils.train` 또는 console script entry point를 추천하는 편이 더 일반적이다.
- `2024-11-14-matplotlib-yaxis-stability.md`: `glob` 순서가 비결정적이고, regex `.group(1)` 실패 가능성이 있다. `sorted(glob.glob(...))`, `pd.to_numeric(..., errors="coerce")`, `dropna/fillna`, match guard를 넣으면 튜토리얼 품질이 좋아진다.
- `2024-05-29-review-dreambooth.md`: 수치 표는 좋아졌지만 “DreamBooth가 LoRA의 foundation”처럼 읽히는 문장은 부정확하다. LoRA 자체는 DreamBooth보다 먼저 나온 PEFT 기법이고, DreamBooth는 텍스트-이미지 개인화 흐름에 큰 영향을 준 논문이라고 쓰는 편이 정확하다.
- `2024-12-28-review-knowledge-enhanced-vlm.md`: KAD 표는 개선되었다. 다만 “expert radiologist 수준”은 특정 unseen pathology/benchmark 조건으로 한정해서 쓰는 편이 안전하다.
- `2025-01-08-review-unet-plus-plus.md`: 큰 오류는 없어 보인다. 출판 연도는 “IEEE TMI 2020, online 2019”처럼 쓰면 가장 깔끔하다.
- `2025-11-29-algo-leetcode-0241-different-ways-to-add-parentheses.md`: 시간복잡도는 출력 개수 자체가 Catalan 계열로 커지는 output-sensitive 문제라고 설명하면 더 정확하다.
- `2026-01-07-plantuml-layout-optimization.md`: `skinparam maxMessageSize` 방향은 공식 문서와 맞다. 다만 “0% line crossing”은 특정 다이어그램에서의 결과로 한정하는 것이 좋다.

## 글별 빠른 판정

| File | 판정 | 권장 사항 |
|---|---|---|
| `2024-02-04-algo-boj-1920-수-찾기.md` | 양호 | 구조/해설 일반적. |
| `2024-04-16-algo-boj-17436-소수의-배수.md` | 양호 | 포함-배제 설명 흐름 좋음. |
| `2024-05-29-review-dreambooth.md` | 수정 권장 | LoRA와의 관계 표현만 정확히 조정. |
| `2024-10-09-algo-boj-11401-이항-계수-3.md` | 양호 | 페르마 소정리/모듈러 역원 구조 무난. |
| `2024-10-10-algo-boj-23832-서로소-그래프.md` | 개선됨 | 샘플 출력/직접 연결쌍 설명 수정 확인. |
| `2024-10-18-algo-boj-10422-괄호.md` | 양호 | Catalan DP 설명 일반적. |
| `2024-10-18-algo-boj-20443-배드민턴-대회.md` | 대체로 양호 | 예시 산출은 맞아 보이나 문제 정의 문장 보강 가능. |
| `2024-11-12-tauri-m1-mac-setup.md` | 중요 수정 | `create-tauri-app` 또는 `tauri init` 단계 추가 필요. |
| `2024-11-14-matplotlib-yaxis-stability.md` | 수정 권장 | import, 파일 정렬, regex/NaN 방어 추가. |
| `2024-11-15-python-import-issues.md` | 수정 권장 | `python -m`/editable install 중심으로 권장안 정리. |
| `2024-12-28-review-knowledge-enhanced-vlm.md` | 대체로 양호 | radiologist 비교는 benchmark 조건으로 한정. |
| `2025-01-08-review-unet-plus-plus.md` | 양호 | 연도 표기만 TMI 2020/online 2019로 보완 가능. |
| `2025-08-23-review-data-contamination.md` | 개선됨 | GT/SST-2 예외 처리 좋아짐. |
| `2025-09-12-algo-leetcode-0003-longest-substring-without-repeating-characters.md` | 양호 | 슬라이딩 윈도우 설명 무난. |
| `2025-09-12-algo-leetcode-0104-maximum-depth-of-binary-tree.md` | 소폭 수정 | 로컬 실행용 `Optional`/TreeNode 주석 추가. |
| `2025-09-12-algo-leetcode-0125-valid-palindrome.md` | 개선됨 | 이전 trace 문제는 해소된 것으로 보임. |
| `2025-09-12-algo-leetcode-0217-contains-duplicate.md` | 소폭 수정 | `from typing import List` 추가. |
| `2025-09-12-algo-leetcode-0680-valid-palindrome-ii.md` | 양호 | 투포인터 구조 일반적. |
| `2025-09-12-algo-leetcode-0704-binary-search.md` | 소폭 수정 | `List` import 추가. |
| `2025-09-13-algo-leetcode-0009-palindrome-number.md` | 양호 | 숫자 뒤집기 설명 무난. |
| `2025-09-17-algo-boj-1018-체스판-다시-칠하기.md` | 양호 | brute force 기준 설명 일반적. |
| `2025-09-26-algo-leetcode-0678-valid-parenthesis-string.md` | 양호 | greedy range 설명 무난. |
| `2025-10-16-algo-boj-11866-요세푸스-문제-0.md` | 양호 | queue 풀이 자연스러움. |
| `2025-10-16-algo-boj-9012-괄호.md` | 양호 | stack/count 풀이 구조 무난. |
| `2025-11-25-cicd-pipeline-fastapi.md` | 중요 수정 | zero downtime, Alembic async, Compose v2 표현 수정. |
| `2025-11-26-blog-migration-wenivlog-to-chirpy.md` | 소폭 수정 | “4 posts migrated”가 당시 기준이면 명시. description 추가. |
| `2025-11-26-polishing-jekyll-chirpy.md` | 소폭 수정 | badge 간격은 `&nbsp;`보다 CSS/flex 또는 Shields 예시 추천. |
| `2025-11-26-troubleshooting-visitor-counter.md` | 소폭 수정 | 외부 script의 privacy/availability caveat 추가. |
| `2025-11-27-algo-leetcode-0001-two-sum.md` | 소폭 수정 | `List` import 추가. |
| `2025-11-29-algo-leetcode-0241-different-ways-to-add-parentheses.md` | 소폭 수정 | complexity를 output-sensitive로 설명. |
| `2025-11-30-protein-variant-classification-esm2.md` | 중요 수정 | pathogenic/benign과 GOF/LOF 태스크 분리. |
| `2025-11-30-troubleshooting-image-paths.md` | 중요 수정 | Jekyll `relative_url` 공식 동작과 fork-specific workaround 분리. |
| `2025-12-01-troubleshooting-latex-rendering.md` | 양호 | MathJax/Jekyll troubleshooting 구조 무난. |
| `2025-12-02-secure-https-cicd-fastapi.md` | 수정 권장 | rate limit 대응 단정 완화, renewal automation 보강. |
| `2025-12-24-pytest-fixture-patterns.md` | 수정 권장 | fixture 생성 시점, `os` import, 성능 예시 caveat. |
| `2025-12-24-test-scenario-documentation-best-practices.md` | 양호 | 구조/문체 일반적. |
| `2025-12-24-troubleshooting-mermaid-diagram-syntax.md` | 수정 권장 | HTML entity escaping을 1차 해법으로. |
| `2025-12-24-uml-communication-vs-sequence-diagram.md` | 양호 | 비교 구조 자연스러움. |
| `2025-12-24-vscode-markdown-pdf-tips.md` | 수정 권장 | “90%” 같은 비측정 수치 완화, escaping 우선. |
| `2025-12-29-skull-mask-generation-mri.md` | 중요 수정 | 의료/영상 일반화 표현과 검증 범위 caveat 필요. |
| `2026-01-07-plantuml-layout-optimization.md` | 소폭 수정 | description 추가, “0% crossing” 한정 표현. |
| `2026-02-18-algo-practice-grid-danger-zone-detection.md` | 양호 | 문제 풀이 글로 구조 무난. |

## 문체/구조 추천

- 튜토리얼 글은 “문제 상황 -> 공식/권장 방법 -> 내가 겪은 예외 -> 최종 코드 -> 검증 결과” 순서가 가장 읽기 쉽다.
- 경험담은 좋지만 “only solution”, “perfectly”, “always”, “minimum” 같은 절대 표현은 공식 문서나 대규모 실험 근거가 있을 때만 쓰는 편이 안전하다.
- 연구 리뷰는 수치/표가 들어가면 논문 조건을 함께 적어야 한다. 예: dataset, split, metric, comparison target.
- 알고리즘 글은 현재 구조가 전반적으로 일반적이다. 다만 LeetCode 코드는 로컬 실행 가능성을 위해 typing import를 붙이면 블로그 품질이 오른다.
- Jekyll/CI/CD 글은 독자가 그대로 따라 할 가능성이 높으므로 “내 환경에서의 workaround”와 “일반 권장 방식”을 분리하는 것이 중요하다.

## 참고한 주요 문서/저장소

- Tauri Create Project: https://v2.tauri.app/start/create-project/
- Docker Compose `version` top-level element: https://docs.docker.com/reference/compose-file/version-and-name/
- Alembic asyncio cookbook: https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
- Jekyll Liquid `relative_url`: https://jekyllrb.com/docs/liquid/filters/
- Let's Encrypt Rate Limits: https://letsencrypt.org/docs/rate-limits/
- pytest fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
- OpenCV threshold/Otsu: https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html
- PyTorch DistributedDataParallel: https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html
- Mermaid flowchart syntax: https://mermaid.js.org/syntax/flowchart.html
- Meta ESM GitHub: https://github.com/facebookresearch/esm
- Hugging Face ESM2 model: https://huggingface.co/facebook/esm2_t33_650M_UR50D
- DreamBooth paper: https://arxiv.org/abs/2208.12242
- KAD paper: https://www.nature.com/articles/s41467-023-40260-7
- UNet++ paper: https://arxiv.org/abs/1912.05074
- Data contamination review target: https://arxiv.org/abs/2401.06059
