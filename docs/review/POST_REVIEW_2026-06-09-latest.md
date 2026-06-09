# Blog Post Review - Round 5 (2026-06-09)

업데이트된 `_posts` 42개를 다시 검토했다. 원문은 수정하지 않았고, 이 파일은 재검토 리포트다.

## 결론

현재 글들은 전반적으로 게시 가능한 상태다. 이전 라운드에서 지적했던 치명적 오류나 공식 문서와 충돌하는 설명은 대부분 정리되었다. 남은 항목은 사실 오류라기보다 운영 hardening, 의료/AI 글의 표현 완화, 예제 코드의 production-safe 버전 제시 정도다.

## 이번에 확인한 개선 사항

- `2025-11-25-cicd-pipeline-fastapi.md`: `latest`, `docker compose down`, `docker image prune -af` 예제가 학습용/first-automation 예시라는 경고가 바로 아래 추가됨.
- `2025-12-02-secure-https-cicd-fastapi.md`: architecture image가 본문에 들어갔고, `nginx:1.25`가 `nginx:stable-alpine`으로 바뀌었으며 Nginx tag 업데이트 전략이 추가됨.
- `2025-11-26-troubleshooting-visitor-counter.md`: “perfectly” 표현이 “cleanly”로 완화됨.
- `2025-11-26-polishing-jekyll-chirpy.md`: `&nbsp;` quick fix와 flex/gap 권장 코드가 분리됨.
- `2025-12-24-vscode-markdown-pdf-tips.md`, `2025-12-24-troubleshooting-mermaid-diagram-syntax.md`: HTML tag 관련 실패를 exporter-specific 경험으로 좁히고 escaping을 우선 권장함.
- `2025-12-29-skull-mask-generation-mri.md`: “not enough to train anything”이 “not enough to train a robust model from scratch”로 완화됨.

## 실행한 검사

- `_posts` 파일 수: 42개.
- front matter 필수 필드 검사: `title`, `date`, `categories`, `tags`, `description` 누락 없음.
- Markdown 코드 펜스 검사: 이상 없음.
- 렌더링되는 로컬 이미지/링크 존재 검사: 이상 없음.
- Jekyll 빌드: 실행하지 못함. 현재 환경에서 `ruby`, `bundle`, `jekyll` 명령이 발견되지 않는다.

## 남은 권장 사항

### 1. Skull mask 글: 제목/description을 “baseline” 쪽으로 더 좁히기

파일: `_posts/2025-12-29-skull-mask-generation-mri.md`

본문 caveat는 충분히 좋아졌지만 제목과 description은 검색 카드에서 먼저 보이므로 여전히 강하게 읽힐 수 있다.

추천:

- `Building a Skull Mask Generator for MRI Images Without Deep Learning`
- `... reaching IoU 0.98 on an internal set of 5 labeled images—no deep learning required`

위 표현을 아래처럼 바꾸면 의료 영상 글로 더 안전하다.

- `A Classical Baseline for Skull-Mask Generation on a 5-Slice MRI Set`
- `... reaching IoU 0.98 in a small internal 5-slice experiment`

또 `The classical approach turned out to be extremely fast`에는 CPU model, process count, image shape 같은 측정 환경을 붙이면 좋다.

### 2. FastAPI CI/CD 글: production-safe snippet을 별도로 제시하면 더 좋음

파일: `_posts/2025-11-25-cicd-pipeline-fastapi.md`

현재 경고와 Operational Notes가 있어서 오해 위험은 많이 줄었다. 다음 단계로는 “학습용 snippet”과 “운영에 가까운 snippet”을 분리하면 더 좋다.

추천:

- Docker image를 `latest`와 `${GITHUB_SHA}`로 함께 tag/push.
- 배포 시 SHA tag를 pull.
- `docker compose down` 대신 app service만 재생성.
- `docker image prune -af`는 제거하거나 보존 정책을 명시.

### 3. HTTPS 글: `stable-alpine`도 moving tag임을 한 문장 추가

파일: `_posts/2025-12-02-secure-https-cicd-fastapi.md`

`nginx:stable-alpine`은 `nginx:1.25`보다 낫지만, 여전히 움직이는 tag다. 운영 환경에서는 특정 stable version 또는 digest pin과 정기 업데이트 정책을 같이 쓰는 것이 더 정확하다.

추천 문장:

