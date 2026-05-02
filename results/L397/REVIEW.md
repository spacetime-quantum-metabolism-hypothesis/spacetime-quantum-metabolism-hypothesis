# L397 — 4인 review (F1–F9 generation script outline + caption)

## 평가
- L318 spec 을 변경 없이 승계, 각 figure 에 (input source, script outline, caption final) 3종 세트로 묶은 구조 — paper 제출 직전 실행 단계로 직결 가능.
- caption 9종 모두 "지지/기각 또는 falsifiability window" 문장을 포함 — JCAP 정직성 기준 부합.
- 데이터 source 요약 표가 OK / partial / MISSING 으로 분류되어 blocker (F1 L319, F8 IC aggregator) 가 명시적.
- Wong palette + linestyle 차이 + hatch (F8) 로 grayscale 안전성 일관 적용.
- 모든 caption 에 `[Source: ..., script: ...]` 태그 강제 — 재현성 규약 준수.

## 보강 권고
- **F1**: caption 에 "이론 band σ_0 = 4π G t_P" 라고 명시했으나 이는 plot 수식 표시이지 지도 위반 아님 (L160 axiom 에서 이미 공개된 정의). 단, paper 본문에서 axiom 으로 도입 후 figure 인용해야 한다는 순서 강조 필요.
- **F2**: 3 galaxy 선택 명단 (e.g. NGC 3198, DDO 154, UGC 2885 류) 을 caption 에서 명시하고 selection criterion 을 1-line 으로 추가 — peer review 에서 cherry-pick 의심 차단.
- **F3**: H_0 두 band (Planck/SH0ES) 를 동시에 보이는 선택은 Hubble tension 인정 + SQMH 가 그 안에 들어감을 정직히 보여주는 강점. caption 에 "SQMH does not resolve H₀ tension" 한 문장 추가 권고.
- **F5**: σ/H = 5×10⁻² 가 z ≲ 1 CMB 외 제약과 합치하는지 caption footnote 로 출처 (Saadeh+2016 등) 명시 권고.
- **F8**: AICc k_SQMH = {N} 자리에 실제 자유 파라미터 수 (예: σ_0, n₀μ, ...) 를 figure 생성 직전에 채워야 함 — placeholder 잔존 위험.
- **F9**: "approximate" 명시는 정직하나 reviewer 가 "그럼 이 figure 를 paper 결론으로 쓸 수 없지 않냐" 반박 가능 — caption 마지막에 "for guidance only, not used in current evidence claims" 한 문장 명시 권고.

## blocker 우선순위
1. **F1 (L319 σ_0(env) aggregator)** — paper 의 핵심 universality claim 의 시각 증거. 미해결 시 F1 자체를 부록 또는 "future work" figure 로 강등 필요.
2. **F8 (joint IC aggregator)** — model comparison 의 정량 근거. 부재 시 본문에서 "ΔIC" 인용 불가, T4 evidence summary 와 일관성 깨짐.
3. **F9 (ETC 1σ)** — 수기 입력으로 비교적 빠르게 보충 가능하나 출처 링크 누락 위험.

## 위험 재확인
- caption 의 falsifiability 문구 ("> 3σ deviation would falsify") 는 paper Limitations 섹션과 직접 cross-ref 되어야 over-claim 이 아님 — TeX 단계에서 \cref{sec:limitations} 강제.
- F2, F4 의 grayscale 안전성: errorbar marker 와 line dash 가 작은 figure 폭 (86 mm) 에서 구분 가능한지 PDF preview 단계에서 재확인.
- F8 hatch pattern 은 matplotlib 에서 PDF 저장 시 화면과 다른 밀도로 렌더링되는 known issue — PDF 직접 확인 필요.
- script outline 이 "의사코드" 수준이므로 실제 코딩 단계에서 spec 누락 시 재작성 비용 발생 — 각 fig 첫 commit 시 outline → 코드 매핑 commit message 권고.

## 정직 한 줄
본 review 는 outline + caption draft 의 적정성만 판정하며 F1/F8 upstream aggregator 가 없는 한 9 figure 일괄 생성은 불가능하다.
