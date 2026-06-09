# Blog Post Review - Round 4 (2026-06-09)

업데이트된 `_posts` 42개를 다시 검토했다. 원문 글은 수정하지 않았고, 이번 파일은 재검토 리포트다.

## 최종 요약

현재 상태는 이전보다 매우 좋아졌다. round2/round3에서 중요하게 지적했던 사실 오류, 과장 표현, 실행 불가능한 튜토리얼 흐름은 대부분 해결되었다. 지금 남은 것은 “게시 전 완성도를 더 끌어올리는” 수준의 소폭 수정 사항이다.

확인한 개선 사항:

- 모든 글에 `description`이 있다.
- Markdown 코드 펜스 불균형은 발견되지 않았다.
- 렌더링되는 로컬 이미지/링크 누락은 발견되지 않았다.
- Tauri 글은 공식 `create-tauri-app`와 수동 `npx tauri init` 경로를 모두 설명한다.
- Jekyll 이미지 경로 글은 `relative_url`의 공식 동작과 fork-specific workaround를 분리했다.
- FastAPI CI/CD 글은 zero-downtime 주장을 철회했고, rollback/`latest`/`docker image prune -af`/`docker compose down` caveat를 추가했다.
- HTTPS 글은 architecture image를 본문에 추가했고, Let’s Encrypt rate limit 대응을 staging/wait/workaround로 정확히 분리했다.
- Protein ESM2 글은 pathogenic/benign 평가와 GOF/LOF 분류를 별도 태스크로 분리했고, DDP backend caveat도 들어갔다.
- Skull mask 글은 “robust model from scratch”로 표현을 낮췄고, OpenCV Otsu dtype, normalization guard, validation limit caveat를 반영했다.
- DreamBooth, KAD, Mermaid/PDF, Matplotlib 글의 핵심 표현도 공식 문서/논문 기준에 맞게 많이 정리되었다.

## 실행한 검사

- `_posts` 파일 수: 42개.
- front matter 필수 필드 검사: `title`, `date`, `categories`, `tags`, `description` 누락 없음.
- Markdown 코드 펜스 검사: 이상 없음.
- 렌더링되는 로컬 이미지/링크 존재 검사: 이상 없음.
- Jekyll 빌드: 실행하지 못함. 현재 환경에서 `ruby`, `bundle`, `jekyll` 명령이 발견되지 않는다.

## 남은 수정 권장 사항

### 1. Skull mask 글: 제목/description만 한 번 더 좁히면 좋음

파일: `_posts/2025-12-29-skull-mask-generation-mri.md`

본문에는 이제 “5 slices 내부 검증” 한계가 충분히 들어갔다. 다만 제목과 description은 검색/카드에서 먼저 보이는 영역이라 여전히 조금 강하게 읽힐 수 있다.

추천:

- `Building a Skull Mask Generator for MRI Images Without Deep Learning`
- `A classical image processing approach ... reaching IoU 0.98 on an internal set of 5 labeled images`

위 표현을 아래처럼 더 명확히 좁히면 의료 영상 글로서 안전하다.

- `A Classical Baseline for Skull-Mask Generation on a 5-Slice MRI Set`
- `... reaching IoU 0.98 in a small internal 5-slice experiment`

또 `The classical approach turned out to be extremely fast`도 실제 측정 환경을 같이 쓰면 더 좋다. 예: CPU model, single process/8 processes, image shape.

### 2. FastAPI CI/CD 글: 첫 코드 snippet이 아직 위험한 예시로 먼저 노출됨

파일: `_posts/2025-11-25-cicd-pipeline-fastapi.md`

운영 caveat는 잘 들어갔다. 다만 독자는 위쪽 GitHub Actions snippet을 먼저 복사할 가능성이 높다. 그 snippet은 여전히 `latest`, `docker compose down`, `docker image prune -af`를 사용한다.

추천:

- snippet 바로 아래에 “이 코드는 학습용/첫 자동화용이며 production hardening은 아래 Operational Notes 참고” 같은 경고를 추가.
- 또는 snippet 자체를 commit SHA tag 기반으로 바꾸고, `docker compose down` 대신 app service만 재생성하는 형태를 보여주기.

공식/권장 기준: Docker Compose v2는 `docker compose` CLI와 Compose Specification 기준으로 보는 것이 맞고, Docker 공식 문서도 `version` top-level element를 obsolete로 안내한다.

### 3. HTTPS 글: Nginx 이미지 태그는 최신 유지 전략을 적어두면 좋음

