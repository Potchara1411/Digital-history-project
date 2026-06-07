"""A Computational History of AI Discourse (1990-2023).

Builds visualizations from two complementary corpora:
  1. Google Ngram   -- "artificial intelligence" vs "machine learning" in books
  2. Media Cloud    -- volume of news articles mentioning AI
  3. Media Cloud    -- AI's share of all news coverage

GDELT was evaluated as a news source but rejected: its event counts jump
~10,000x between 2013 and 2015 (GDELT 2.0's coverage expansion), which makes
it unusable as a longitudinal trend. See README.md and data/gdelt_results.csv.

Outputs (to figures/):
  ai_discourse_final.png  -- the combined three-panel figure
  panel1_ngram.png        -- standalone panels, for the web exhibit (index.html)
  panel2_volume.png
  panel3_share.png

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

# Light theme palette (matches the website).
BG = "#FFFFFF"        # figure / axes background
FG = "#1A1D24"        # primary text, ticks, titles
MUTED = "#666666"     # secondary annotations
SPINE = "#B8BCC4"     # axis lines
ACCENT = "#B8860B"    # event markers (dark goldenrod, readable on white)
BLUE = "#2E75B6"
RED = "#E74C3C"
PURPLE = "#7E4FA8"

# ============================================================
# DATA
# ============================================================
ngram = pd.read_csv(DATA / "ngram_ai_ml_1990_2019.csv")
# Convert to per-million words for readable axis values.
ngram["ai"] = ngram["artificial_intelligence"] * 1e6
ngram["ml"] = ngram["machine_learning"] * 1e6

mc = pd.read_csv(DATA / "mediacloud_ai_2010_2023.csv")

# GDELT normalized "Volume Intensity" (% of all monitored coverage), daily 2017-2023.
# Used only as a robustness check: a second, independent news source. GDELT's raw
# event counts are unusable as a trend (see README), but this *normalized* metric is
# comparable across time. Aggregated to yearly means for the 2017-2023 overlap.
gdelt_daily = pd.read_csv(DATA / "gdelt_ai_volume_daily_2017_2023.csv")
gdelt_daily["year"] = pd.to_datetime(gdelt_daily["Date"]).dt.year
gdelt_year = gdelt_daily[gdelt_daily["year"] <= 2023].groupby("year")["Value"].mean()

# GDELT average tone of AI coverage (2010-2023). Tone is an average sentiment score,
# so unlike the raw event count it is only mildly affected by GDELT's source growth.
# 2010-2013 rest on small samples (<400 events) and are flagged in the chart.
gdelt_tone = pd.read_csv(DATA / "gdelt_results.csv")
gdelt_tone.columns = ["year", "event_count", "avg_tone"]

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


def style_ax(ax):
    """Apply the shared light theme to a single axis."""
    ax.set_facecolor(BG)
    ax.tick_params(colors=FG)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines["bottom"].set_visible(True)
    ax.spines["bottom"].set_color(SPINE)
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_color(SPINE)
    ax.grid(axis="y", color="#EEEEEE", lw=0.8)
    ax.set_axisbelow(True)


# ============================================================
# PANEL DRAWING FUNCTIONS (shared by combined + standalone figures)
# ============================================================
def draw_ngram(ax):
    ax.plot(ngram["year"], ngram["ai"], color=BLUE, lw=2.5, marker="o", ms=4,
            label="artificial intelligence")
    ax.plot(ngram["year"], ngram["ml"], color=RED, lw=2.5, marker="s", ms=4,
            label="machine learning")
    for yr, lbl in events_ngram.items():
        ax.axvline(yr, color=ACCENT, lw=1, ls="--", alpha=0.6)
        ax.text(yr + 0.2, ax.get_ylim()[1] * 0.05, lbl, color=ACCENT, fontsize=7.5,
                va="bottom", bbox=dict(facecolor=BG, edgecolor="none", alpha=0.7))
    ax.annotate("AI Winter\n1990s decline", xy=(1995, ngram["ai"].iloc[5]),
                xytext=(1998.3, 1.78), color=MUTED, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.annotate('"Machine learning"\novertakes "AI" ~2013', xy=(2013, ngram["ml"].iloc[23]),
                xytext=(2007, ngram["ml"].iloc[23] + 0.5), color=ACCENT, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=ACCENT))
    ax.set_title('Google Ngram: "artificial intelligence" vs "machine learning" in books (1990-2019)',
                 color=FG, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("Frequency per million words", color=FG, fontsize=10)
    ax.legend(facecolor=BG, edgecolor=SPINE, labelcolor=FG, fontsize=9)
    ax.tick_params(axis="both", colors=FG)
    ax.set_xticks(ngram["year"][::2])
    ax.set_xticklabels(ngram["year"][::2], rotation=45, color=FG)


def draw_volume(ax):
    colors_bar = [RED if y >= 2022 else BLUE for y in mc["year"]]
    ax.bar(mc["year"], mc["count"] / 1000, color=colors_bar, alpha=0.85, width=0.6)
    for yr, lbl in events_mc.items():
        ax.axvline(yr, color=ACCENT, lw=1, ls="--", alpha=0.6)
        ax.text(yr + 0.1, mc["count"].max() / 1000 * 0.88, lbl, color=ACCENT,
                fontsize=7.5, bbox=dict(facecolor=BG, edgecolor="none", alpha=0.7))
    ax.set_title('Media Cloud: Global news articles mentioning "artificial intelligence" (2010-2023)\n'
                 "Source: Harvard/MIT Media Cloud -- 1,600+ global English-language news sources",
                 color=FG, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("Articles (thousands)", color=FG, fontsize=10)
    ax.set_xticks(mc["year"])
    ax.set_xticklabels(mc["year"], rotation=45, color=FG)
    ax.tick_params(axis="y", colors=FG)
    blue_patch = mpatches.Patch(color=BLUE, alpha=0.85, label="Pre-ChatGPT era")
    red_patch = mpatches.Patch(color=RED, alpha=0.85, label="ChatGPT era (2022+)")
    ax.legend(handles=[blue_patch, red_patch], facecolor=BG, edgecolor=SPINE,
              labelcolor=FG, fontsize=9)


def draw_share(ax):
    ax.fill_between(mc["year"], mc["ratio"] * 100, color=PURPLE, alpha=0.25)
    ax.plot(mc["year"], mc["ratio"] * 100, color=PURPLE, lw=2.5, marker="o", ms=6)
    top = ax.get_ylim()[1]
    for yr, lbl in events_mc.items():
        ax.axvline(yr, color=ACCENT, lw=1, ls="--", alpha=0.6)
        # 2023 is described by the value annotation below, so skip its line label.
        if yr != 2023:
            ax.text(yr + 0.1, top * 0.62, lbl, color=ACCENT, fontsize=7.5,
                    bbox=dict(facecolor=BG, edgecolor="none", alpha=0.7))
    ax.set_title("Media Cloud: Share of all news coverage devoted to AI (2010-2023)\n"
                 "(AI articles / total articles per year)",
                 color=FG, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("% of all news coverage", color=FG, fontsize=10)
    ax.set_xticks(mc["year"])
    ax.set_xticklabels(mc["year"], rotation=45, color=FG)
    ax.tick_params(axis="y", colors=FG)
    ax.annotate(f'2023: {mc["ratio"].iloc[-1] * 100:.2f}%\n(ChatGPT effect)',
                xy=(2023, mc["ratio"].iloc[-1] * 100),
                xytext=(2020, mc["ratio"].iloc[-1] * 100 - 0.2),
                color=FG, fontsize=8,
                arrowprops=dict(arrowstyle="->", color=FG))


TEAL = "#159A8C"


def draw_tone(ax):
    """Average tone of AI news coverage. The point: it is negative every year —
    there was no 'optimism' era to lose. What changed was scale, not sentiment."""
    g = gdelt_tone
    small = g["event_count"] < 1000  # 2010-2013: small, noisier samples
    ax.axhline(0, color="#888888", lw=1.2)
    ax.text(2009.6, 0.12, "neutral", color=MUTED, fontsize=8, va="bottom")
    ax.fill_between(g["year"], g["avg_tone"], 0, color=RED, alpha=0.08)
    ax.plot(g["year"], g["avg_tone"], color=RED, lw=2.5, zorder=3)
    ax.scatter(g.loc[~small, "year"], g.loc[~small, "avg_tone"], color=RED, s=45, zorder=4)
    ax.scatter(g.loc[small, "year"], g.loc[small, "avg_tone"], facecolors="white",
               edgecolors=RED, linewidths=1.5, s=45, zorder=4)
    ax.annotate("Negative every single year —\nno 'optimism' phase to lose",
                xy=(2018, float(g.loc[g.year == 2018, "avg_tone"].iloc[0])),
                xytext=(2014.0, -2.2), color=FG, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=MUTED))
    ax.text(2009.6, -6.7, "Hollow points (2010–2013): small samples (<400 articles), so noisier.",
            color=MUTED, fontsize=7.5)
    ax.set_ylim(-7, 0.8)
    ax.set_title("GDELT: average tone of AI news coverage (2010–2023)\n"
                 "Lower = more negative.  Tone is an average, so it resists the source-growth "
                 "problem that ruins GDELT's counts.",
                 color=FG, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("Average tone (GDELT)", color=FG, fontsize=10)
    ax.set_xticks(g["year"])
    ax.set_xticklabels(g["year"], rotation=45, color=FG)
    ax.tick_params(axis="y", colors=FG)


def draw_robustness(ax):
    """Robustness check: GDELT and Media Cloud, two independent news datasets,
    plotted as normalized % of coverage over their 2017-2023 overlap."""
    mc_over = mc[(mc["year"] >= 2017) & (mc["year"] <= 2023)]
    ax.plot(mc_over["year"], mc_over["ratio"] * 100, color=PURPLE, lw=2.5,
            marker="o", ms=6, label="Media Cloud — AI share of all news")
    ax.plot(gdelt_year.index, gdelt_year.values, color=TEAL, lw=2.5,
            marker="s", ms=6, label="GDELT — AI % of monitored coverage")
    ax.axvline(2022, color=ACCENT, lw=1, ls="--", alpha=0.6)
    ax.text(2022.05, ax.get_ylim()[1] * 0.5, "ChatGPT\nlaunched", color=ACCENT,
            fontsize=7.5, bbox=dict(facecolor=BG, edgecolor="none", alpha=0.7))
    ax.set_title("Robustness check: two independent news datasets agree (2017-2023)\n"
                 "Both normalize away source growth -- and both spike after ChatGPT",
                 color=FG, fontsize=11, fontweight="bold", pad=10)
    ax.set_ylabel("% of news coverage", color=FG, fontsize=10)
    ax.set_xticks(range(2017, 2024))
    ax.set_xticklabels(range(2017, 2024), color=FG)
    ax.tick_params(axis="y", colors=FG)
    ax.legend(facecolor=BG, edgecolor=SPINE, labelcolor=FG, fontsize=9, loc="upper left")


PANELS = [
    (draw_ngram, "panel1_ngram.png"),
    (draw_volume, "panel2_volume.png"),
    (draw_share, "panel3_share.png"),
]
# Supplementary panel — a methodological robustness check, shown on the web exhibit
# but kept out of the main three-act narrative figure.
EXTRA_PANELS = [
    (draw_robustness, "panel4_robustness.png"),
    (draw_tone, "panel5_tone.png"),
]


def save_combined():
    """The stacked three-panel figure (used in the README)."""
    fig, axes = plt.subplots(3, 1, figsize=(14, 17))
    fig.patch.set_facecolor(BG)
    for ax, (draw, _) in zip(axes, PANELS):
        style_ax(ax)
        draw(ax)
    fig.suptitle("From the AI Winter to the ChatGPT Explosion\n"
                 "A Computational History of AI Discourse (1990-2023)",
                 color=FG, fontsize=15, fontweight="bold", y=1.01)
    plt.tight_layout(pad=3.0)
    out = FIGURES / "ai_discourse_final.png"
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    return out


def save_panels():
    """Standalone panels for the web exhibit (index.html)."""
    saved = []
    for draw, name in PANELS + EXTRA_PANELS:
        fig, ax = plt.subplots(figsize=(11, 5.5))
        fig.patch.set_facecolor(BG)
        style_ax(ax)
        draw(ax)
        plt.tight_layout(pad=1.5)
        out = FIGURES / name
        fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
        plt.close(fig)
        saved.append(out)
    return saved


if __name__ == "__main__":
    outputs = [save_combined(), *save_panels()]
    for path in outputs:
        print(f"Saved {path.relative_to(BASE)}")
