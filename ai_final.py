"""A Computational History of AI Discourse (1990-2023).

Generates a three-panel figure from two complementary corpora:
  1. Google Ngram   -- "artificial intelligence" vs "machine learning" in books
  2. Media Cloud    -- volume of news articles mentioning AI
  3. Media Cloud    -- AI's share of all news coverage

GDELT was evaluated as a news source but rejected: its event counts jump
~10,000x between 2013 and 2015 (GDELT 2.0's coverage expansion), which makes
it unusable as a longitudinal trend. See README.md and data/gdelt_results.csv.

Data provenance and queries are documented in README.md. Run from anywhere;
paths are resolved relative to this file.
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
FIGURES = BASE / "figures"
FIGURES.mkdir(exist_ok=True)

# ============================================================
# DATA
# ============================================================
ngram = pd.read_csv(DATA / "ngram_ai_ml_1990_2019.csv")
# Convert to per-million words for readable axis values.
ngram["ai"] = ngram["artificial_intelligence"] * 1e6
ngram["ml"] = ngram["machine_learning"] * 1e6

mc = pd.read_csv(DATA / "mediacloud_ai_2010_2023.csv")

# ============================================================
# KEY EVENTS
# ============================================================
events_ngram = {
    1997: "Deep Blue\nvs Kasparov",
    2011: "IBM Watson\nwins Jeopardy",
    2016: "AlphaGo\nbeats Lee Sedol",
}
events_mc = {
    2016: "AlphaGo",
    2020: "GPT-3",
    2022: "ChatGPT\nlaunched",
    2023: "ChatGPT\nexplosion",
}

# ============================================================
# FIGURE
# ============================================================
fig, axes = plt.subplots(3, 1, figsize=(14, 17))
fig.patch.set_facecolor("#0F1117")
for ax in axes:
    ax.set_facecolor("#0F1117")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color("#444")
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_color("#444")

ax1, ax2, ax3 = axes

# --- Plot 1: Ngram ---
ax1.plot(ngram["year"], ngram["ai"], color="#4A90E2", lw=2.5, marker="o", ms=4,
         label="artificial intelligence")
ax1.plot(ngram["year"], ngram["ml"], color="#E74C3C", lw=2.5, marker="s", ms=4,
         label="machine learning")
for yr, lbl in events_ngram.items():
    ax1.axvline(yr, color="#FFD700", lw=1, ls="--", alpha=0.6)
    ax1.text(yr + 0.2, ax1.get_ylim()[1] * 0.05, lbl, color="#FFD700", fontsize=7.5,
             va="bottom", bbox=dict(facecolor="#0F1117", edgecolor="none", alpha=0.7))
ax1.annotate("AI Winter\n1990s decline", xy=(1995, ngram["ai"].iloc[5]),
             xytext=(1992, ngram["ai"].iloc[5] + 0.3), color="#AAAAAA", fontsize=8,
             arrowprops=dict(arrowstyle="->", color="#AAAAAA"))
ax1.annotate('"Machine learning"\novertakes "AI" ~2013', xy=(2013, ngram["ml"].iloc[23]),
             xytext=(2007, ngram["ml"].iloc[23] + 0.5), color="#FFD700", fontsize=8,
             arrowprops=dict(arrowstyle="->", color="#FFD700"))
ax1.set_title('Google Ngram: "artificial intelligence" vs "machine learning" in books (1990-2019)',
              color="white", fontsize=11, fontweight="bold", pad=10)
ax1.set_ylabel("Frequency per million words", color="white", fontsize=10)
ax1.legend(facecolor="#1A1A2E", edgecolor="#444", labelcolor="white", fontsize=9)
ax1.tick_params(axis="both", colors="white")
ax1.set_xticks(ngram["year"][::2])
ax1.set_xticklabels(ngram["year"][::2], rotation=45, color="white")

# --- Plot 2: Media Cloud article count ---
colors_bar = ["#E74C3C" if y >= 2022 else "#4A90E2" for y in mc["year"]]
ax2.bar(mc["year"], mc["count"] / 1000, color=colors_bar, alpha=0.8, width=0.6)
for yr, lbl in events_mc.items():
    ax2.axvline(yr, color="#FFD700", lw=1, ls="--", alpha=0.6)
    ax2.text(yr + 0.1, mc["count"].max() / 1000 * 0.88, lbl, color="#FFD700",
             fontsize=7.5, bbox=dict(facecolor="#0F1117", edgecolor="none", alpha=0.7))
ax2.set_title('Media Cloud: Global news articles mentioning "artificial intelligence" (2010-2023)\n'
              "Source: Harvard/MIT Media Cloud -- 1,600+ global English-language news sources",
              color="white", fontsize=11, fontweight="bold", pad=10)
ax2.set_ylabel("Articles (thousands)", color="white", fontsize=10)
ax2.set_xticks(mc["year"])
ax2.set_xticklabels(mc["year"], rotation=45, color="white")
ax2.tick_params(axis="y", colors="white")
blue_patch = mpatches.Patch(color="#4A90E2", alpha=0.8, label="Pre-ChatGPT era")
red_patch = mpatches.Patch(color="#E74C3C", alpha=0.8, label="ChatGPT era (2022+)")
ax2.legend(handles=[blue_patch, red_patch], facecolor="#1A1A2E", edgecolor="#444",
           labelcolor="white", fontsize=9)

# --- Plot 3: Media Cloud share of coverage ---
ax3.fill_between(mc["year"], mc["ratio"] * 100, color="#9B59B6", alpha=0.4)
ax3.plot(mc["year"], mc["ratio"] * 100, color="#9B59B6", lw=2.5, marker="o", ms=6)
for yr in events_mc:
    ax3.axvline(yr, color="#FFD700", lw=1, ls="--", alpha=0.6)
ax3.set_title("Media Cloud: Share of all news coverage devoted to AI (2010-2023)\n"
              "(AI articles / total articles per year)",
              color="white", fontsize=11, fontweight="bold", pad=10)
ax3.set_ylabel("% of all news coverage", color="white", fontsize=10)
ax3.set_xticks(mc["year"])
ax3.set_xticklabels(mc["year"], rotation=45, color="white")
ax3.tick_params(axis="y", colors="white")
ax3.annotate(f'2023: {mc["ratio"].iloc[-1] * 100:.2f}%\n(ChatGPT effect)',
             xy=(2023, mc["ratio"].iloc[-1] * 100),
             xytext=(2020, mc["ratio"].iloc[-1] * 100 - 0.2),
             color="white", fontsize=8,
             arrowprops=dict(arrowstyle="->", color="white"))

fig.suptitle("From the AI Winter to the ChatGPT Explosion\n"
             "A Computational History of AI Discourse (1990-2023)",
             color="white", fontsize=15, fontweight="bold", y=1.01)

plt.tight_layout(pad=3.0)
out = FIGURES / "ai_discourse_final.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="#0F1117")
print(f"Done! Saved {out}")
