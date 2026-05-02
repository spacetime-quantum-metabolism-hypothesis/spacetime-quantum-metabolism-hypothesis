# L197 — Information-theoretic justification of Branch B

## 정보 이론적 관점

### Minimum Description Length (MDL)

Branch B = 3 σ_0 values + boundaries (~5 numbers)
Smooth quadratic = 3 coefficients (a, b, c)
*동일 자유도*

### MDL 비교

```
Description complexity:
Branch B 3-regime:
  - 3 σ_0 values (each ~6 bits precision)
  - 2 ρ_c boundaries (each ~6 bits)
  - 2 transition widths (each ~3 bits)
  Total: ~30 bits

Smooth quadratic:
  - 3 coefficients (each ~6 bits)
  - 1 expansion point (each ~6 bits)
  Total: ~24 bits
```

→ Smooth slightly simpler in MDL. But:

### Predictive bits

Branch B *qualitative* prediction (regime structure exists) provides
information beyond just fit values:
- Different physics in different regimes
- Phase transition possibility
- Cluster vs galactic distinct mechanisms

Smooth provides:
- σ continuously varies with ρ
- No phase transitions
- Mass scaling

**This qualitative content is NOT in the bits**. Branch B's "extra
content" is the assertion of *discrete physics*, which is testable
but not in the description.

### Implication for paper

```
Information-theoretic position:
"Branch B and smooth σ(ρ) provide statistically equivalent
descriptions of current data. Branch B is selected based on
ITS QUALITATIVE PROPOSITION OF DISCRETE PHYSICS, which is
testable in the future via dSph and intermediate-density
observations."
```

### Reviewer expected response

```
"Acceptable framing. Honest about quantitative equivalence.
Hypothesizes specific physics (regime structure) that's testable.
Score: ★★★½ for theoretical positioning."
```

## 결론

Branch B 의 *information-theoretic 정당화*: 모형의 *실증 비교*에서는
약간 우월 (L192 ΔAICc=26+) 하나, *information content* 자체는 smooth 와
*비슷*. Branch B 의 강점은 *qualitative claim* (discrete physics) 이며,
이는 future test 의 *목표*가 됨.

Paper 의 limitations section 에서 *명시 권고*.
