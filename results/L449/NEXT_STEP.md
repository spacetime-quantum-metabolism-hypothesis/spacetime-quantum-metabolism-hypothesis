# L449 NEXT_STEP — 8인팀 다음 단계 설계

선행: L449/ATTACK_DESIGN.md (B1–B8) — dSph anchor 사전등록 path 의 6항목
메타-거버넌스. 4 조건의 *수치값* 미지정 (CLAUDE.md [최우선-1] 준수).

원칙: CLAUDE.md [최우선-1, 2] — 본 NEXT_STEP 은 사전등록 문서의 *섹션
골격* 과 paper/base.md 갱신 *정책 문구 형식* 만 제시. 4 조건의
임계 수치 / 부호 / prior 폭 절대 미지정.

---

## 1. 8인팀 토의 (요약 — 사전등록 path 의 6항목 잠금)

**P1**: "L424 4 조건 (부호-결정 임계 / ρ_env 매핑 / σ₀ 변환 prior /
175-point mock false-rate Δ) 사전등록은 paper §6.1 row 14 의 'v-preDR1-
2026.NN' triple-timestamp (arXiv + GitHub tag + OSF DOI) 표준을 dSph
P9 에도 동일 적용. row 14 가 cosmic-shear 4.4σ falsifier 사전등록
프로토콜로 이미 작동 중 — 본 dSph 사전등록은 그 프로토콜의 *재사용*."

**P2**: "단, dSph 사전등록은 *측정값 자체* 가 이미 공개 카탈로그
(McConnachie 2012, Walker 2009, Gaia DR3) 에 있음 — Euclid DR1 처럼
'data-blind' 가 아님. 따라서 prereg 문서는 '카탈로그 측정값은 본 시점
이전에 이미 공개되어 있으나 **본 시점 이후 추가 archive 도입은 금지**'
잠금 진술이 추가로 필요. ATTACK B1 대응."

**P3**: "결정 매트릭스 (ATTACK B2) 형식: 3×4 매트릭스 (3 분기 × R-grid
{2,3,5,10}). 각 셀에 사전 결정 (PASS / FAIL / INCONCLUSIVE) 지정.
사전등록 문서는 셀 내용을 비워둘 수 없음 — '데이터 보고 채움' 시 사전
등록 의미 상실. 결정 매트릭스의 *형식* 만 본 NEXT_STEP 에 제시,
구체적 cell label 은 prereg draft 에서 사전 결정."

**P4**: "ρ_env 매핑 primary/secondary 잠금 (ATTACK B3): prereg 문서는
'primary mapping = X, secondary = sensitivity check only' 로 지정.
X 의 선택 (LG-outer vs galactic-internal) 자체는 prereg draft 에서
*8인 합의* 로 결정 — 본 NEXT_STEP 에서 미지정. 다만 *합의 메커니즘*
(만장일치 / 다수결 / synthesizer 결정) 을 prereg 메타-규칙으로 명시."

**P5**: "변환 prior 함수형 (ATTACK B4): Walker 2009 의 σ_los → M_dyn
공식 또는 McConnachie 2012 의 mass-to-light 변환 어느 한 채널을
prereg 에 *함수 형태* 로 고정. 함수형 자체의 출처 (peer-reviewed paper
+ DOI + 식 번호) 가 prereg 문서에 명기. prior 분포 폭은 인용 paper 의
publication σ 그대로 차용 (no inflation, no contraction)."

**P6**: "175-point mock false-rate threshold (ATTACK B5): paper §3.5
의 100% baseline 대비 'X% 이하면 강화' 의 X 자체는 prereg draft 에서
8인 합의로 결정. 본 NEXT_STEP 에서 미지정. 다만 X 가 *baseline 보다
낮은* 값임 (즉 조건부 falsifier 임) 만 형식적 잠금."

**P7**: "Sample lock (ATTACK B7): 5 dSph (Draco/UMi/Scl/Sextans/Carina)
+ 제외 3개 (Fornax/Leo I/Leo II) 사유 prereg 명기. 제외 사유는
*objective criterion* (예: distance > X, contamination > Y) 만 허용 —
'tension 결과 회피' 사유 금지. Gaia DR4 신규 dSph 발견 시 *re-registration*
필수 (automatic addition 금지) — ATTACK B7 잠금."

**P8 (synthesizer)**: "다음 단계 합의:
(a) **즉시 (이번 세션)**: dSph_PREREG.md draft 작성 — 6항목 섹션
    골격 + triple-timestamp 채널 + 잠금 진술. 4 조건 *수치값* 빈 칸
    placeholder 로 두고 *형식적* 잠금만 제시.
(b) **즉시**: paper/base.md §6.1 row #5 + §4 P9 row 갱신 *정책 문구*
    형식 제시. 본 세션은 *형식 제시* 만 — 실제 base.md 편집 PR 은 별도
    세션 (L450+).
(c) **NO (다음 세션)**: 8인 합의 회의 — primary mapping / 부호-결정
    매트릭스 cell label / 변환 prior 함수형 출처 / false-rate threshold
    / sample 제외 objective criterion 5 항목 *수치/부호* 결정. 별도
    세션 (L450) 에서 8인 토의로만 진행.
