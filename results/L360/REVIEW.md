# L360 REVIEW (사전 등록 / 실행 전)

## 한 줄 정직 한국어
아직 실행 전이라 SPARC·DESI·Planck σ_0 사이의 Q_DMAP 값은 측정되지 않았으며, 본 문서는 ATTACK_DESIGN 의 사전 등록판에 불과하다.

## 8인 자율 점검 — 설계 단계 (코드 미작성)
- **D1. 통일 σ_0 정의**: 세 채널이 동일 스칼라를 공유하는지가 핵심. 만약
  SPARC fit 에 들어가는 σ_0 가 우주론 σ_0 와 정의·단위가 다르면 Q_DMAP 자체가
  무의미. → 임베딩 노트 우선 작성 (NEXT_STEP §1).
- **D2. Q_DMAP 가정**: nested MAP 비교는 두 데이터셋 likelihood 가 서로
  독립이라는 가정 필요. SPARC ↔ DESI 는 명백 독립. DESI ↔ Planck 는
  CMB lensing reconstruction 통한 약한 상관 가능성 — compressed shift
  parameters (R, l_A) 단계에서 무시 수준이라고 일반적으로 가정하나,
  보고서에 명시 필요.
- **D3. Non-Gaussian posterior**: σ_0 가 SPARC 에서 highly non-Gaussian (long
  tail) 일 가능성. Q_DMAP 의 robustness 우위가 여기서 발휘. profile
  likelihood 와 교차검증.
- **D4. Prior 영향**: σ_0 사전이 너무 좁으면 MAP 이 boundary 에 박혀 Q_DMAP
  과소추정. wide & flat σ_0 prior + boundary 박힘 검사 (L4 재발방지).
- **D5. 합격선 선등록**: Q_DMAP > 5 KILL, 2~5 WATCH, <2 PASS 를 코드 작성
  전에 고정. 사후 임계 조정 금지.

## 잠재 위험 (사전)
- SPARC σ_0 fit 이 baryon 분포 (M/L) 와 강하게 degenerate → marginalize 후
  effective σ_0 prior 가 다중모드일 위험. profile likelihood 필수.
- DESI DR2 BAO 만으로는 σ_0 제약이 약해 MAP 이 잘 정의되지 않을 가능성 →
  BAO+RSD fσ8 결합 필수 (DESI fσ8 LRG/ELG bins).
- 삼중 joint ABC 가 어떤 한 페어보다 더 큰 tension 을 보일 수 있음
  (Raveri-Doux 의 "hidden tension"). 결과에 모두 보고.

## 검토 미수행 사항 (코드 작성 시 4인 코드리뷰 대상)
- σ_0 임베딩 모듈 단일 진실원
- MAP optimiser (Nelder-Mead 경계 박힘 방지: tight box + smooth penalty)
- Q_DMAP 함수 (negative radicand → 0 처리)
- 부트스트랩 시드 고정 / 재현성

## 판정
- **현 단계**: GO for implementation (설계 무결, 사전 등록 완료).
- **다음 게이트**: Pair 1 (SPARC↔DESI) Q_DMAP 산출 후 8인 재검토.
