# L459 — CITATION.cff + Zenodo metadata

날짜: 2026-05-01
독립 세션 (L459).

## 산출물

- `/CITATION.cff` — Citation File Format v1.2.0, Zenodo DOI 호환 schema.
- `/.zenodo.json` — Zenodo deposit metadata (upload_type=software, MIT, eng).
- `/results/L459/REVIEW.md` — 본 문서.

## 핵심 필드

| 필드 | 값 |
|---|---|
| title | "SQMH — Spacetime Quantum Metabolism Hypothesis: BAO/SN/CMB/RSD joint analysis and SQT reconstruction" |
| authors | Blu (genesos@gmail.com), Independent researcher |
| license | MIT |
| version | L459-pre |
| publication_date | 2026-05-01 |
| DOI | `10.5281/zenodo.PLACEHOLDER` (Zenodo deposit 후 교체) |
| upload_type | software |
| keywords | cosmology, DESI DR2, BAO, DESY5, CMB, RSD, coupled quintessence, SQMH, SQT, negative result, Bayesian evidence, MCMC |

## placeholder DOI 명시

CITATION.cff `identifiers[0].value` 와 `.zenodo.json.doi` 두 곳에 동일하게
`10.5281/zenodo.PLACEHOLDER` 로 기재. Zenodo 첫 deposit 직후 concept DOI 로
일괄 교체 필요 (sed 한 줄로 가능). `.zenodo.json.notes` 에도 교체 지침 명시.

## 정직 한 줄

본 세션은 metadata 파일 생성만 수행했으며, Zenodo 실제 deposit 또는 DOI 발급은 하지 않았다 — placeholder DOI는 반드시 첫 release 시점에 실제 값으로 교체해야 한다.
