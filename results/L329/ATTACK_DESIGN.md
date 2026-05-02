# L329 ATTACK_DESIGN — SQT vs N=5 Alternatives Global Head-to-Head

## 목표
L232~L236 (단일 이슈별 비교) + L271 시점 cross-theory 합산 + L290 (BTFR) + L291 (Bullet)
를 **하나의 글로벌 best-fit 좌표축** 위에 다시 줄세움.
질문: SQT 가 *모든* alternatives (MOND / TeVeS / EMG / EG / SymG) 보다
글로벌 ΔAICc 기준으로도 우위인가? 아니라면 어디서 깨지는가?

---

## 비교 축 5개 (각 이론 × 5 axis)

1. **Joint dataset ΔAICc**
   - dataset: BAO (DESI DR2 13pt) + SN (DESY5) + CMB (compressed) + RSD + (선택) WL S8.
   - 자유 파라미터 수 / AICc 패널티 명시 (CLAUDE.md 과적합 원칙).
   - 비교 기준선: LCDM joint best-fit χ².

2. **Bullet cluster (1E 0657-558)**
   - lensing 피크 vs 가스 피크 분리 ~150 kpc.
   - 각 이론이 무시 / 우회 / 정합 중 어디에 속하는지.
   - SQT: P27 (L291) 결과를 글로벌 좌표에 재투영.

3. **Cluster regime σ (cluster scale velocity dispersion)**
   - 갈락틱 한정 이론은 cluster 에서 어떤 식으로 깨지는지 정성 + 정량.
   - SQT: depletion zone 의 cluster 스케일 누적 효과를 별도 평가.

4. **Cosmic Λ origin**
   - 각 이론이 우주상수/암흑에너지의 미시적 기원을 가지는가.
   - SQT 4-pillar (L257~L261) 와 alternatives 의 origin status 대조.

5. **Falsifiable prediction count (14-list)**
   - SQT 14 prediction set (P15-P22 + 기존 P11-P14 등) 대비
     각 alternative 가 동일 데이터셋에서 falsifiable 한 정량 예측 수.
   - "정량 falsifier" 정의: 5σ 가능 시설 매핑 + 부호 + 크기 명시된 것만 카운트.

---

## 8인 토의 방향 (역할 사전 배정 금지)

8인은 위 5개 축을 자율 분담.
- 누구도 "MOND 담당", "AICc 담당" 등 라벨 받지 않음.
- 자연 발생 분업만 허용.
- 결론은 "SQT 우위 / 동률 / SQT 열위" 3-tier 로 axis × theory = 25 셀 채움.

## 과적합 가드
- ΔAICc 보고 시 (k_SQT, k_alt) 동시 명시.
- SQT Branch B (3 free) vs MOND (1 free, a_0) 비대칭 강조.
- "SQT 가 더 많은 자유도로 이기는" 셀은 별도 ⚠ 표기.

## 산출물
- /results/L329/REVIEW.md : 25-cell matrix + 8인 honest verdict.
- /results/L329/NEXT_STEP.md : 깨진 셀 (있다면) 후속 공격 설계.

## 금지 (CLAUDE.md 최우선-1, 최우선-2)
- 본 문서에 수식, 수치 파라미터, 유도 경로 힌트 일절 없음.
- 8인은 직접 SPARC / DESI DR2 / DESY5 / Planck-compressed / RSD 데이터에서 ΔAICc 재도출.
- 과거 L232~L236 결과는 *입력 가설* 로만 취급, 자동 채택 금지.
