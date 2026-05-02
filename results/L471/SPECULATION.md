# L471 — Multi-field n & Cluster Dip 자유 추측

작성: 2026-05-01
모드: 자유 추측 (falsifiable 가설 후보 생성). [최우선-1] 준수 — 수식 0줄, 방향만.

---

## 0. 출발점 — 우리가 보고 있는 현상

L46x 시리즈에서 반복적으로 관측된 패턴:
**cluster 환경(고밀도, virialized)에서 SQMH 의 n field 신호가 dip(국소적 약화/소멸)을 보인다**.
지금까지의 단일-field 가정으로는 dip 의 깊이/위치/스케일 의존성이 자연스럽게 떨어지지 않음.

이 SPECULATION 의 핵심 질문:
> **n 이 진짜로 single field 인가?**
> 만약 n 이 두 개(또는 그 이상) component 의 합성이라면, cluster 에서 dip 은
> "약해지는" 것이 아니라 "**상쇄(destructive interference)**" 의 결과일 수 있다.

---

## 1. Single field n 가정이 강요하는 것

지금 우리가 single-field n 으로 묶어서 부르는 양은 사실상 다음을 모두 동시에 떠안고 있다:

- 우주 가속의 source (배경 우주론 채널)
- 대사공리 L0/L1 의 미시 drift 항 (시공-생성률)
- 클러스터 내부의 환경 의존 신호 (L46x dip)
- (시도된) Cassini-safe 한 PPN 행동

하나의 scalar 가 이 모든 역할을 동시에 수행하려면 **결합 구조와 mass 스케일이 동시에 두 개 이상 필요**.
즉 single-field 라는 가정 자체가 *암묵적으로 multi-scale* 을 강제하고 있고,
그 강제가 cluster dip 같이 "왜 거기서만 약해지는가" 를 외부 fitting parameter 로 떠넘기게 만든다.

이 떠넘김을 거두고, **자유도 분리** 를 가설로 올린다.

---

## 2. 가설 H1 — n = n_a + n_b (이중 component)

**방향만**: n 을 두 component 로 분해.

- 한 component 는 *long-range / cosmological* 채널: 배경 우주 가속·저 z 영역에서 지배.
- 다른 component 는 *short-range / environmental* 채널: 고밀도(cluster, halo core) 에서 지배.

두 component 가 cluster 에서 **위상이 반대(혹은 부분적으로 반대)** 로 드러나면,
관측되는 합성 신호는 그 영역에서 *국소적으로 상쇄* — 이것이 dip 의 정체.

falsifiable 신호:
- dip 의 깊이가 cluster mass / virial radius / surrounding void density 에 *비단조* 의존.
- dip 위치가 두 component 의 mass 비에 의해 결정된 *공명 스케일* 근방에 정렬.
- low-z 와 high-z cluster 에서 dip 모양이 *같은 스케일이 아닌 상대적으로 redshift 한* 형태로 이동.

만약 dip 이 단순한 screening (Vainshtein/chameleon 류) 이면 깊이는 항상 단조.
관측이 비단조 이면 single-field screening 은 즉시 falsified, multi-field 가설로 무게 이동.

---

## 3. 가설 H2 — Bose-Einstein 류 두 mode 간섭

**방향만**: SQMH 가 깔고 있는 시공 substrate 가 macroscopic occupation 의 보존자(boson-like) 라면,
"단일 ground mode" 가 아니라 *두 개 이상의 macroscopically populated mode* 의 중첩이
일반적 상태일 수 있다.

이 가설의 매력:
- BEC 두-component 계에서 알려진 *Josephson-like 위상 동역학* 이
  cluster 같은 deep-potential well 에서 두 mode 의 *상대 위상* 을 강제로 정렬.
- 정렬 방향에 따라 합성 진폭이 cluster 안쪽으로 갈수록 *증폭(constructive)* 될 수도, *상쇄(destructive)* 될 수도 있다.
- L46x 가 일관되게 dip(증폭이 아니라 상쇄)을 본다는 것은,
  potential well 이 두 mode 를 *반위상으로* 정렬하는 채널이 존재함을 시사.

falsifiable 신호:
- dip 가 일정 cluster mass 임계 이하에서 사라지거나 **부호 반전**(작은 halo 에서 미약한 *bump*).
- 두 mode 의 chemical potential 차이에 해당하는 *간섭 fringe* 가 cluster 외곽 splashback radius 근처 잔류 신호.
- 시간 의존성: 두 mode 가 정확히 degenerate 가 아니면 cluster 중심에서 dip 깊이가 *느린 oscillation* 을 가져야 함.
  단일 cluster 에서 시간 oscillation 검출은 비현실적이나, **cluster 표본의 통계적 dip 분포** 가
  정적 screening 예측보다 *더 넓은 분산* 을 가져야 한다 (각 cluster 의 위상이 무작위).

---

## 4. 가설 H3 — coherent vs incoherent 의 환경 의존 전이

**방향만**: 두 component / 두 mode 가 **언제나** 위상 결맞음(coherent) 일 필요는 없다.

- 우주 평균 영역(low density): 두 채널이 *incoherent* — 합성은 단순한 power 합 (dip 없음).
- cluster 깊은 영역(deep well): 환경이 두 채널을 동기화 — *coherent* — 위상 정렬 결과로 강한 dip.
- 중간 영역: 부분 결맞음 — dip 이 부드럽게 켜지는 *전이대역*.