> `stable-alpine` is convenient for tutorials, but production deployments should pin a specific supported version or digest and update it on a regular security cadence.

앱 이미지도 `wapang:latest`로 되어 있으므로, FastAPI CI/CD 글의 immutable SHA tag 원칙과 연결해도 좋다.

### 4. Protein ESM2 글: “proved crucial”을 실험 범위로 한정

파일: `_posts/2025-11-30-protein-variant-classification-esm2.md`

태스크 분리와 DDP backend 설명은 좋아졌다. 다만 `Difference Vector proved crucial`은 ablation 결과가 명시되지 않으면 조금 강하다.

추천:

- “proved crucial” -> “was helpful in my experiments” 또는 “was the key design choice in my experiments”
- 실제 ablation이 있다면 baseline vs difference-vector F1/AUROC 표를 추가.

### 5. KAD 글: XAI/clinical trust 표현 완화

파일: `_posts/2024-12-28-review-knowledge-enhanced-vlm.md`

radiologist 비교는 metric/scope가 잘 들어갔다. 다만 결론의 “will greatly help increase trust in clinical settings”는 의료 AI 문맥에서는 조금 강하다.

추천:

- “may help clinicians inspect model behavior”
- “clinical trust still requires prospective validation, calibration, and workflow evaluation”

### 6. Mermaid 글: `AND/OR` workaround는 현재도 괜찮고, label 단순화 예시를 추가하면 더 튼튼함

파일:

- `_posts/2025-12-24-troubleshooting-mermaid-diagram-syntax.md`
- `_posts/2025-12-24-vscode-markdown-pdf-tips.md`

현재는 empirical workaround라고 잘 한정했다. 추가로 portable한 예시를 넣으면 더 좋다.

- `q=[cond1, _AND_, cond2]`
- `q: cond1 + cond2`
- `q: all conditions`

## 글별 판정

