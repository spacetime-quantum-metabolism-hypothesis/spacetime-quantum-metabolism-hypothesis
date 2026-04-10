---
description: SQMH 논문 프로젝트 실행 — GitHub 레포 + Python 시뮬레이션 + 논문 섹션
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent, WebFetch, WebSearch
---

# /bigwork-paper

SQMH (Spacetime Quantum Metabolism Hypothesis) 논문 프로젝트를 실행한다.

## 실행 흐름

1. **상태 확인**: `refs/meta.json` + `refs/test-plan.md` 읽어 현재 진행 상태 파악
2. **다음 체크포인트 식별**: test-plan.md에서 미완료 항목 중 첫 번째
3. **Generator 에이전트 실행**: 해당 체크포인트의 구현 작업 할당
4. **Evaluator 에이전트 실행**: 완료된 작업 검증 (CP1, CP3, CP5에서)
5. **KPI 측정**: define.md 기준 진행률 보고
6. **Adjust 기록**: 사이클 종료 시 adjust.md 업데이트

## 핵심 참조
- 가설 원본: `base.md`
- 성공 지표: `.claude/skills/bigwork-paper/refs/define.md`
- 기능 명세: `.claude/skills/bigwork-paper/refs/spec.md`
- 검증 계획: `.claude/skills/bigwork-paper/refs/test-plan.md`
- 의도 파악: `.claude/skills/bigwork-paper/refs/intent.md`

## 에이전트 팀
- Manager: `.claude/agents/bigwork-paper-manager.md` (지시·평가·반영)
- Generator: `.claude/agents/bigwork-paper-generator.md` (구현)
- Evaluator: `.claude/agents/bigwork-paper-evaluator.md` (회의적 검증)

## 규칙
- 자유 매개변수 0개 원칙 절대 위반 금지
- 물리 상수는 `simulations/config.py`에서만 가져옴
- base.md의 자체 한계 평가(Section 10.4, XVI, XVII) 정직하게 반영
- DESI DR3 사전 예측이 최고 우선순위 산출물