이 경우 dip 은 "깊이의 문제" 가 아니라 "**결맞음 전이의 문제**".
즉 cluster 안으로 들어갈수록 dip 이 *급격히* 켜지는 *threshold-like* 행동을 예측한다.

falsifiable 신호:
- dip 의 시작이 *연속이 아니라 step-like* 한 cluster radial profile 에서 켜짐.
- threshold radius 가 cluster 의 *가상 온도(virial temperature)* 또는 *velocity dispersion* 의 단순 monotone 함수로 정리되어야 함.
- 이 threshold 가 single-field screening 이론의 *어떤 자연 스케일과도 일치하지 않는다* 는 점이 결정적 차별 신호.

---

## 5. 가설 H4 — 자유로 더 멀리: n 은 *연속체* 일 수도

**가장 자유로운 추측**: 두 component 도 모자랄지 모른다.
n 이 *연속 spectrum* 을 가진 field tower 라면, cluster 환경이
spectrum 의 *특정 부분만 선택적으로 활성화* 하는 envelope 역할을 한다.

- low-density 영역: 거의 전 spectrum 이 활성, 신호는 평균화되어 매끈함.
- cluster: 좁은 band 만 활성 — 그 band 의 위상 구조가 그대로 노출되어 dip / fringe / ringing.

이 그림에서 dip 은 결국 **cluster-induced spectral filtering**.
이는 multi-field 보다 더 큰 자유도지만, 만약 cluster 표본에서
dip 모양이 *cluster 의 어떤 환경 변수의 함수로 *연속적으로 변형* 한다면*
(단순 on/off 가 아니라 *형태 자체가 미끄러진다면*) H4 가 H1/H2 보다 우세.

---

## 6. H1~H4 를 가르는 결정 실험 (방향만)

다음 측정 중 어떤 패턴이 나오느냐가 가설을 분리한다.

| 관측 | 단일 field screening | H1 (이중 component) | H2 (BEC 간섭) | H3 (결맞음 전이) | H4 (연속체) |
|---|---|---|---|---|---|
| dip 깊이 vs cluster mass | 단조 | 비단조 | 비단조 + 부호 반전 가능 | step-like | 연속 변형 |
| dip 의 cluster 외곽 fringe | 없음 | 약함 | **있음** | 없음 | 있음 (다중) |
| 표본 통계 분산 | 좁음 | 중간 | **넓음** | 좁음 (전이 후) | 매우 넓음 |
| 작은 halo 에서 부호 | 약화만 | 약화 | **반전 가능** | off | 약한 잔존 |
| 형태 변형 | 자기 닮음 | 두 종 mix | fringe 변형 | on/off 만 | **연속 변형** |

볼드체는 그 가설의 *고유 시그니처*. 다른 가설로는 자연스럽게 나오지 않는 항.

---

## 7. 이 추측이 SQMH 본체에 미치는 함의 (방향만)

- 만약 H1 이 채택되면, 지금 single n 이 떠안고 있던 "배경 우주론 + 환경 신호" 의 이중역할이 *깨끗하게 분리* 되어 L0/L1 대사공리 도출 경로가 단순해진다.
- 만약 H2 가 채택되면, SQMH 의 시공 substrate 가 단순한 scalar 가 아니라 *macroscopic quantum 상태* 라는 그림이 강제 — 이는 J(시공생성률) 의 통계적 기원을 *quantum coherence* 로 묶는 새 이론 채널을 연다.
- 만약 H3 가 채택되면, cluster 는 단순한 "강한 중력장" 이 아니라 *위상 동기화기(phase synchronizer)* — 이는 splashback / cool-core 같은 클러스터 자체 현상학과의 cross-correlation 을 새로 요구.
- 만약 H4 가 채택되면, n 은 사실상 *field 가 아니라 medium* — SQMH 의 입자 vs 시공 이분법을 다시 검토해야 한다.

이 네 갈래 중 어느 쪽이든, 지금까지 cluster dip 을 single-field 로 fitting 하던 모든 결과는
**해석을 잠정 보류** 해야 한다 (값은 살아있되, 그 값이 가리키는 물리량이 다른 것을 가리킬 수 있음).

---

## 8. 다음 행동 후보 (제안만, 지시 아님)

- L472: H1~H4 각각에 대해 *fitting-free* 한 정성 패턴(부호, 단조성, fringe 유무)만으로 cluster 표본을 재집계.
  값을 맞추지 말고 *어느 가설이 패턴을 통과/불통과 시키는지* 만 본다.
- L473: BEC 두-mode 류 toy 의 *형식 구조* 가 cluster potential 안에서 어떤 위상 동역학을 가지는지를
  팀 자율 분담으로 독립 도출. (Command 에 수식 한 줄도 금지 — [최우선-1].)
- L474: H3 의 결맞음 전이 가설을 검증할 cluster radial 표본 설계.
  threshold 가 자연 스케일 어떤 것과도 무관하다는 negative 검증이 더 강한 신호.

---

## 9. 한 줄 요약 (한국어)

cluster dip 은 n 이 "거기서만 약해진" 결과가 아니라, **두(이상의) component 가 그 환경에서 위상이 어긋나 서로 지워지는 결맞음 간섭의 흔적** 일 수 있다.
