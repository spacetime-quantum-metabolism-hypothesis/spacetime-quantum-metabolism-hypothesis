# L368 — NEXT STEP (Sec 6 14-row 통합)

## 1. 논문 Sec 6 본문 텍스트 초안

> **Section 6. Limitations and Honest Disclosure**
>
> We acknowledge fourteen limitations of the present analysis, organized in four
> tiers: (i) four *permanent structural* limits inherent to a background-only
> approach; (ii) six issues raised in the L322-L330 global audit; (iii) two
> follow-on items from the L332-L340 attack loops; and (iv) two additional
> structural limits surfaced by the L342-L367 accumulation. Each row is mapped
> to a concrete mitigation status (structural / acknowledged / downgraded /
> plan / OPEN). No limitation is hidden in supplementary material.

(이후 Table 6.1 - 14행, ATTACK_DESIGN.md §3 그대로 삽입)

---

## 2. 통합 체크리스트

- [ ] Sec 6 표 12행 → 14행 교체 (LaTeX `\begin{tabular}` 갱신)
- [ ] 표 캡션: "Fourteen acknowledged limitations (4 permanent + 6 L322-L330 + 2 L332-L340 + 2 L342-L367)"
- [ ] Sec 6 본문 첫 단락에 "fourteen limitations" 명시
- [ ] Abstract 의 "honest disclosure" 문구는 14행으로 일관
- [ ] L341 SYNTHESIS_255 의 "12행" 카운트는 본 loop 에서 14로 supersede — 인용 시 L368 명시
- [ ] Row 13 (cosmic-shear) 은 Sec 5 BMA 표 옆에 "S_8 channel not fit" footnote
- [ ] Row 14 (DR3 blind) 은 Sec 7 future work 와 cross-reference (P17 pre-reg)

---

## 3. JCAP acceptance 영향

- 14행 정직 disclosure → reviewer 신뢰 +.
- L341 추정 90-94% → L368 추정 **89-93%** (-1% net: 정직 +0.5%, 격하 -1.5%).
- PRD Letter 진입 조건 (Q17 완전 OR Q13+Q14) 여전히 미달, 변동 없음.

---

## 4. 후속 loop 권고

1. L369: 14행 표를 LaTeX `paper/sec6_limitations.tex` 에 직접 반영, diff commit.
2. L370+: row 13 cosmic-shear DES-Y3 chi2 직접 계산 시도 (hi_class 또는 CLASS_EFT).
3. L371+: row 14 DR3 pre-reg 문서 OSF upload draft 작성.

---

## 5. 한 줄

> 14-row limitations table 정직 disclosure — 격하 회피용 hedging 없음, 신규 2행 (cosmic-shear, DR3-blind) 영구 인정.
