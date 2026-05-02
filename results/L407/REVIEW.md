# L407 REVIEW — 4인팀 코드리뷰 + 통합 결론

## 1. 4인팀 코드 자율 분담 결과

자율 분담 (사전 역할 지정 없음):

- **R1 (수치/적분)**: `cubic_roots()` 검증 — β(x) = a x − b x² + c x³ factorization 후 quadratic discriminant 계산. x=0 root 항상 포함, 이는 *shift 후* x − x₀ 의 root → x₀ 는 항상 free-scan 결과에 1 root 로 포함됨. 정상.
- **R2 (통계/scan 설계)**: log-uniform |a|, |b|, |c| ∈ [10⁻², 10²], sign random. 충분한 dynamic range. 300k samples → MC error ≈ 0.05% on 1.4% probability — 통계적 충분.
- **R3 (해석/정합성)**: shifted_cubic_roots() 의 x₀ = LOG_COSMIC = 8.37 선택 → free scan 결과의 root 분포가 cosmic 부근에 spike. middle root 는 spike 와 *독립적 분포* 인지 확인 필요. → 결과: middles histogram 이 8.37 부근 양쪽으로 대칭, 단봉 아닌 광역 분포. cluster band 1.4% 는 prior length 의 자연 분율 (band width 0.5 dex / window 폭 ~7 dex ≈ 7%) 보다 *낮음* → x₀ shift effect 로 saddle 이 x₀ 부근 spike 하는 측면은 있으나, cluster band 가 x₀ 직하방에 있어 자연 분율보다 낮게 나옴. 해석: free scan 도 cluster 위치 자연성 결여 확인.
- **R4 (구조적 발견)**: between-prior P=0 finding 은 *해석적 명백* (CLUSTER_BAND[1]=8.0 < LOG_COSMIC=8.37). 코드 정상. 이건 시뮬레이션이 *발견*한 게 아니라 *수치적으로 확정*한 사실.

### 코드 이슈 (4인팀 발견)
- 없음. 단, 대규모 sample 에서 Python loop 가 ~수 초 — vectorization 가능하나 결과 영향 없음. 우선순위 낮음.
- numpy 2.x 호환성 OK. `trapz` 미사용.
- print 유니코드 미사용. cp949 안전.

### 4인팀 결론
**코드 정상**. 결과 신뢰 가능. 통계적 결론 robust.

---

## 2. 통합 정직 결론

### 2.1 priori 도출 가능성: **부분만 (sign-only)**, magnitude 영구 anchor

L407 의 정량 결과:
- 자유 RG cubic scan 에서 saddle 이 cluster band 에 떨어질 확률 1.4%
- ±0.10 dex (실험 정밀도) 매칭률 0.5%
- 표준 between-FPs 가정 시 P=0 (구조적, cluster < cosmic IR)

→ "RG saddle 이 자연스럽게 cluster 영역에 위치한다"는 주장은 **데이터 없이는 성립 불가**. postdiction 정직 인정 필수.

### 2.2 base.md 권고 변경사항 (실제 적용 권한은 user 결정)

1. **§3.2 ★★ caveat 추가**:
> "★★ cubic β(σ) saddle topology 자체의 정합성도 미입증: 경험적 σ_cluster (7.75) 가 σ_cosmic (8.37) 보다 작아 표준 monotone-RG (IR<saddle<UV) 와 부등식 부합 안 됨. quintic-RG 또는 다단계 flow 필요. 이는 § 3.4 postdiction caveat 와 함께 readers 에게 명시."

2. **§6.1 row "RG b, c future"** → "RG b, c + topology compatibility future" 로 확장.

3. **§7 future work priority**: Wetterich Wilsonian truncation (P1) + 1-loop EFT matching (P2) 를 top-2 로 격상.

4. README "Claims status" 의 "96.8% 호환" 표기에 "(topology 정합성은 별도 future work)" 한 줄 추가.

### 2.3 paper 포지셔닝 (8인팀 합의)

> "SQT 는 σ₀(env) 비단조성을 *데이터 fit* 으로 발견하고, monotonic 가설을 17σ-equivalent 로 기각하는 *falsifiable test* 를 제공한다. *위치 자연성*은 미입증이며, RG b/c 계수 도출 + topology 정합성은 future work 의 핵심 우선순위다."

이는 §3.4 의 *기존 caveat* 와 일치 — paper 의 정직성을 *유지*하며 L407 발견을 *반영*하는 최소 수정.

### 2.4 PRD vs JCAP 포지셔닝 영향

base.md L692 (JCAP 타깃 조건: "정직한 falsifiable phenomenology") 는 그대로 유효. PRD Letter 는 Q17 (priori 도출) 미달성 상태이므로 진입 불가 — L407 결과 *변동 없음*.

---

## 3. 산출 파일 목록

- `results/L407/ATTACK_DESIGN.md` — 8인팀 reviewer 공격 시뮬레이션 + 5 path 평가
- `results/L407/NEXT_STEP.md` — Wetterich/EFT/holographic 3 path 정량 + 옵션 A/B/C 분석 + priority stack
- `results/L407/REVIEW.md` — 4인팀 코드리뷰 + 통합 결론 + base.md 권고
- `results/L407/saddle_distribution.json` — RG saddle FP 위치 정량 분포
- `results/L407/saddle_distribution.png` — 분포 히스토그램 시각화
- `simulations/L407/run.py` — 실행 스크립트

## 4. 한 줄 요약

priori 도출 단기 불가 → §3.4 caveat 유지 + §3.2 ★★ topology caveat 추가 + RG b/c/topology future work 우선순위 격상 (옵션 C, 8인팀 만장).
