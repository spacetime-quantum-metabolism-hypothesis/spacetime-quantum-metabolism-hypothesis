# L358 REVIEW — dynesty vs emcee multimodal 검출 사전 리뷰

## 정직 한국어 한 줄
dynesty 와 emcee 는 동일 단봉 posterior 에서는 일치해야 하고, 일치하지 않으면 둘 중 하나가 mode 를 놓치고 있다는 뜻이다.

## CLAUDE.md 규칙 준수 체크
- [x] **시뮬레이션 병렬 최우선**: 후보별 subprocess 분리 (L5 재발방지)
- [x] **워커당 스레드 1**: `OMP/MKL/OPENBLAS_NUM_THREADS=1` 강제
- [x] **dynesty 3.0.0 rstate**: `np.random.default_rng(seed)` 사용
- [x] **chi² sentinel 금지**: None/nan → `-np.inf` (L4 재발방지)
- [x] **`_jsonify` 변환기**: `np.bool_/np.float_` 직렬화 방지 (L4 재발방지)
- [x] **emcee 시드**: `np.random.seed(42)` + walker 초기화 시드 (L4 재발방지)
- [x] **역할 사전 지정 금지**: 4인 코드리뷰 자율 분담
- [x] **이론 도출 아님**: 본 작업은 sampler 검증, 새 이론 도입 없음 → 최우선-1 비해당

## 방법론 사전 점검

### 1. dynesty 가 emcee 보다 multimodal 에 강한 이유
- nested sampling 은 likelihood contour 를 안쪽으로 압축. 떨어진 두 mode 가 각자 contour 안에 들면 bounding ellipsoid 가 자동 분리
- emcee stretch move 는 walker 쌍 간 직선 보간. 두 mode 사이 valley 에 가로막히면 cross-mode jump 확률 ~0
- dynesty `bound='multi'`: K-means 기반 ellipsoid 분리, mode count 자동 추정

### 2. dynesty 가 놓칠 수 있는 경우
- 두 mode 의 likelihood scale 차이가 매우 크면 (낮은 mode 가 prior volume 만 넓음) live point 를 다 잃음
- enlarge factor 가 작으면 ellipsoid 가 mode 사이 gap 을 못 메우고 mode merging
- prior 가 너무 좁으면 mode 가 prior 밖으로 밀려나 못 봄

### 3. emcee 와 dynesty 가 일치할 때 의미
- 단봉 posterior 라는 강한 증거
- L5 winner (A12, C28) ln Z 안정성 확인
- emcee R̂<1.05 + dynesty modes=1 → "single mode 확정"

### 4. 불일치 시 의미
- emcee 가 한 mode 만 봤다면 → L5/L6 evidence 재계산 필수
- dynesty 가 spurious mode 만들었다면 → enlarge / nlive 재조정
- chi² 함수 자체에 numerical instability 가 있을 가능성 (L33 적분 버그 패턴)

## 위험 등급
- **중간 위험**: L5/L6 evidence 가 단봉 가정에 의존. 만약 multimodal 이면 결론 일부 수정.
- **낮은 위험**: dynesty 자체 버그 가능성은 낮음 (잘 검증된 라이브러리)
- **시간 위험**: 4 모델 × 1 시간 dynesty = 4 시간. 동시 실행 시 CPU 8 코어 점유.

## 합격 기준 검토
- K-L358-1~4 는 모두 정량적, 자동 평가 가능
- Hellinger 임계 0.05 는 보수적; 0.10 까지 허용해도 무방하나 conservative 유지
- ln Z 일관성 0.5 는 dynesty 자체 표준오차 (~0.3) 의 ~2배 — 적절

## 미해결 / 후속
- **K20 (amplitude-locking)** 와 별개 작업. L358 결과 ≠ Q17 진척
- **DR3 데이터 사용 금지**: BAO 는 DR2 만 (L6 재발방지)
- **PRD Letter 진입**: L358 만으로는 불충분. Q17 OR (Q13+Q14) 조건 변동 없음
- multimodal 발견 시 L359 후속, 미발견 시 L5 winner 안정성 보고서로 마감

## 8인 팀 관점
- **이론 정합성**: 본 작업은 sampler 비교이므로 8인 토의 비필수, 4인 코드리뷰 충분 (Rule-B)
- **결과 클레임 시**: ln Z 변동 또는 multimodal 발견은 8인 리뷰 트리거