| File | 판정 | 메모 |
|---|---|---|
| `2024-02-04-algo-boj-1920-수-찾기.md` | 양호 | 알고리즘 풀이 구조 자연스러움. |
| `2024-04-16-algo-boj-17436-소수의-배수.md` | 양호 | 포함-배제 설명 무난. |
| `2024-05-29-review-dreambooth.md` | 양호 | LoRA/개인화 흐름 표현 개선됨. |
| `2024-10-09-algo-boj-11401-이항-계수-3.md` | 양호 | 수식과 복잡도 설명 무난. |
| `2024-10-10-algo-boj-23832-서로소-그래프.md` | 양호 | 샘플과 phi 설명 정상. |
| `2024-10-18-algo-boj-10422-괄호.md` | 양호 | Catalan DP 설명 자연스러움. |
| `2024-10-18-algo-boj-20443-배드민턴-대회.md` | 양호 | 풀이 구조 무난. |
| `2024-11-12-tauri-m1-mac-setup.md` | 양호 | Tauri 공식 생성 흐름 반영됨. |
| `2024-11-14-matplotlib-yaxis-stability.md` | 양호 | import, 정렬, dtype, OO API note 보강됨. |
| `2024-11-15-python-import-issues.md` | 양호 | src layout와 editable install 설명 정확함. |
| `2024-12-28-review-knowledge-enhanced-vlm.md` | 소폭 수정 | XAI/clinical trust 표현만 완화 추천. |
| `2025-01-08-review-unet-plus-plus.md` | 양호 | 논문 리뷰 구조 무난. |
| `2025-08-23-review-data-contamination.md` | 양호 | 결론 균형 좋음. |
| `2025-09-12-algo-leetcode-0003-longest-substring-without-repeating-characters.md` | 양호 | sliding window 설명 무난. |
| `2025-09-12-algo-leetcode-0104-maximum-depth-of-binary-tree.md` | 양호 | 로컬 실행용 type/TreeNode 보강됨. |
| `2025-09-12-algo-leetcode-0125-valid-palindrome.md` | 양호 | trace와 two-pointer 설명 정상. |
| `2025-09-12-algo-leetcode-0217-contains-duplicate.md` | 양호 | import 보강됨. |
| `2025-09-12-algo-leetcode-0680-valid-palindrome-ii.md` | 양호 | 구조 무난. |
| `2025-09-12-algo-leetcode-0704-binary-search.md` | 양호 | import 보강됨. |
| `2025-09-13-algo-leetcode-0009-palindrome-number.md` | 양호 | 숫자 palindrome 설명 무난. |
| `2025-09-17-algo-boj-1018-체스판-다시-칠하기.md` | 양호 | brute force 풀이 무난. |
| `2025-09-26-algo-leetcode-0678-valid-parenthesis-string.md` | 양호 | greedy range 설명 무난. |
| `2025-10-16-algo-boj-11866-요세푸스-문제-0.md` | 양호 | queue 풀이 자연스러움. |
| `2025-10-16-algo-boj-9012-괄호.md` | 양호 | stack/count 기준 설명 무난. |
| `2025-11-25-cicd-pipeline-fastapi.md` | 대체로 양호 | production-safe snippet 추가 시 더 좋음. |
| `2025-11-26-blog-migration-wenivlog-to-chirpy.md` | 양호 | migration log 구조 자연스러움. |
| `2025-11-26-polishing-jekyll-chirpy.md` | 양호 | flex/gap 권장 코드 반영됨. |
| `2025-11-26-troubleshooting-visitor-counter.md` | 양호 | privacy/availability caveat와 표현 완화 반영됨. |
| `2025-11-27-algo-leetcode-0001-two-sum.md` | 양호 | import 보강됨. |
| `2025-11-29-algo-leetcode-0241-different-ways-to-add-parentheses.md` | 양호 | output-sensitive complexity 설명 개선됨. |
| `2025-11-30-protein-variant-classification-esm2.md` | 소폭 수정 | “proved crucial” 표현 또는 ablation 근거 보강 추천. |
| `2025-11-30-troubleshooting-image-paths.md` | 양호 | Jekyll 공식 원칙과 fork workaround 분리됨. |
| `2025-12-01-troubleshooting-latex-rendering.md` | 양호 | troubleshooting 구조 무난. |
| `2025-12-02-secure-https-cicd-fastapi.md` | 대체로 양호 | `stable-alpine` moving tag caveat 추가 추천. |
| `2025-12-24-pytest-fixture-patterns.md` | 양호 | fixture scope/성능 caveat 반영됨. |
| `2025-12-24-test-scenario-documentation-best-practices.md` | 양호 | 문서화 글 구조 자연스러움. |
| `2025-12-24-troubleshooting-mermaid-diagram-syntax.md` | 양호 | escaping 우선, empirical caveat 반영됨. |
| `2025-12-24-uml-communication-vs-sequence-diagram.md` | 양호 | 비교 구조 무난. |
| `2025-12-24-vscode-markdown-pdf-tips.md` | 양호 | exporter-specific 표현으로 개선됨. |
| `2025-12-29-skull-mask-generation-mri.md` | 대체로 양호 | 제목/description에서 small internal baseline임을 더 강조 추천. |
| `2026-01-07-plantuml-layout-optimization.md` | 양호 | diagram scope 한정 표현 좋음. |
| `2026-02-18-algo-practice-grid-danger-zone-detection.md` | 양호 | 풀이 글 구조 무난. |

## 문체/구조 총평

- Algorithm 글은 문제 -> 실패 접근 -> 핵심 아이디어 -> 풀이 -> 복잡도 흐름이 일관적이다.
- Troubleshooting 글은 Symptom/Root Cause/Solution 구조가 반복되어 일반적인 테크블로그 문체에 잘 맞는다.
- Paper Review 글은 수치와 조건이 보강되어 과장 위험이 줄었다. 의료 AI 관련 문장은 계속 dataset/metric/scope를 함께 쓰는 방향이 좋다.
- DevOps 글은 경험담과 공식 권장 방식을 분리하기 시작해서 신뢰도가 높아졌다. production snippet을 별도로 제시하면 더 완성도가 올라간다.

## 참고한 주요 문서/저장소

- Tauri Create Project: https://v2.tauri.app/start/create-project/
- Docker Compose `version` top-level element: https://docs.docker.com/reference/compose-file/version-and-name/
- Docker Compose CLI: https://docs.docker.com/reference/cli/docker/compose/
- Docker Hub Nginx Official Image: https://hub.docker.com/_/nginx
- Alembic asyncio cookbook: https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic
- Jekyll Liquid `relative_url`: https://jekyllrb.com/docs/liquid/filters/
- Chirpy theme GitHub: https://github.com/cotes2020/jekyll-theme-chirpy
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
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