(d) **NO (paper update)**: dSph_PREREG.md 의 8인 합의 후 final 버전
    triple-timestamp commit. paper §6.1 row #5 + §4 P9 row 의 *동일
    PR* 갱신. 별도 세션 (L451)."

---

## 2. 다음 단계 task list

| # | task | 즉시? | budget |
|---|------|------|--------|
| N1 | dSph_PREREG.md draft 6항목 섹션 골격 | YES | <1min |
| N2 | paper §6.1 row #5 + §4 P9 row 갱신 정책 문구 형식 | YES | <1min |
| N3 | REVIEW.md 4인팀 형식 검토 (수치 검토 아님) | YES | <1min |
| N4 | 8인 합의 회의 (primary mapping / 매트릭스 cell / prior 출처) | NO (L450) | 1d |
| N5 | dSph_PREREG.md final + triple-timestamp commit | NO (L451) | 0.5d |
| N6 | paper/base.md §6.1 row #5 + §4 P9 row 갱신 PR | NO (L451) | 0.5d |
| N7 | OSF DOI mint + arXiv preprint cross-reference | NO (L451) | 1d |

본 세션은 N1–N3 만 수행 → results/L449/{ATTACK_DESIGN, NEXT_STEP, REVIEW,
dSph_PREREG}.md.

---

## 3. paper/base.md 갱신 정책 문구 형식 (N2)

### §6.1 row #5 갱신 안 (정책 형식)

현재 (L424 권고 강화 후 가정):
> | 5 | Three-regime 강제성 약함. L424 forecast 결과 ... 4 조건 사전등록
> 후만 가능. ... | ACK_REINFORCED | 4 조건 사전등록 (L425 GitHub release
> tag) → 실 SPARC+dSph mock 재실행 |

**L449 추가 정책 문구**:
> Pre-registration 채널: triple-timestamp (GitHub release tag
> `v-dSph-prereg-YYYY.NN` + OSF DOI + paper commit hash). 등록 문서:
> `results/L449/dSph_PREREG.md` (8인 합의 final 버전, L451 commit).
> 등록 *후* 어떤 archive 도입도 금지 — re-registration 필수.

### §4 P9 row 갱신 안 (정책 형식)

현재 (가정):
> | P9 | dSph σ₀ saturation | low-ρ_env regime 재진입 | 정성 |

**L449 권고**:
> | P9 | dSph σ₀ saturation | **conditional** (4 조건 prereg 후만
> falsifier) | qualitative → conditional-falsifier (prereg L451 후
> 활성화) |

---

## 4. dSph_PREREG.md 섹션 골격 (N1)

dSph_PREREG.md 에 포함될 6 섹션:

1. **Sample lock**: 5 dSph 명단 + 제외 3 dSph + 제외 objective criterion.
   Gaia DR4 신규 발견 시 re-registration 정책.
2. **Primary ρ_env mapping lock**: primary 매핑 1개 명시 + secondary
   sensitivity check 만 허용 잠금.
3. **σ₀ 변환 prior lock**: 함수형 (peer-reviewed paper + DOI + 식 번호)
   + prior 분포 폭 (인용 publication σ 그대로).
4. **부호-결정 결정 매트릭스 (3 분기 × R-grid)**: 12 cell 의 PASS/FAIL/
   INCONCLUSIVE label 사전 결정.
5. **175-point mock false-rate threshold**: paper §3.5 100% baseline
   대비 강화/약화 임계값 + 결정 규칙.
6. **Triple-timestamp lock**: GitHub tag + OSF DOI + paper commit
   hash 3 채널 동시 등록.

각 섹션은 잠금 진술 (locking statement) 포함 — "본 시점 이후 [항목]
변경 시 사전등록 무효" 형식.

---

## 5. 회복 가능성 정직 판정

- 본 사전등록 path 가 *완성* 되어도 (L451 final), dSph anchor 가
  three-regime 강제력을 *자동 회복* 시키는 것은 아님 — L424 4인팀 결과
  (mock false-rate 0% baseline) 가 paper §3.5 175-point mock 으로
  재현되어야 강제력 회복 *측정 가능*. 즉 본 prereg 는 *측정 path 를
  cherry-pick-free 로 잠그는* 도구이지, 결과 자체가 강화임을 보장하지
  않음.
- 만약 사전등록 후 4 조건 모두 prereg 임계 충족 시 → §6.1 row #5
  ACK_REINFORCED → ACK 또는 RECOVERY 격상 가능 (별도 세션 판정).
- 만약 4 조건 중 하나라도 미충족 시 → row #5 status 유지 + P9 conditional
  falsifier 등급 유지 → 정직 disclosure.
- **JCAP timeline**: 사전등록 commit 자체는 paper submission *후* 라도
  유효 (post-publication preregistration). 다만 paper §6.1 row #5
  갱신은 submission *전* 권장 (referee review 와 동시 진행 가능).

→ 본 L449 의 산출은 메타-거버넌스 design only. 실제 사전등록 commit /
DOI mint / paper PR 은 L450 (8인 합의) → L451 (commit) 분리 진행.
