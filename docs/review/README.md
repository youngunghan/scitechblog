# Review Notes

블로그 글 검토 리포트 정리 폴더입니다. `_posts` 원문은 여기서 관리하지 않고, Codex가 작성한 검토 기록만 보관합니다.

## 현재 구조

```text
docs/review/
├── README.md
├── POST_REVIEW_2026-06-09-latest.md
└── archive/
    ├── POST_REVIEW_2026-06-09-round2.md
    ├── POST_REVIEW_2026-06-09-round3.md
    └── POST_REVIEW_2026-06-09-round4.md
```

## 파일별 역할

| File | 상태 | 설명 |
|---|---|---|
| `POST_REVIEW_2026-06-09-latest.md` | 유지 권장 | 가장 최신 검토본입니다. 현재 `_posts` 상태를 기준으로 남은 권장 사항만 정리되어 있습니다. |
| `archive/POST_REVIEW_2026-06-09-round2.md` | 삭제 후보 | 초반 검토본입니다. 이후 수정으로 해결된 내용이 많아 현재 기준으로는 오래된 지적이 많이 포함되어 있습니다. |
| `archive/POST_REVIEW_2026-06-09-round3.md` | 삭제 후보 | 중간 검토본입니다. round4/round5에 같은 내용이 더 최신 상태로 정리되어 있습니다. |
| `archive/POST_REVIEW_2026-06-09-round4.md` | 선택 보관 | round5 직전 상태를 비교하고 싶을 때만 유용합니다. 최종 요약만 필요하면 삭제해도 됩니다. |

## 정리 추천

최소 보관 구성을 원하면 아래 두 파일만 남기면 됩니다.

```text
docs/review/
├── README.md
└── POST_REVIEW_2026-06-09-latest.md
```

삭제 추천 파일:

- `docs/review/archive/POST_REVIEW_2026-06-09-round2.md`
- `docs/review/archive/POST_REVIEW_2026-06-09-round3.md`

조건부 삭제 파일:

- `docs/review/archive/POST_REVIEW_2026-06-09-round4.md`

round4는 “이전 상태와 최신 상태 비교”가 필요하면 남기고, 최종 결론만 필요하면 삭제해도 됩니다.

## 삭제 전 확인

현재 `latest` 파일은 round5 내용을 담고 있으므로, round2~4를 삭제해도 최신 검토 결론은 유지됩니다. 다만 “어떤 지적이 언제 해결되었는지”의 과정 기록은 사라집니다.
