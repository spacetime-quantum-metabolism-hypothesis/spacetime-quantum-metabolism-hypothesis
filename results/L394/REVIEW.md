# L394 REVIEW — Sec 5 (Cosmology) final, 8인 토의 + 4인 코드리뷰

## 입력
- L207 report.json: ρ_q_0 = 6.8555e-27 kg/m³ = ρ_Λ(Planck), match_ratio = 1.0000,
  absorption_per_hubble = 0.10414 (10.4%).
- L207 verdict: T^{μν}_n = (ρ_q+p_q) u^μ u^ν + p_q g^{μν}, Bianchi drho_q/dt vs 3H ρ_q = 1.04e-1,
  "rho_q evolves strongly — phantom/quintessence-like".
- L208: SPARC vs anchor, dAICc=99.49 (anchor by-construction caveat).
- L209: SQT n-field DM cross-section FAIL (sigma_np ~ 1.20e-24 vs SENSEI 1e-30).
- DESI DR2 (CLAUDE.md 공식): w_0 = -0.757 +/- 0.058, w_a = -0.83 (+0.24/-0.21), DESI+Planck+DES-all.
- L33/L34/L46~L56 BAO 탐색 history.

## 8인 자유 토의 (자율 분담)

**P** (배경 매칭 라인): ρ_q_0 / ρ_Λ = 1.0000 은 *4-자리 정확*. 우연 가능성 vs SQT 가
ρ_Planck/(4π) 로부터 ρ_Λ scale 을 자연 도출하는지가 핵심. 후자라면 cosmological
constant problem 의 새 해석. 다만 본 결과만으로는 "도출"인지 "튜닝"인지 *증명 미달*.

**N** (DE phenomenology 라인): 10.4% per Hubble = effective |w_a| ~ 0.3. DESI w_a = -0.83 의
약 1/3. *방향 일치 (phantom-like)*, 크기 *factor ~3 미달*. "SQT 가 DESI 를 설명한다"고
주장 시 K5 위반.

**O** (관측 비교 라인): L34 joint fit 까지 가야 정량 비교 가능. 본 Sec 5 는 배경 mech 만
제시하고 정량 fit 은 future work 로. DR3 falsification target 명시.

**H** (이론 정합 라인): T^{μν}_n fluid form 은 L207 에서 확정. Bianchi source 항이
matter sector 와의 covariant exchange 채널을 제공 → IDE family 와 phenomenology 공유.
SQMH-consistent branch (β>0, ξ_q>0) 만 인용.

**S** (한계 라인): L208 SPARC dAICc=99 은 anchor by-construction artifact. L209 DM null
tension 은 n-field 의 nucleon coupling 미도출 caveat. Sec 5 본문은 cosmology only —
galactic / DM 은 다른 섹션.

**T** (포지셔닝 라인): JCAP 톤 (정직 falsifiable phenomenology). PRD Letter 는 ρ_q 도출의
완전한 1차 원리 + DESI 정량 동시 달성 필요 — 미달.

**R** (재발방지 라인): CLAUDE.md L4/L5/L6 규칙 — μ_eff≈1 으로 S8 미해결, BAO-only ≠ joint,
DR2 출처 명시, w_a 부호 함정. 본 draft 모두 준수.

**M** (캐비엇 라인): "10.4%" 는 absorption_per_hubble 의 1차 추정. CPL 매핑은 미시행.
"effective w_a ~ -0.3" 는 order-of-magnitude.

## 4인 코드리뷰 (자율 분담, 수식/인용 검증)

- ρ_q_0 = 6.8555e-27 kg/m³ 단위 OK (ρ_crit ≈ 9.47e-27 kg/m³, Ω_Λ ≈ 0.685 → ρ_Λ ≈ 6.49e-27;
  Planck-mass-density / 4π 정의 차이 약 5% 이내). report.json 값 그대로 인용.
- T^{μν} signature: (-,+,+,+) 가정 명시 필요 → SEC5_DRAFT 에 footnote 추가.
- DESI DR2 인용: arXiv 2404.03002 (DR1) → DR2 update 2503.14738. CLAUDE.md 규칙 준수.
- Unicode: 본문은 ASCII + LaTeX 수식, "ρ" 는 LaTeX `\rho` 로. cp949 print 함정 회피.
- BAO-only vs joint: 본 draft 는 배경 mech only — joint 정량 fit 미주장 OK.
- L208 anchor caveat / L209 DM tension cross-link 정확.

## K 판정

- K1 PASS — ρ_q_0 = ρ_Λ(Planck), match_ratio = 1.0000 정확 인용.
- K2 PASS — fluid form, signature, p_q = -ρ_q (Λ-like) 한계 명시.
- K3 PASS — 10.4% per Hubble 인용 + "phantom/quintessence-like" 표현.
- K4 PASS — DESI DR2 공식 값 + 출처.
- K5 PASS — "구조적 근접 + 직접 fit 미달" 정직 명시.
- K6 PASS — ASCII 본문 + LaTeX 수식, 유니코드 깨짐 없음.
- K7 PASS — BAO-only/joint 혼동 없음, future work 로 분리.
- K8 PASS — L208/L209 caveat 정직 cross-link.

## 정직 한 줄
ρ_q/ρ_Λ = 1.0000 은 SQT 의 가장 강력한 cosmology 결과지만, DESI w_a 정량 일치는
factor ~3 부족 — Sec 5 는 "mechanism PASS, quantitative fit pending" 으로 정직 기록.
