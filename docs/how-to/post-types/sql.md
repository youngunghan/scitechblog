# SQL 패턴 글 작성 가이드

> **범위:** 공개 가능한 SQL 패턴 글의 구조·쿼리 설명·검증 절차. 공통 front matter는 [write-posts.md](../write-posts.md) 참고.
> **대상:** 블로그 작성자.
> **상태:** 구현 반영 — 기준일 2026-07-10.

글은 영어로 작성합니다. 문제 제공자가 외부 공개를 금지하면 문제명, 원문, 스키마, 데이터, 기대 결과와 제출 SQL을 게시하지 않습니다. 허가 범위가 불명확하면 일반적인 패턴과 자체 placeholder만 사용합니다.

## 1. 공개 가능성 확인

| 확인 항목 | 공개 가능 | 공개 금지·불명확 |
|---|---|---|
| 문제명·링크 | 제공자 정책이 허용할 때만 표기 | 플랫폼과 문제를 식별하지 않음 |
| 스키마·샘플 데이터 | 재배포 허가가 있을 때만 사용 | 자체 generic schema로 대체 |
| 제출 SQL | 풀이 공개가 허용될 때만 사용 | 동일 문제를 복원할 수 없는 일반 패턴만 설명 |
| 결과값·채점 화면 | 개인정보·약관 검토 후 사용 | 생략 |

공개 정책은 robots.txt나 로그인 가능 여부가 아니라 서비스 약관과 문제 페이지의 명시적 안내를 기준으로 판단합니다.

## 2. 섹션 구조

| 섹션 | 필수 | 목적 |
|---|---:|---|
| `## Scope` | ✅ | 일반화한 문제 유형과 공개하지 않는 범위 |
| `## Why the Pattern` | ✅ | 단순 접근의 한계와 선택한 SQL 패턴 |
| `## Generic Pattern` | ✅ | 자체 placeholder를 사용한 재사용 가능 SQL |
| `## Clause-by-Clause` | 권장 | 필터·집계·window 순서 설명 |
| `## Edge Cases` | ✅ | NULL, tie, empty group, 정렬과 numeric type |
| `## Key Takeaways` | 권장 | 특정 문제와 무관한 재사용 원칙 |

### 2.1 허용된 공개 문제

제공자가 풀이 공개를 허용하는 경우에만 `Problem`, `Data Model`, `Expected Result`, `Solution`을 추가합니다. 해당 허가 근거를 글의 `Resources`에 연결합니다.

### 2.2 제한된 문제

문제 고유 이름과 테이블·컬럼을 제거하고 `group_key`, `entity_key`, `metric_value`처럼 자체 placeholder를 씁니다. 원문을 역으로 복원할 수 있는 조건 조합이나 정답 쿼리는 남기지 않습니다.

## 3. 제목과 Front matter

제한된 문제에서 도출한 글은 플랫폼명이 아니라 패턴명을 사용합니다.

```yaml
---
title: "SQL Pattern: Tie-Aware Top Rows per Group"
date: YYYY-MM-DD 00:00:00 +0900
categories: [SQL, Patterns]
tags: [SQL, CTE, Window Function, RANK, Top per Group]
description: "A reusable SQL pattern for returning all top-ranked ties within each group."
image:
  path: assets/img/posts/algo/math.png
  alt: "Tie-aware top-per-group SQL pattern"
author: seoultech
mermaid: true
---
```

## 4. SQL 코드 스타일

- SQL 절은 대문자로 씁니다: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`.
- 선택 컬럼이 둘 이상이면 각 컬럼을 한 줄씩 씁니다.
- CTE와 중첩 표현식은 2-space indentation을 사용합니다.
- 행 단위 필터는 `WHERE`, 집계 결과 필터는 `HAVING`에 둡니다.
- window 결과는 CTE 또는 바깥 쿼리에서 필터링합니다.
- 출력 순서가 의미 있으면 최종 `ORDER BY`를 명시합니다.
- tie 정책은 `RANK`, `DENSE_RANK`, `ROW_NUMBER` 중 의도에 맞게 선택합니다.

## 5. 일반 패턴 예시

```sql
WITH per_entity AS (
  SELECT
    group_key,
    entity_key,
    SUM(metric_value) AS aggregate_value
  FROM measurements
  WHERE is_valid = TRUE
  GROUP BY
    group_key,
    entity_key
),
ranked AS (
  SELECT
    group_key,
    entity_key,
    aggregate_value,
    RANK() OVER (
      PARTITION BY group_key
      ORDER BY aggregate_value DESC
    ) AS group_rank
  FROM per_entity
)
SELECT
  group_key,
  entity_key,
  aggregate_value
FROM ranked
WHERE group_rank = 1
ORDER BY
  group_key,
  entity_key;
```

이 예시는 자체 relation·column 이름만 사용하며 특정 플랫폼 문제의 제출 답안을 나타내지 않습니다.

## 6. 게시 전 검증

1. 원문·스키마·샘플·정답의 공개 권한을 확인합니다.
2. generic 예제가 독립적인 fixture에서 실행되는지 확인합니다.
3. 출력 컬럼, row granularity와 tie 정책을 문장으로 명시합니다.
4. `WHERE`·`HAVING`·window 필터의 실행 순서를 확인합니다.
5. NULL, empty group, 동일 점수와 안정적 정렬을 테스트합니다.
6. 특정 문제의 고유 명칭이나 값을 검색해 남은 노출이 없는지 확인합니다.

## 관련 문서

- [공통 글 작성 규칙](../write-posts.md)
- [SQL Pattern: Tie-Aware Top Rows per Group](../../../_posts/2026-06-14-sql-tie-aware-top-rows-per-group.md)
