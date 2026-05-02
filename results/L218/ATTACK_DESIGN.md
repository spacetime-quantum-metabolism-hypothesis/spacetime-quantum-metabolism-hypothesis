# L218 — PARTIAL #2: Δchi² head-to-head independent data

## 8인팀 공격
**Target**: L208 ΔAICc=99 결과의 anchor caveat. DESI BAO + Planck CMB + DESY5 SN 같은 데이터로 fit. 독립 데이터 (eBOSS Lyα BAO, Pantheon+, ACT DR6)로 cross-check 필요.

### 약점
1. 99 는 L208 anchor 데이터 (DESI DR2). cherry-picking 의심.
2. eBOSS Lyα-α BAO (Hou+2021) 미사용.
3. ACT DR6 H0 ≠ Planck H0.
4. Pantheon+ 1701 SNe vs DESY5 1635 SNe.

### KILL
- K-cross1: 독립 데이터셋에서 ΔAICc<10 면 anchor artifact.

### 실행
- 토이: chi^2 LCDM vs SQT on eBOSS Lyα + Pantheon+. 데이터 fetch 어려우니, L208 결과 + 30% noise 가정한 robustness 토이.