파일: `_posts/2025-12-02-secure-https-cicd-fastapi.md`

`nginx:1.25`는 글 작성 당시에는 자연스러운 pin일 수 있지만, 2026년 기준으로는 오래된 태그다. Docker Hub의 Nginx 공식 이미지에는 현재 `stable-alpine`, `1.28.3-alpine` 계열 태그가 보인다.

추천:

- 학습용 예시는 `nginx:stable-alpine` 또는 특정 최신 stable pin 예시로 교체.
- 운영에서는 “무조건 latest”보다 “보안 업데이트를 주기적으로 따라가는 pinned stable tag”라는 원칙을 한 문장 추가.

### 4. Visitor counter 글: 결론의 “perfectly”만 약간 완화

파일: `_posts/2025-11-26-troubleshooting-visitor-counter.md`

privacy/availability caveat가 들어간 점은 좋다. 결론의 “integrates perfectly with the Chirpy theme's dark mode”는 문체상 약간 강하다.

추천:

- “integrates cleanly with the Chirpy theme's dark mode”
- 또는 “integrates well in my current Chirpy setup”

### 5. Polishing Chirpy 글: `&nbsp;`는 quick fix로 명확히 처리됨, 가능하면 최종 권장 코드는 flex로

파일: `_posts/2025-11-26-polishing-jekyll-chirpy.md`

현재 note에서 CSS/flexbox가 더 낫다고 잘 말한다. 그래도 본문 Solution의 주 코드가 `&nbsp;`라서 독자는 그걸 따라 할 수 있다.

추천:

```html
<div class="badge-row">
  <img src="..." alt="Python">
  <img src="..." alt="C">
</div>
```

```css
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}
```

### 6. Mermaid/PDF 글: 현재 구조는 좋음, 단 “AND/OR workaround”를 더 portable하게 만들 수 있음

파일:

- `_posts/2025-12-24-troubleshooting-mermaid-diagram-syntax.md`
- `_posts/2025-12-24-vscode-markdown-pdf-tips.md`

공식 문서 기준으로 `end`만 reserved라고 한 점, HTML entity escaping을 우선한 점은 좋다. `AND`/`OR`은 empirical workaround라고 분명히 했으므로 사실 오류는 아니다.

추가 추천:

- `_AND_` 외에도 edge label 전체를 더 단순한 문장으로 바꾸는 방법을 추천하면 좋다. 예: `q: cond1 + cond2`, `q: all conditions`.

## 글별 판정

