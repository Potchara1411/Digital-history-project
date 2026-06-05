# From the AI Winter to the ChatGPT Explosion

A computational history of how "artificial intelligence" has been discussed in
books and news media from 1990 to 2023. The analysis combines two complementary
corpora to trace both a **vocabulary shift** (AI → machine learning → AI) and an
**attention explosion** (the post-2015, and especially post-ChatGPT, surge in
news coverage).

## The figure

Running the script produces a single three-panel figure
([figures/ai_discourse_final.png](figures/ai_discourse_final.png)):

1. **Google Ngram** — frequency of *"artificial intelligence"* vs *"machine
   learning"* in books (1990–2019). Shows the 1990s "AI Winter" decline and the
   point (~2013) where "machine learning" overtakes "artificial intelligence".
2. **Media Cloud** — volume of news articles mentioning AI (2010–2023). The
   ChatGPT-era years (2022+) are highlighted in red.
3. **Media Cloud** — AI's *share* of all news coverage, normalising for the
   overall growth in news volume. Peaks sharply in 2023.

## Data sources

| Source | File | Coverage | Notes |
|--------|------|----------|-------|
| Google Books Ngram | `data/ngram_ai_ml_1990_2019.csv` | 1990–2019 | Frequency as a fraction of all bigrams; multiplied by 1e6 in the chart for readability. |
| Media Cloud (Harvard/MIT) | `data/mediacloud_ai_2010_2023.csv` | 2010–2023 | `count` = articles mentioning AI; `ratio` = count ÷ total articles that year. 1,600+ global English-language sources. |
| GDELT | `data/gdelt_results.csv` | 2010–2023 | **Evaluated and rejected** — see below. Kept for transparency. |

> **TODO — confirm provenance before submitting.** For full reproducibility,
> record the exact query strings and the date each dataset was accessed:
> - Ngram: corpus used (e.g. *English 2019*), smoothing setting, case sensitivity.
> - Media Cloud: the exact query, collection/source list, and export date.

### Why GDELT was excluded

GDELT's AI-related `event_count` jumps from **347 (2013)** to **52,830 (2014)**
to **3.9 million (2015)** — a ~10,000× increase in two years. This is not a real
signal of AI discourse growing; it reflects GDELT 2.0's massive source-coverage
expansion in February 2015. Because the early years are not comparable to the
later ones, GDELT is unusable as a longitudinal trend, so the news-volume panels
use Media Cloud instead. The raw GDELT export is retained in `data/` so this
decision can be audited.

## Reproducing the analysis

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python ai_final.py
```

The script resolves all paths relative to its own location, so it can be run
from any working directory. Output is written to `figures/`.

## Project structure

```
.
├── ai_final.py        # the analysis + figure generation (single source of truth)
├── data/              # source datasets (CSV)
├── figures/           # generated output (regenerable)
├── requirements.txt
└── README.md
```
