# L317 REVIEW — Section 7 (Outlook + Future) 4인 코드리뷰

## 0. 리뷰 대상
- ATTACK_DESIGN.md §1–§7 전부.
- 4인 자율 분담 (역할 사전 지정 없음, 사후 분류).

## 1. 자율 분담 결과
- R1 (timeline 정합성): P15/P17/P21 시기와 미션 윈도 fact-check.
- R2 (정직성 가드): §5 정직성 조항이 §7 와 중복 또는 누락되었는지 검사.
- R3 (이론 미완 노출): §7.6/§7.7 이 reviewer 가 "왜 PRD Letter 아닌가" 답으로 충분한지.
- R4 (재현성): §7.8 GitHub/Zenodo placeholder 와 본 논문 reproducibility 약속 정합성.

## 2. 핵심 발견
- F1 (R1): P15 PIXIE 시기 표기. PIXIE 자체는 NASA Probe-class 후보로 confirmed launch date 없음. "2025–2030" 은 미션 윈도 가정. 본문은 "if approved, late-2020s deployment" 로 약화 필요.
- F2 (R1): P17 DR3 윈도 "2025–2026". DESI DR3 공식 공개는 2026 후반 예상 — "12–18 mo from L317 (2026-05)" 표기는 정합. PASS.
- F3 (R1): P21 LSST WL "2030+". Vera Rubin Y10 stack 기준 2034–2035 가 더 정확. "late-decade" 는 안전 표현. PASS.
- F4 (R2): §4 "DR3 will confirm 금지" 가드는 §5 (L315) 정직성 가드와 중복 — 정합. 누락 없음. PASS.
- F5 (R2): §4 "Companion paper 작성 중 금지" — L6 "PRD Letter 진입 조건 미달" 가드와 동기. PASS.
- F6 (R3): §7.6 β-function "future quantitative" 표현은 충분히 약함. §7.7 V(n,t) "complete derivation" 은 reviewer 가 "그럼 현재 §5.2 Λ origin 1.0000 은 무엇이냐" 로 되묻을 가능성. → 본문에서 "L207 부분 유도 (Q17 partial) → full V(n,t) complete derivation" 으로 명시적 단계 구분 필수.
- F7 (R4): §7.8 Zenodo DOI 미확보. L317 시점에 DOI 발급 안 됨 → 본 논문 submission 직전 (L320+) freeze tag 후 DOI 확보 필요. 지금 placeholder 는 안전.
- F8 (R4): code/data release 에 13-pt DESI 공분산 raw 파일 직접 포함 금지 — CobayaSampler 라이선스. 본문은 "use script + CobayaSampler bao_data 인용" 으로만.

## 3. 권고 수정 (ATTACK_DESIGN 반영 사항)
- C1: §7.3 PIXIE 단락 첫 문장에 "mission-approval contingent" 명시.
- C2: §7.7 첫 문장에 "Q17 partial achievement (L207, ρ_q/ρ_Λ = 1.0000) → full V(n,t) derivation deferred" 단계 구분 명시.
- C3: §7.8 placeholder 에 "DOI to be assigned at submission freeze (planned L320+)" 주석 추가.
- C4: §7.8 데이터 재배포 금지 → "scripts + upstream data citations" 로 표현.

## 4. 합격 판정
- ATTACK_DESIGN §1–§7 골격: PASS (위 C1–C4 반영 조건).
- §4 정직성 가드: PASS (누락 없음).
- 산출물 체크리스트 §6: PASS (Table/Fig 분리 명확).
- Open issue §7: 다음 loop 로 정상 이월.

## 5. 다음 loop 인계
- L318: §7.6/§7.7 합칠지 여부 본문 분량 측정 후 결정.
- L319: §7.8 GitHub 레포 freeze candidate tag 작성.
- L320: Zenodo DOI 확보 + companion paper 8인 재투표.
