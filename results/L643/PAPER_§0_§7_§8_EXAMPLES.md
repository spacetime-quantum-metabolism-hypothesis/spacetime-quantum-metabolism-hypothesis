# L643 — Paper §0 / §7 / §8 본문 예시

본 문서는 paper plan v3 의 §0 (Abstract), §7 (Outlook), §8 (Reproducibility) 본문 예시를 plan 수준 산출물로 제공한다. 어떤 paper / claims_status / 디스크 파일도 직접 수정하지 않으며, 수식·파라미터 값·새 prediction·새 후보는 일절 도입하지 않는다. 어휘는 L591 / L596 / L635 동기 가이드를 따른다 — "통합 이론" / "0 free parameter" / "priori 도출" 표현은 영구 금지하고, "phenomenology framework" / "multi-session" / "PASS_MODERATE" 로 통일하며, 외부 출판 표현 ("PRD Letter target") 은 내부 OR-게이트 표현으로 치환한다.

본 산출물의 채택 절차는 다음과 같다 — (i) 8인 Rule-A 순차 리뷰로 §0/§7/§8 어휘·범위·정직성 합의 확정, (ii) 4인 Rule-B 코드 리뷰는 §8 verify_*.py / Docker / OSF DOI 워크플로 텍스트가 실제 산출물 (L637 7/7 PASS, expected_outputs JSON 스키마) 와 일관한지 확인 후, (iii) plan v3 본문 통합. 리뷰 미완료 상태에서 paper 본문 / claims_status / 외부 산출물 어디에도 본 예시를 반영하지 않는다.

정직 한 줄 — 본 예시는 어휘·범위·한계 preview 의 plan 수준 초안이며, §0 의 정량 결과 표현, §7 의 박탈 risk 서술, §8 의 재현 절차 모두 8인 Rule-A 합의 후 확정된다.

---

## §0 Abstract (1 paragraph, 250–300 자)

We present a phenomenology framework that organises a 6-axiom Spacetime-Quantum-Tension (SQT) structure under four operational pillars — background dynamics, growth, screening, and reproducibility — within an explicit scope axiom A0 that restricts current applicability to the Mpc-scale linear regime and selected galactic-rotation tests. On the calibrated benchmarks the galactic-rotation discriminant a₀ attains the PASS_MODERATE band (per the L633-fixed gate language), and the σ₀ axis exhibits a dimensional uniqueness property under the multi-session derivation protocol; both numerical claims are reported with their full uncertainty budgets and the four a priori claims that were withdrawn during Phase 31–40, together with the ≈ 90 % share of fabricated-trace items already disclosed in the L591 audit. Six pre-registered falsifiers are listed and, conditional on the DESI DR3 release window, will be evaluated under the BCNF protocol; the framework is therefore presented as falsifiable phenomenology rather than as a unified or zero-parameter theory, and any priori-style derivation is treated as multi-session evidence (per L633 H2) — never as a single-session a priori claim — with limitations actively previewed in §1 and §6.

## §7 Outlook (3 paragraphs, 250–300 자 each)

### §7.1 DR3 (2027 Q2) BCNF protocol — paradigm-shift trigger

The principal outlook anchor is the DESI DR3 release in 2027 Q2, which will activate the pre-registered Blind-Conditional Null-First (BCNF) protocol on the six falsifiers fixed in §5. The BCNF flow — blinded data ingestion, null-first chi-square evaluation, then conditional unblinding only after the null gate fixes its sign — is documented in plan v3 §4.3 and will be executed without modification of the gates or thresholds frozen at L591/L596 sync. A paradigm-shift verdict is reserved for the case where the DR3 evaluation co-confirms the background and growth pillars within the pre-registered tolerances; otherwise, the framework remains in its present phenomenology status. The DR3 run will not be initiated before the public release (per the CLAUDE.md DR3 rule), and the run_dr3.sh wrapper is held in a frozen state until then to prevent premature execution against absent DR3 directories.

### §7.2 multi-session 의무 (L599 / L615 외부 검증)

All priori-style derivations referenced in this paper are subject to the multi-session obligation established in L599 and re-confirmed in L615 — every claim of the form "derived from the 6-axiom SQT structure" must be reproduced across independent sessions with independent team configurations before it is admitted into §3 or §4. Single-session a priori derivations are explicitly excluded from the claims_status table; this is one reason the four priori candidates examined during Phase 31–40 were withdrawn rather than promoted, and the document records this withdrawal as a normal outcome of the protocol rather than as a defect. External-validation requests (e.g., independent re-run of σ₀ dimensional uniqueness or a₀ PASS_MODERATE gate) are routed through the multi-session pathway, with team composition and seed records archived alongside each session result.

