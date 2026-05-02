# L345 NEXT_STEP — Bayes factor 계산 실행 절차

## 0. 실행 전 정직 점검
- 본 loop 의 *유일한* 판정 척도는 ln Z 차이 (Bayes factor). Akaike weight,
  AICc, BIC 결과는 보조 보고만 허용. 결론 진술에 인용 금지.
- 사전분포는 *반드시 사전 등록* 한 후 evidence 계산 시작. 사후 사전분포 변경
  금지 (post-hoc prior tuning 은 결과 무효).

## 1. 함수 가족 사전 등록 (방향만)
- 단조 family M: 환경 변수의 단조 함수.
- 비단조 family N: 단일 극값(또는 변곡)을 갖는 함수.
- 두 family 의 자유도 차이는 표시 필수 (k_N − k_M).
- 구체적 함수형은 8인 팀이 자율 선택. Command 는 함수형 명시 금지 (최우선-1).

## 2. 사전분포 등록표 (구체값은 팀이 도출)
| 항목 | 단조 M | 비단조 N | 비고 |
|------|--------|----------|------|
| 환경 변수 도메인 | 동일 | 동일 | 데이터 범위 |
| 진폭 prior | wide weakly-informative | wide weakly-informative | 동일 family |
| 위치/극값 prior | — | uniform over 도메인 | 좁히기 금지 |
| 자유도 | k_M | k_N (=k_M+Δ) | Δ 명시 |

두 가지 prior set 모두 실행:
- Set A: wide weakly-informative.
- Set B: tight physical-scale (이론적 근거 명시).
결과는 두 set 모두 보고. Set A 를 primary, Set B 를 sensitivity 로 명시.

## 3. Evidence 계산
- nested sampling: dynesty static (nlive=1000 권고, 자율 조정 가능).
  - dynamic mode 보조 실행 (수렴 검증).
- 멀티시드: 시드 5개. ln Z 평균/표준편차 보고.
- 수렴 진단: dlogz < 0.1, 그리고 멀티시드 σ(ln Z) < 0.5 충족 시에만 인정.
- 워커: `multiprocessing.get_context('spawn').Pool(n)`, n ≤ 9.
- 환경: `OMP/MKL/OPENBLAS_NUM_THREADS=1` 강제.

## 4. 통계 보고
- Δ ln Z = ln Z(N) − ln Z(M), 양 prior set 별.
- Δ ln Z 표준오차 = sqrt(σ_N^2 + σ_M^2) 멀티시드 기반.
- Jeffreys scale (ATTACK_DESIGN A4) 항목으로 분류.
- Akaike weight 는 같은 fit 에서 함께 계산. 부호 일치 여부만 보고.

## 5. 판정 분기
- Set A 와 Set B 부호가 같고 |Δ ln Z| > 2.5: 결론 robust.
- 부호 같으나 한쪽 |Δ ln Z| < 1: weak/inconclusive.
- 부호 다름: prior-sensitive. 결론 "evidence does not robustly prefer either".
- 어느 경우든 결과 그대로 carry-over. 주관적 강조 금지.

## 6. 산출물 작성 규칙
- 모든 수치는 ASCII. 파일 저장 후 인코딩 확인.
- print() 유니코드 금지 (cp949). matplotlib 라벨만 유니코드.
- 결과 파일 경로: `results/L345/evidence/<prior_set>/<seed>/run.json`.
- 종합표: `results/L345/EVIDENCE_TABLE.md`.

## 7. 위반 점검 체크리스트
- [ ] Command 에 수식/파라미터 값 없음 (최우선-1).
- [ ] 8인 팀 자율 도출 보장 (최우선-2).
- [ ] 사전분포 사후 변경 없음.
- [ ] dynesty 수렴 진단 통과.
- [ ] Akaike weight 가 ln Z 결론을 대체하지 않음.
- [ ] 멀티시드 5개 일치.

## 8. 차기 loop 연결
- 결과가 inconclusive 일 경우 L346 에서 데이터 측 cross-validation (bin LOO)
  로 비단조 신호의 robustness 재검증.
- 결과가 monotonic 우세일 경우 본문 "비단조 선호" 표현 정정 (paper revision).
- 결과가 non-monotonic 우세일 경우 sigma_0(env) 함수형 정식화는 별도 loop.

## 9. 한 줄 (정직 한국어)
**비단조가 정말로 우세한지는 사전분포를 정직하게 등록한 ln Z 만이 답한다.**
