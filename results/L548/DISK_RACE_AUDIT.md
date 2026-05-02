# L548 R10-DA — Disk Race Audit (synthesis vs audit timing)

> **저자**: 단일 분석 에이전트 (8인/4인 라운드 *없음* — disk forensics only)
> **임무**: L499/L505/L511/L518/L521/L537/L540 의 "빈 디렉터리 / 부재" 정직 보고와, 다음 wake 에서 동일 디렉터리에 산출물이 발견되는 패턴의 *원인 진단* + *재발방지 권고*.
> **방법**: synthesis `.md` 의 mtime 과 sibling audit 산출물의 mtime 을 직접 비교 (`stat -f %Sm`).

---

## 1. 결론 한 줄 (정직)

**"빈 디렉터리" 보고는 거짓이 아니라 *synthesis 시점의 사실* 이었다 — 그러나 그 사실은 *동일 phase 의 audit 에이전트들이 아직 끝나지 않은* race 상태였고, synthesis 가 먼저 종료되어 디스크에 박혔을 뿐이다. 즉 모든 사례가 "synthesis-runs-before-siblings-finish" race condition.**

---

## 2. mtime forensics — race 직접 증거

다음 표는 synthesis `.md` 의 mtime (= synthesis 종료 시각) 과, 그 synthesis 가 "부재 / 빈" 으로 보고한 sibling 디렉터리에 *현재 존재하는* 산출물의 mtime 을 함께 나열한다. **synthesis mtime 이 sibling mtime 보다 앞서면 race 확정**.

| Synthesis | mtime (종료) | "부재" 보고 sibling | sibling 산출물 mtime | Δt | race? |
|---|---|---|---|---|---|
| L499/PHASE1_SYNTHESIS | 01:17:07 | L500 DWARF_INVESTIGATION | 01:21:52 | +4m 45s | **YES** |
|  |  | L501 RAR_PREREG | 01:20:45 | +3m 38s | **YES** |
|  |  | L502 HIDDEN_DOF_AICC | 01:23:05 | +5m 58s | **YES** |
|  |  | L503 UNIVERSALITY | 01:21:20 | +4m 13s | **YES** |
|  |  | L504 PAPER_UPDATE_PLAN_v6 | 01:22:08 | +5m 01s | **YES** |
| L505/PHASE2_SYNTHESIS | 01:21:10 | L506 CASSINI_ROBUSTNESS | 01:22:49 | +1m 39s | **YES** |
|  |  | L507 BBN_CROSS_EXP | 01:21:51 | +0m 41s | **YES** |
| L511/PHASE3_SYNTHESIS | 01:24:40 | L512 REVIEW | 01:25:29 | +0m 49s | **YES** |
|  |  | L513 REVIEW | 01:26:05 | +1m 25s | **YES** |
|  |  | L515 REVIEW | 01:27:34 | +2m 54s | **YES** |
| L518/SYNTHESIS_v7 | 01:29:06 | L515 REVIEW | 01:27:34 | −1m 32s | no (already done) |
|  |  | L519, L520 | (현재도 산출물 1, ts 01:27–01:28) | small | borderline |
| L521/SYNTHESIS_v8 | 01:29:27 | L523, L524 | 01:35–01:36 | +6m | **YES** |
| L537/PHASE8_SYNTHESIS | 17:43:33 | L535 HYBRID_AG | 17:43:40 | +0m 7s | **YES (razor)** |
|  |  | L536 NEW_PRIORI | 17:43:49 | +0m 16s | **YES (razor)** |
| L540/SESSION_FINAL_v2 | 17:48:42 | L538 REVIEW | 17:47:37 | −1m 05s | no |
|  |  | L539 REVIEW | 17:49:32 | +0m 50s | **YES** |

**해석**: 7개 synthesis 중 **6개** (L499, L505, L511, L521, L537, L540) 가 적어도 한 sibling audit 보다 *먼저* 종료되어 "부재" 를 보고했다. L537 의 razor (Δt = 7~16 초) 는 거의 동시 실행된 multi-agent batch 의 typical race window.

L540 본문이 이미 자가 인정한 표현: *"L537 EXEC PHASE8_SYNTHESIS.md (단, 그 시점에 L533–L536 빈 보고 — 사후 채워짐)"* — race 패턴이 한 번은 본문에 직접 기록되었다.

---

## 3. Phase 배치 mtime 클러스터 (병렬 실행 추정)

| Phase batch | mtime 범위 | 구성 |
|---|---|---|
| Phase 1+2+3 (L491–L515) | 2026-05-02 **01:16–01:30** (~14 min) | 약 25 디렉터리 |
| Phase 6 (L519–L524) | 01:27–01:36 (~9 min) | 6 디렉터리 |
| Phase 7+8+9 (L527–L539) | 17:37–17:49 (~12 min) | 13 디렉터리 |

각 batch 내부에서 디렉터리는 *동시-launch* 된 것으로 보이며 (ts spread <15 분), synthesis 도 **batch 내부**에 launch 되어 sibling audit 의 종료를 기다리지 않고 즉시 디스크 스냅샷을 찍었다.

---

## 4. 빈-디렉터리 패턴 카탈로그 — task 유형별

| 유형 | 사례 | 특징 | race 빈도 |
|---|---|---|---|
| **A. Phase synthesis** (R-Phase 종합) | L499, L505, L511, L518, L537 | 동일 Phase audit 의 직후 launch — sibling 와 race | **6/7 (86%)** |
| **B. Strategy synthesis** (전략 / final) | L521, L540 | 누적 Phase 종합 — 후행 audit 와 race | 2/2 |
| **C. Meta-paper edit** | L516, L538, L539 | paper/base.md 수정 트랙 — disk-absent 자체로 미실행 | (race 아님) |
| **D. 4인 Rule-B review** | L512, L513, L515, L538, L539 | 단일 REVIEW.md 산출 — synthesis 와 race 가능 | L511/L540 와 충돌 |

