# L318 — 4인 review (paper figures + tables plan)

## 평가
- 9 essential figures + 4 tables 구조 JCAP 한도 (본문 ≤ 10 figure) 정합.
- 색맹 안전성: Wong palette / cividis 명세 OK. F8 grouped bar 는 hatch pattern 추가 권고 (grayscale 안전).
- 단위/축 명세: F1 σ_0 [m³ kg⁻¹ s⁻¹] SI 표기 정합. F3 a_0 [m s⁻²] OK. F4 log-log axis 명시 OK.
- Caption clarity: 모든 figure 에 "지지/기각 명시" 패턴 강제 — 정직성 확보.
- Reproducibility: results/Lxx/report.json 단일 의존 + seed 고정 + git hash 규약 적절.
- T3 22-row longtable 압박: 본문 6 + 부록 분리 옵션 합리적. 실제 분할은 L320+ TeX 작업에서 결정.

## 보강 권고
- F1 σ_0(env) aggregation pipeline 부재 → L319 선행 작업 필수. 본 spec 만으로는 figure 생성 불가.
- F9 facility forecast 1σ 추정 — 공개 ETC 출처 (DESI DR3 spec, Euclid Red Book 등) caption 에 명시 의무화.
- T2 derived quantities: n₀, μ 개별값 표기 금지 (CLAUDE.md 규칙) — 곱 n₀μ 만 기재.
- F3 caption 에 "a_0 = c·H_0/(2π) 는 derivation 결과이며 fitting 결과 아님" 명시 권고 (오해 방지).
- F5 Bianchi shear 레벨 3종 선택 기준 (e.g. σ/H = 0, 0.01, 0.05) caption 명시 필요.

## 위험 재확인
- F2 SPARC 3-galaxy 선택 편향 가능 — low/mid/high SB 대표성 정당화 caption 필요.
- F8 IC 비교에서 AICc 패널티 (CLAUDE.md 과적합 방지) 명시 — SQMH free param 수 footnote.
- T4 evidence summary 의 Δχ² vs LCDM 계산은 fixed-Om vs best-fit Om 혼동 금지 (CLAUDE.md L34 규칙).

## 정직
spec 확정만 완료. 실제 figure rendering / TeX 표 생성 / aggregation pipeline (특히 F1) 은
별도 long-running session (L319+) 필수. 본 review 는 plan 적정성만 판정.