| File | 판정 | 메모 |
|---|---|---|
| `2024-02-04-algo-boj-1920-수-찾기.md` | 양호 | 알고리즘 풀이 구조 일반적. |
| `2024-04-16-algo-boj-17436-소수의-배수.md` | 양호 | 포함-배제 설명 무난. |
| `2024-05-29-review-dreambooth.md` | 양호 | LoRA/개인화 흐름 표현 개선됨. |
| `2024-10-09-algo-boj-11401-이항-계수-3.md` | 양호 | 수식/복잡도 구조 무난. |
| `2024-10-10-algo-boj-23832-서로소-그래프.md` | 양호 | 샘플/phi 설명 정상. |
| `2024-10-18-algo-boj-10422-괄호.md` | 양호 | Catalan DP 설명 자연스러움. |
| `2024-10-18-algo-boj-20443-배드민턴-대회.md` | 양호 | 풀이 구조 무난. |
| `2024-11-12-tauri-m1-mac-setup.md` | 양호 | 공식 scaffolder/수동 init 흐름 반영됨. |
| `2024-11-14-matplotlib-yaxis-stability.md` | 양호 | import, 정렬, dtype, OO API note까지 보강됨. |
| `2024-11-15-python-import-issues.md` | 양호 | src layout, editable install caveat 정확함. |
| `2024-12-28-review-knowledge-enhanced-vlm.md` | 양호 | radiologist 비교가 metric/scope와 함께 표현됨. |
| `2025-01-08-review-unet-plus-plus.md` | 양호 | 논문 리뷰 구조 무난. |
| `2025-08-23-review-data-contamination.md` | 양호 | 예외와 결론 균형 개선됨. |
| `2025-09-12-algo-leetcode-0003-longest-substring-without-repeating-characters.md` | 양호 | sliding window 설명 무난. |
| `2025-09-12-algo-leetcode-0104-maximum-depth-of-binary-tree.md` | 양호 | 로컬 실행용 type/TreeNode 보강됨. |
| `2025-09-12-algo-leetcode-0125-valid-palindrome.md` | 양호 | two-pointer 설명 무난. |
| `2025-09-12-algo-leetcode-0217-contains-duplicate.md` | 양호 | import 보강됨. |
| `2025-09-12-algo-leetcode-0680-valid-palindrome-ii.md` | 양호 | 구조 무난. |
| `2025-09-12-algo-leetcode-0704-binary-search.md` | 양호 | import 보강됨. |
| `2025-09-13-algo-leetcode-0009-palindrome-number.md` | 양호 | 숫자 palindrome 설명 무난. |
| `2025-09-17-algo-boj-1018-체스판-다시-칠하기.md` | 양호 | brute force 설명 무난. |
| `2025-09-26-algo-leetcode-0678-valid-parenthesis-string.md` | 양호 | greedy range 설명 무난. |
| `2025-10-16-algo-boj-11866-요세푸스-문제-0.md` | 양호 | queue 풀이 자연스러움. |
| `2025-10-16-algo-boj-9012-괄호.md` | 양호 | stack/count 기준 설명 무난. |
| `2025-11-25-cicd-pipeline-fastapi.md` | 대체로 양호 | snippet 바로 아래 production caveat를 더 앞당기면 좋음. |
| `2025-11-26-blog-migration-wenivlog-to-chirpy.md` | 양호 | migration log 구조 자연스러움. |
| `2025-11-26-polishing-jekyll-chirpy.md` | 소폭 수정 | 최종 권장 코드는 flex/gap 예시가 더 좋음. |
| `2025-11-26-troubleshooting-visitor-counter.md` | 소폭 수정 | caveat 좋음. 결론의 “perfectly”만 완화 추천. |
| `2025-11-27-algo-leetcode-0001-two-sum.md` | 양호 | import 보강됨. |
| `2025-11-29-algo-leetcode-0241-different-ways-to-add-parentheses.md` | 양호 | output-sensitive complexity 설명 개선됨. |
| `2025-11-30-protein-variant-classification-esm2.md` | 양호 | 태스크 분리/ESM2/DDP caveat 반영됨. |
| `2025-11-30-troubleshooting-image-paths.md` | 양호 | Jekyll 공식 원칙과 fork workaround 분리됨. |
| `2025-12-01-troubleshooting-latex-rendering.md` | 양호 | troubleshooting 구조 무난. |
| `2025-12-02-secure-https-cicd-fastapi.md` | 대체로 양호 | Nginx 이미지 태그 최신 유지 전략 추가 추천. |
| `2025-12-24-pytest-fixture-patterns.md` | 양호 | fixture scope/성능 caveat 반영됨. |
| `2025-12-24-test-scenario-documentation-best-practices.md` | 양호 | 문서화 글 구조 자연스러움. |
| `2025-12-24-troubleshooting-mermaid-diagram-syntax.md` | 양호 | escaping 우선, empirical caveat 반영됨. |
| `2025-12-24-uml-communication-vs-sequence-diagram.md` | 양호 | 비교 구조 무난. |
| `2025-12-24-vscode-markdown-pdf-tips.md` | 양호 | exporter-specific 표현으로 개선됨. |
| `2025-12-29-skull-mask-generation-mri.md` | 대체로 양호 | 제목/description에서 내부 5-slice 실험임을 더 강조하면 좋음. |
| `2026-01-07-plantuml-layout-optimization.md` | 양호 | “for this star-topology diagram”으로 한정되어 좋음. |
| `2026-02-18-algo-practice-grid-danger-zone-detection.md` | 양호 | 풀이 글 구조 무난. |

## 문체/구조 총평

- Algorithm 글: 문제 -> 실패 접근 -> 핵심 아이디어 -> 풀이 -> 복잡도 흐름이 일관적이라 읽기 좋다.
- Troubleshooting 글: Symptom/Root Cause/Solution 구조가 반복되어 일반적인 테크블로그 문체에 잘 맞는다.
- Paper Review 글: 수치와 조건이 많이 보강되어 과장 위험이 줄었다. 의료/AI 성능 비교는 지금처럼 dataset/metric/scope를 같이 쓰는 방향을 유지하면 좋다.
- DevOps 글: 경험담과 공식 권장 방식을 분리하기 시작해서 신뢰도가 올랐다. 운영 글은 rollback, healthcheck, immutable tag, secret rotation을 짧게라도 언급하면 더 탄탄하다.

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
