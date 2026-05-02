# L331 — Global Best-Fit Audit (Single Loop)

**Loop**: L331 (single, synthesis-focused)
**Target**: 245-loop 누적 종합 + 글로벌 최적합 audit (BB σ_0 후보가 진정 global 인가, local 함정인가?)
**Date**: 2026-05-01

---

## 1. Audit 의도

L322 ATTACK_DESIGN 에서 8인 공격팀이 "BB σ_0 후보 = global 인가" 질문에 대해 A1-A8 8개 채널을 설계했고, 합의 Top-3 = **A4 multi-start + A5 merger test + A7 dynesty multimodal**. L323-L330 디렉터리에는 **실제 실행 산출물 부재** (디렉터리 비어 있음 — 파일 시스템 확인). 따라서 L331 은 **이미 수행된 235-loop 결과** 위에서 글로벌성 audit 를 **간접 증거** 로 시도한다.

직접 실행 (A4/A5/A7) 은 본 단일 loop scope 밖. 본 audit 는 기존 누적 증거 4 종을 글로벌성 관점에서 재해석한다.

## 2. 간접 증거 채널 (4 종)

| 채널 | 출처 loop | 글로벌성 관련 해석 |
|------|-----------|----|
| C1 prior sensitivity | L275 | σ_0 prior shift 시 posterior 0.045 dex 만 이동. **단일 mode 안정성** 시사하나 multimodality 는 분리 못 함. |
| C2 jackknife / leverage | L278 | leverage outlier 없음. **현재 mode 가 데이터 일부 의존이 아님**. global vs local 직접 증거는 아님. |
| C3 marginalized evidence | L281 | ΔlnZ = 0.8 → 다른 mode 가 ΔlnZ ≳ 0.8 안에 있을 가능성 **배제 못 함**. |
| C4 SBC rank | L280 | rank uniform → posterior 가 "한 mode" 에 대해선 calibrated. multi-mode coverage 는 미검증. |

## 3. Audit 결론

**글로벌 최적합 미입증.** 현재 단일 mode (cosmic 8.37, cluster 7.75, galactic 9.56) 는:
- prior-robust (C1)
- leverage-robust (C2)
- 단일-mode 가정 하 calibrated (C4)

이지만 **multimodality 자체를 배제한 직접 검정 (A4/A5/A7) 은 미실시**. L272 mock 100% false-detection 결과는 anchor flexibility 가 spurious mode 를 만들 수 있음을 시사하므로, **글로벌성 미확정** 이 더 정직한 입장이다.

## 4. 권고 (후속 loop 가용 시)

1. **A4 (multi-start)**: 100 LBFGS Latin hypercube σ_0 ∈ [3,15]^3, distinct minima 개수 보고. (단발성 단일 loop, 100 ms × 1만 step ≈ 17 분.)
2. **A5 (2-regime merge)**: cosmic+cluster 병합 모델 ΔAICc. 부호 < 0 이면 3-regime 은 over-partition.
3. **A7 (dynesty multimodal)**: ndim=3, multimodal=True, lnZ + mode count 직접 추출.

L323-L330 부재 상태에서 위 3종 미실시 — 본 audit 는 결과 미보유 정직 명시.

## 5. 정직 명시

- A1-A8 설계는 L322 에 존재하나 **실행 결과 부재**
- 본 L331 의 글로벌성 audit 는 **간접 증거 4종** 으로만 수행 → "단일 mode 안정성은 시사, multimodality 배제는 미입증"
- L272 mock 100% / L281 marginalized ΔlnZ=0.8 → **글로벌성 의심 채널은 여전히 열려 있음**