### §7.3 paradigm shift conditional (Phase 31–40 trial, 박탈 risk 정직)

Whether the framework can advance from "falsifiable phenomenology" to a paradigm-level claim depends on the post-DR3 outcome and on continued survival of the surviving pillars under independent re-runs. The Phase 31–40 trial demonstrated that priori-status candidates can and do lose their priori grade upon stricter scope or multi-session re-evaluation — four such withdrawals occurred during this period — and the same risk applies to the present a₀/σ₀ results. The document therefore states the paradigm-shift conditional honestly — it is contingent, time-bound (DR3 window), and subject to further withdrawal — and avoids any language that would frame the current framework as "unified," "zero-parameter," or "a priori-derived." The outlook closes by reaffirming that the internal OR-gate (formerly framed as a "PRD Letter target") remains an internal acceptance gate uncoupled from any external publication target.

## §8 Reproducibility (2 paragraphs, 250–300 자 each)

### §8.1 verify_*.py (L637 7/7 PASS) + Docker + expected_outputs JSON

Reproducibility is operationalised through the seven verify_*.py scripts catalogued in L637, all of which currently report PASS (7/7) on the reference environment; each script is paired with an expected_outputs JSON manifest that pins the exact numerical and string fields the verifier compares against, so a downstream reviewer can detect drift without re-reading the analysis code. The full pipeline is shipped inside a Docker image whose base layer fixes Python 3.x, numpy 2.x (with the trapezoid migration noted in the project rules), and the bao_data / sn_data CobayaSampler snapshots used throughout §3–§5; the image entrypoint runs the seven verifiers in declared order and writes a PASS/FAIL summary that mirrors the L637 7/7 result. expected_outputs JSON files are versioned alongside the verifier scripts so that any change in gate thresholds (e.g., post-DR3 BCNF re-calibration) is recorded as a JSON diff rather than as a silent code edit.

### §8.2 OSF DOI workflow + GitHub release (preprint 단계만)

Long-term archival follows an OSF DOI workflow tied to the GitHub release tag for the preprint snapshot — the DOI is minted once at preprint deposition, and the release tarball includes the Docker image digest, the seven verifier scripts, the expected_outputs JSON manifests, and the frozen DR3 BCNF wrapper. The OSF / GitHub release pairing is restricted to the preprint stage; permanent submission-stage archival is explicitly not performed in this revision, in keeping with the L591/L596 policy that external-submission artefacts are out of scope for the current phenomenology framework. Any future revision that updates the verifiers, expected_outputs, or Docker base layer will be released under a new DOI rather than by overwriting the existing one, so that the L637 7/7 PASS state and the pre-registered DR3 falsifier definitions remain immutably attributable to this version of the document.

---

## 어휘 가이드 cross-reference

- L591 sync: "통합 이론" / "0 free parameter" / "priori 도출" 영구 금지, fabrication 비율 (≈ 90 %) 명시 의무, 4 priori 박탈 명시.
- L596 sync: "phenomenology framework" 통일 어휘, 외부 출판 표현 → 내부 OR-게이트 치환.
- L635 sync: PASS_MODERATE 등 게이트 어휘 고정, multi-session 의무 (L633 H2) 인용.
- L633 H2: 모든 priori-style 도출은 multi-session 의무.
- L637: verify_*.py 7/7 PASS 상태가 §8.1 의 사실적 근거.
- L639 / L640: §6 / §1–§5 본문 예시와 어휘·범위·한계 preview 일관 유지.

## 8인 Rule-A 의무

§0 abstract 의 정량 결과 표현, §7 의 박탈 risk·DR3 conditional·multi-session 의무 서술, §8 의 재현 절차·OSF DOI 정책은 모두 이론·정책 클레임에 해당하므로 8인 Rule-A 순차 리뷰가 본문 통합 전 의무이다. §8 의 verify_*.py / Docker / expected_outputs JSON 텍스트가 실제 산출물과 일치하는지에 대한 별도 4인 Rule-B 코드 리뷰는 Rule-A 합의 이후 진행한다.

## 정직 한 줄

본 예시 문서는 plan v3 §0/§7/§8 의 어휘·범위·한계 preview 초안이며, 8인 Rule-A 합의 전 어떤 paper / claims_status / 외부 산출물에도 반영되지 않는다.
