# L660 — DR3 (2027 Q2) Preregistration Document Plan

**Status**: PLAN ONLY (preregistration document 의 *구조* plan).
**Predecessor**: L657 Q1 ("임계값 동결 + preregistration 의무").
**Trigger**: DESI DR3 공개 *이전* OSF 등록 의무.
**Scope**: 본 문서는 plan. 실제 OSF DOI 등록 + 임계값 정량 lock-in 은 별도 8인 Rule-A 세션.

---

## [최우선-1] 준수 명시

본 plan 에는:
- 수식 0줄
- 임계값 정량값 0개 (모두 placeholder `?`)
- 파라미터 값 0개

임계값 / 결정 경계 / 수치는 *별도* 8인 Rule-A 합의 세션에서 lock-in.

---

## §1 Pre-registration metadata (구조)

| 항목 | 내용 (placeholder) |
|---|---|
| 등록일 | DR3 공개 *이전* (정확 일자 lock-in 시 기재) |
| OSF DOI | `osf.io/<placeholder>` (등록 후 채움) |
| GitHub release tag | `vL660-prereg-<date>` (placeholder) |
| author signatures | 8인 Rule-A 합의 후 명단 첨부 |
| 임계값 lock-in date | DR3 공개 *이전* (사후 변경 금지) |
| Hash commit | preregistration 시점 repo SHA |

**의무**: 등록 후 임계값 / decision tree 변경 0건. 변경 시 falsifiability 무효 선언.

---

## §2 SQT 6 falsifier list (L498 reference)

본 preregistration 은 6 falsifier 모두 등록. 단, **DR3 w_a 는 primary** (L657 결정).

1. **DESI DR3 w_a** — *primary* falsifier (2027 Q2 expected)
2. **Euclid DR1 cosmic-shear S_8** (timeline: TBD)
3. **CMB-S4 N_eff** (timeline: late 2030s)
4. **ET inspiral phase** (timeline: 2030s)
5. **SKA cosmic-string null** (timeline: TBD)
6. **LSST cluster-shear** (timeline: TBD)

각 falsifier 별 별도 §3 형식 임계값 표 첨부 (본 plan 에서는 primary 만 시연).

---

## §3 DR3 w_a 임계값 (primary falsifier)

**구조** (정량값은 8인 Rule-A 결정 후 채움):

| Outcome | Condition | Action |
|---|---|---|
| **PASS** | `w_a < ?` (placeholder) | paper §5/§7 update, framework 유지 |
| **Inconclusive** | `? < w_a < ?` | minimal update, 다음 falsifier 대기 |
| **KILL** | `w_a > ?` | paper retraction *or* framework 격하 |

**임계값 결정 input** (8인 Rule-A 가 검토할 자료):
- L575 fixed-θ Δlog Z penumbra
- L498 SQT 자체 예측 분포
- L633 H2 multi-session 가용 budget
- DR3 공식 σ(w_a) 예측

**lock-in 의무**: DR3 공개 *이전* 등록. 사후 임계값 조정 금지.

---

## §4 BCNF protocol (L583 reference)

DR3 결과 평가 단계별 의무:

- **B (Blind)**: 결과 미인지 상태에서 임계값 적용 코드 frozen.
- **C (Cross-validate)**: 다른 falsifier (Euclid S_8, CMB-S4 N_eff 등) 와 cross-check.
- **N (Null)**: noise-only / mock 데이터 통과 시뮬 의무 (false positive rate 점검).
- **F (Falsifier)**: §3 등록 임계값만 사용. 사후 임계값 조정 금지.

각 단계 산출물:
- B: 코드 SHA + frozen flag
- C: cross-falsifier 일치/불일치 표
- N: null-test χ² 분포
- F: 등록 임계값 vs 측정값 직접 비교

---

## §5 Decision tree (L657 3 시나리오)

```
DR3 w_a measured
        │
        ├── PASS  → paper §5 update + §7 outlook 갱신 + framework 유지
        │            (8인 Rule-A 사후 검증 의무)
        │
        ├── Inconclusive → minimal update only
        │            (다음 falsifier 대기, framework 유지)
        │
        └── KILL  → 두 갈래 (8인 Rule-A 결정):
                     (a) paper retraction (arXiv withdraw)
                     (b) framework 격하 (phenomenological → speculative)
```

**의무**: 시나리오별 action 은 사전 등록. DR3 결과 본 후 갈래 변경 금지.

---

## §6 Multi-session 의무 (L633 H2 reference)

**금지**: 본 세션 단독 평가.

**의무**:
1. 외부 cross-agent 의무 (L620 Path 1/2/3 중 최소 2개)
   - Path 1: independent LLM cross-check
   - Path 2: human reviewer (외부 cosmologist)
   - Path 3: alt-tool re-run (CLASS / hi_class)
2. 8인 Rule-A 사후 검증
3. 4인 Rule-B 코드 검증 (chi2_joint 재실행, evidence 재계산)
4. 검증 미달 시 결과 inconclusive 처리

---

## §7 Public commitment

**arXiv preprint §7 outlook 의무 문구** (구조 plan):
- 본 preregistration OSF DOI cross-ref
- DR3 공개 일자 expected
- 임계값 표 (§3) 직접 인용
- decision tree (§5) 직접 인용

**동시 등록**:
- OSF DOI (immutable)
- GitHub release (tag + commit hash)
- arXiv preprint v2 (footnote cross-ref)

---

## §8 8인 Rule-A 의무 (CLAUDE.md L6 룰 적용)

**합의 필수 항목**:
1. §3 임계값 정량 (PASS / Inconclusive / KILL 경계)
2. §5 decision tree 갈래별 action 확정 (특히 KILL 의 a/b 선택 기준)
3. §6 multi-session protocol 확정 (Path 조합)
4. §7 arXiv §7 footnote 정확 문구

**산출물**: 8인 합의 minutes → `results/L660/RULE_A_MINUTES.md` (별도 세션).

---

## §9 OSF DOI workflow plan

1. 8인 Rule-A 합의 완료 → 본 plan 의 placeholder 모두 정량화.
2. OSF 프로젝트 생성 (`SQMH DR3 preregistration`).
3. 문서 immutable upload (PDF + raw .md).
4. DOI 발급 → GitHub release `vL660-prereg-<date>` tag 와 cross-link.
5. arXiv preprint v2 §7 footnote 갱신 (DOI 직접 인용).
6. 최종 hash 검증: OSF PDF SHA == GitHub release SHA.
7. DR3 공개 일자 *이전* 모든 단계 완료 의무.

**DR3 공개 후 단계 변경 금지** (falsifiability 무효 방지).

---

## §10 정직 한 줄

본 plan 은 preregistration document 의 *구조* 만 정의한다. 임계값 정량값 / decision tree action 갈래 / multi-session Path 조합은 모두 별도 8인 Rule-A 세션에서 lock-in 되며, 본 plan 단독으로는 falsifiability 를 확보하지 못한다.
