# refs/l8_kill_criteria.md — L8 Kill/Keep 기준 (실행 전 고정)

> 작성일: 2026-04-11. L8 실행 전 고정. 변경 금지.

---

## KILL 조건

| ID | 조건 | 결과 |
|----|------|------|
| **K31** | A12 역유도 실패: erf형태가 SQMH ODE 어떤 극한에서도 chi²/dof > 10 (8인 수학적 판정) | A12는 현상론 proxy 확정. §2에서 이론 연결 주장 금지 |
| **K32** | C11D 역유도 실패: CLW 자율계에서 n̄=f(x,y) 변수 치환 존재하지 않음 (8인 판정) | C11D와 SQMH의 동형성 주장 금지. 현상론 수준 유지 |
| **K33** | C28 역유도 실패: RR 보조장 V 방정식과 SQMH dn̄/dt 방정식 동형 없음 (8인 판정) | C28는 독립 이론 확정. SQMH 연결 주장 금지 |
| **K34** | K31+K32+K33 모두 발동: 전면 역유도 실패 | §8에 "역유도 시도 실패, 현상론 한계" 기재. L8 이론 채널 종료. |
| **K35** | 역유도 성공했으나 8인팀 "사후 합리화" 판정: 새 예측 없음, 데이터 사후 맞춤만 | 성공 클레임 철회. "형태 유사" 수준으로 격하. |

---

## KEEP 조건

| ID | 조건 | 달성 시 |
|----|------|---------|
| **Q31** | A12 역유도 부분 성공: SQMH ODE 수치 해 ↔ erf proxy chi²/dof < 1.0 (z=0~2.5) | §2 A12 이론 연결 문장 추가. "erf emerges from SQMH homogeneous ODE" |
| **Q32** | C11D 역유도 성공: n̄=f(x,y) 변수 치환 존재 + σ_eff 역산 ≈ 4πGt_P (10% 이내) | Q21 달성. PRD Letter 이론 조건 충족. L7-P 즉시 실행 트리거 |
| **Q33** | C28 역유도 부분 성공: V ↔ n̄ 구조 동형 수학적 확립 OR n̄_eff σ_eff 역산 일치 | §2 각주 추가. "RR auxiliary field isomorphic to SQMH n̄" |
| **Q34** | Q32 달성 후 PRD Letter §2 완성: C11D를 SQMH 장 이론적 실현으로 서술 | PRD Letter 투고 조건 충족 |
| **Q35** | Q31+Q33 동시 달성 (A12+C28): 복수 후보에서 SQMH 구조 출현 | JCAP §2 "L8 역유도 분석" 섹션 추가 |

---

## 언어 규칙 (L7 승계)

| 상황 | 허용 | 금지 |
|------|------|------|
| 역유도 성공 | "X contains a sector isomorphic to SQMH" | "X is derived from SQMH" |
| σ_eff 일치 | "σ_eff consistent with 4πGt_P" | "σ = 4πGt_P is proven" |
| 수치 일치 | "numerically consistent at < X%" | "confirmed", "proven" |
| 인과 방향 | 후보 → SQMH 구조 발견 | SQMH → 후보 유도 (역전 금지) |

---

## 판정 수준 정의

| 수준 | 조건 | 해당 keep |
|------|------|---------|
| 1 (수치 일치) | chi²/dof < 1.0 (E²(z) 비교) | Q31 |
| 2 (구조 동형) | 변수 치환 존재 + kernel 동형 | Q33 |
| 3 (파라미터 일치) | σ_eff = 4πGt_P (10% 이내) | Q32 → Q34 |

---

*고정 일자: 2026-04-11. 이후 수정 금지.*
