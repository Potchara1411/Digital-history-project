# From the AI Winter to the ChatGPT Explosion

A computational history of how "artificial intelligence" has been discussed in
books and news media from 1990 to 2023. The analysis combines two complementary
corpora to trace both a **vocabulary shift** (AI → machine learning → AI) and an
**attention explosion** (the post-2015, and especially post-ChatGPT, surge in
news coverage).

**🔗 Live exhibit: https://potchara1411.github.io/Digital-history-project/**

![The three-panel figure](figures/ai_discourse_final.png)

## The exhibit

The project is presented as a single-page web exhibit ([`index.html`](index.html),
published via GitHub Pages) that walks through the history in three acts:

1. **The Winter and the Rebranding (1990–2013)** — Google Ngram. "Artificial
   intelligence" *declines* through the 1990s AI Winter while "machine learning"
   rises and overtakes it around 2013.
2. **Back into the Light (2012–2021)** — Media Cloud. News coverage climbs from a
   few thousand to tens of thousands of articles a year as deep learning and
   AlphaGo bring AI back to the front page.
3. **The ChatGPT Explosion (2022–2023)** — Media Cloud. AI's *share* of all news
   coverage more than doubles in a single year, reaching ~1% of everything in the
   press.

## Data sources

| Source | File | Coverage | Notes |
|--------|------|----------|-------|
| Google Books Ngram | `data/ngram_ai_ml_1990_2019.csv` | 1990–2019 | Phrase frequency as a fraction of all text; multiplied by 1e6 in the chart for readability. |
| Media Cloud | `data/mediacloud_ai_2010_2023.csv` | 2010–2023 | Yearly totals aggregated from the raw daily export `data/mediacloud_ai_daily_2010_2023.csv`. `count` = articles mentioning AI; `ratio` = count ÷ total articles that year. |
| GDELT | `data/gdelt_results.csv` | 2010–2023 | **Evaluated and rejected** — see below. Kept for transparency. |

### Provenance

**Google Books Ngram** — [Ngram Viewer](https://books.google.com/ngrams)
- Search terms: `artificial intelligence`, `machine learning`
- Corpus: **English 2019** (`en-2019`)
- Smoothing: **3**
- Years: **1990–2019**
- Case-sensitive (the default; case-insensitive was *not* enabled)

**Media Cloud** — [search.mediacloud.org](https://search.mediacloud.org)
- Query: `artificial intelligence`
- Collection: **Online News Archive** (`onlinenews-mediacloud`)
- Date range: **2010-01-01 – 2023-12-31** (collected daily, then summed by year)
- Exported: **2026-06-01**
- The raw daily export (`count`, `total_count`, `ratio` per day) is kept at
  `data/mediacloud_ai_daily_2010_2023.csv`; the yearly file is derived from it.

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
from any working directory. It writes four images to `figures/`: the combined
three-panel figure (`ai_discourse_final.png`) and one standalone panel per
chart (`panel1_ngram.png`, `panel2_volume.png`, `panel3_share.png`), which the
web exhibit embeds.

## Project structure

```
.
├── index.html         # the web exhibit (published via GitHub Pages)
├── style.css          # shared light theme for the exhibit
├── ai_final.py        # analysis + figure generation (single source of truth)
├── data/              # source datasets (CSV)
├── figures/           # generated charts (regenerable)
├── requirements.txt
└── README.md
```

## Publishing updates

The site is served from the `main` branch by GitHub Pages. After changing the
data, charts, or `index.html`, regenerate the figures and push:

```bash
python ai_final.py
git add -A && git commit -m "Update exhibit" && git push
```

GitHub Pages rebuilds automatically within about a minute.
