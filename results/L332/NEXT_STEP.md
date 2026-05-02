# L332 NEXT STEP — 3-regime vs 2-regime 후속 행동 (8인)

## 단기 (1-2 loop)
1. **P11 NS saturation mock forecast** (B1, B2 주도)
   - g(rm1) high-ψ regime 곡률을 NS M_max 에 매핑. EOS family (APR, SLy4, BSk22)
     marginalization. 2-regime / 3-regime 모델 fit, ΔAICc 분포 1000 mock.
   - 산출: simulations/L332/run.py (단일 forecast).
2. **2-regime merge 모델 lock-in** (B3)
   - L322 multistart_result.json best 파라미터를 baseline 으로 고정. 3-regime 은
     "조건부 reserve" 로 보존만, 본문 주장 baseline 에서 제외.

## 중기 (3-8 loop)
3. **P9 dSph + void 보조 anchor 동시 forecast** (B4)
   - 단독 효과 약하나 P11 과 결합 시 정보 이득 평가. ΔAICc joint forecast.
4. **EOS systematic 통제** (B5, B6)
   - NS M_max forecast 에 EOS prior 폭 ±0.15 M_sun, ±0.30 M_sun 두 시나리오.
     Robust 한 ΔAICc 임계 산출.
5. **글로벌 입증 가능성 정량** (B7)
   - "P11 + EOS tight" 조건에서 3-regime favor 확률 (Bayes factor > 3) 추정.

## 장기 (9+ loop, 데이터 의존)
6. **DESI DR3 + Pantheon+ extended** 출시 후 anchor 없이 자체 재판정.
7. **Athena/SKA forecast** (cosmic void galaxy density 정밀화).

## 즉시 결정
- 본문 baseline: **2-regime merge** 채택 (정직).
- 3-regime: "anchor-conditional reserve, P11 dependent" 명시.
- 등급 -0.07 유지, JCAP 91-95% 유지 (변화 없음).
- 3-regime 글로벌 입증 강행 금지: 데이터 부족.

## 정직 한 줄
현 시점 글로벌 입증 불가능. 미래 anchor (P11) 에 조건부.
