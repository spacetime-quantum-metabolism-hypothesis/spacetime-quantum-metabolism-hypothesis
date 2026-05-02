# L442 NEXT STEP

## 즉시 후속 (별도 LXX 에서 처리)
1. `paper/base.md` 또는 본문 §6/§7 에 STATISTICAL_METHODS_APPENDIX.md 인용 링크 추가
   (본 L442 범위 외).
2. `paper/REFEREE_RESPONSE_v3.md` 의 R3 항목에 본 부록 §A.6 매핑 표 인용 (별도 LXX).
3. `simulations/l442/mock_seeds.txt` 실제 파일 생성 (현재는 부록에서 참조만).
   생성 시 `seed = 100 + i, i = 0..99` 한 줄씩 기록. 본 L442 범위 외.

## 향후 검증 트리거
- Phase-5/L5 winner posterior 가 갱신되면 §A.2.1 의 fixed-θ vs marginalized
  주의 문구가 여전히 유효한지 8 인 재확인 (L6 재발방지 규칙).
- DR3 공개 시 §A.5 의 R-grid sensitivity 를 DR3 covariance 로 재실행
  (단, DR3 스크립트 실행 금지 규칙 준수: 공개 확인 후에만).
- DIC/WAIC 가 발산하는 후보 (multi-modal C28) 발생 시 §A.2 의 nested-sampling
  fallback 절차 호출.

## 결정 단상
본 작업은 메타 부록이므로 추가 시뮬레이션 호출 없음. 후속 인용/링크 작업만 큐.

## 정직 한 줄
NEXT_STEP 은 본 부록을 본문에 묶는 후속 인용 작업과 DR3 시 재검토 트리거만 나열한다.
