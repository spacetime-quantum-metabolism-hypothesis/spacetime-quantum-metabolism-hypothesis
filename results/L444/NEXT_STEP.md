# L444 — NEXT_STEP

## 즉시 후속
1. **Bibtex 매핑**: T3/T4 각 행의 출처 (L-task 또는 paper §)을 `paper/references.bib` 키로 변환. 현재 표는 ``L48--L54'' 같은 L-id로만 표기.
2. **paper §8과 T4 동기화**: 22행 모두 §8.1~§8.10 어딘가에 본문 텍스트가 존재하는지 확인 — #19 (D1 cross-regime 31× off), #20 (NS regime), #21 (1/π vs 1/(2π)), #22 (cluster hybrid)는 새로 §8.x 추가 필요 가능성.
3. **paper §2와 T1/T2 정합**: 현재 02_sqmh_axioms.md는 L0/L1 두 공리로 압축. T1은 a1~a6 6공리 표기 — 두 표기 사이의 매핑 노트(``L0 ⊃ a1+a3+D2'' 등) 한 단락 추가 필요.

## 이론 측 후속 (T4 mitigation 경로)
- T4#2 (τ_q 이중 정의): L56 옵션 D 채택했지만 σ_macro/σ_micro = 2.6e60 다리 미증명. L58 후속 작업 (RG flow / coarse-graining 후보).
- T4#9 (DESI w_a): L78 Γ_0(t) 후보 + L112 wrong-sign 우려. DR3 (~2027) 결과 대기.
- T4#11 (Lagrangian partial): L118 SK formal 진행. Full QFT는 Phase 6.
- T4#13 (3-regime empirical): L142 Landau-Ginzburg / L165 cubic-RG는 plausibility만. action principle 도출은 미완.

## 데이터 측 후속
- **MICROSCOPE-2 (~2027)**: T3#3, #20 (P3, T35) 결정.
- **SKA Phase 1 (~2028)**: T3#7, #21 (P7, T36) 결정.
- **ATLAS-3D / SAMI (~2025-2030)**: T3#15 (G2) 결정 — π/3 vs 2 factor.
- **DESI DR3 (~2027)**: T4#9, #17 직접 영향.

## 표 자체 후속
- LaTeX 컴파일 테스트 (booktabs + table*).
- 표 폭이 컬럼 넘어가면 `\small` → `\footnotesize` 또는 행 수 분할.
- T3 22행은 부록으로 빼고 본문에 ``key 6'' 표만 두는 옵션 검토.