**A 와 B 가 핵심**: Phase 종합 / 전략 종합은 *audit-종속* 이지만 *audit-병렬* 로 launch 되는 구조. 이 구조 자체가 race 의 근본 원인.

---

## 5. 진단 — *에이전트 실행 vs synthesis 시점 race* 의 근원

1. **병렬 launch 패턴**: Phase batch 가 multi-agent (audit N개 + synthesis 1개) 를 *동시 spawn* 한다. synthesis 에이전트는 sibling audit 가 끝났는지 알 수 없으며, "디스크 검증" 만으로 substrate 존재를 판단한다.
2. **synthesis 가 먼저 끝남**: synthesis 작업 (meta-합성) 은 token budget 이 큰 audit 작업보다 평균적으로 더 빨리 종료된다. mtime 클러스터에서 synthesis ts 가 sibling ts 의 *중앙값보다 앞* 에 위치.
3. **mkdir-only 흔적**: 일부 sibling 은 audit 가 mkdir 만 수행하고 본문 write 직전에 buffer flush 가 지연되어, synthesis 의 `ls` 시점에 빈 디렉터리로 노출된다 (L537 의 L533–L536 razor 사례).
4. **CLAUDE.md "결과 왜곡 금지" 의 정직 의무**: synthesis 에이전트는 race 를 인식하지 못한 채 "빈 디렉터리 → audit 0건" 으로 정직 보고한다. 이 보고는 *synthesis 시점* 에는 사실이지만 *최종 디스크 상태* 와는 어긋난다.

---

## 6. 권고 — 재발방지

### 6.1 즉시 적용 (single-line CLAUDE.md 추가)

> **synthesis 에이전트는 sibling audit 디렉터리가 "빈 / 부재" 일 때 즉시 종합을 시작하지 말고, *최소 60 초 polling × 최대 3 회* 재확인 후에도 비어 있을 때만 disk-absent 으로 확정 보고. 1초 이내 razor race 방지.**

### 6.2 구조적 (Command 작성 시)

- **Synthesis launch 를 audit batch 와 분리**: Phase audit N개 → 모두 종료 확인 → 별도 invocation 으로 synthesis launch. 동시 spawn 금지.
- **Sentinel 파일 사용**: 각 audit 마지막 단계에서 `DONE.sentinel` 작성. synthesis 는 N 개 sentinel 모두 존재할 때만 진행.
- **mtime sanity check**: synthesis 가 "빈" 보고 시 *부모 디렉터리 mtime* 이 self mtime 보다 5분 이내면 race 가능성 명시 (단순 `os.path.getmtime(parent) > self_start_ts - 300`).

### 6.3 보고 체계 (synthesis 에이전트 프롬프트)

- "빈 디렉터리" 보고 시 항상 *3 가지 가능성* 을 명시: (a) 진정 미실행, (b) sibling-still-running race, (c) mkdir-only flush 지연. L537 처럼 razor Δt 가 의심되면 (b)/(c) 를 default 로 추정.
- **사후 검증 의무**: 다음 wake 에 동일 디렉터리 재확인 → 산출물 발견 시 이전 보고를 *amendment* 로 정정. L540 가 한 번 이를 부분 시도 ("사후 채워짐") — 패턴화 필요.

### 6.4 CLAUDE.md 추가 권고 텍스트 (L548 R10-DA 재발방지)

> **L499~L540 disk-race 재발방지**: synthesis 에이전트가 sibling audit 디렉터리를 "빈" 으로 본 시점은 *race 가능* 이다 (L548 R10-DA 확정 6/7 사례). synthesis launch 는 (a) Phase audit 의 명시적 DONE.sentinel 또는 (b) audit batch 종료 후 별도 invocation 후에만 허용. 동시 spawn 으로 synthesis launch 시 razor Δt < 60 s race 발생. "빈 디렉터리" 보고는 사후 wake 에서 반드시 *amendment* 로 재검증.

---

## 7. 본 보고의 한계

- **command 파일 부재**: `commands/` 에 L491+ command 파일이 없어 synthesis launch 시각을 mtime 외 channel 로 검증 불가. command spawn 로그가 있다면 race 확정성이 razor 사례에서 더 강해질 것.
- **buffer flush vs spawn delay 분리 불가**: razor Δt < 30 초 사례 (L537) 가 "audit 가 진짜 늦게 시작" 인지 "audit 가 거의 완료되었으나 write flush 지연" 인지 mtime 만으로 분리 불가. sentinel 패턴 도입 시 이 모호성 해소.
- **단일 에이전트 disk forensics**: 8인/4인 라운드 미실행. 본 보고는 R10-DA 1차 진단이며, 정책 채택 전 Rule-A 8인 라운드로 §6.1/§6.4 텍스트 합의 필요.

---

## 8. 핵심 산출 요약 (5 lines)

1. **race 확정 6/7 synthesis**: L499/L505/L511/L521/L537/L540 가 sibling audit 보다 먼저 종료.
2. **razor case**: L537 가 L535/L536 보다 7~16 초 먼저 종료 — 거의 동시 spawn 의 typical window.
3. **batch 패턴**: Phase 디렉터리 ~14 분 내 cluster 생성, synthesis 가 그 cluster 내부에 launch 되는 구조 자체가 race 원인.
4. **권고 1**: synthesis launch 를 audit batch 와 분리 + DONE.sentinel polling.
5. **권고 2**: CLAUDE.md 에 L548 R10-DA 재발방지 한 줄 추가 (§6.4 텍스트), 8인 Rule-A 라운드 합의 후 적용.
