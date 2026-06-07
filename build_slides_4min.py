"""Build the 4-minute in-progress presentation (ai_discourse_4min.pptx) — a tight
7-slide promo version in simple English (audience-friendly), separate from the full
deck (build_slides.py).

    python ai_final.py
    python build_slides_4min.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE = Path(__file__).resolve().parent
FIG = BASE / "figures"
OUT = BASE / "ai_discourse_4min.pptx"

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1A, 0x1D, 0x24)
MUTED = RGBColor(0x5B, 0x64, 0x70)
GOLD = RGBColor(0xB8, 0x86, 0x0B)
BLUE = RGBColor(0x2E, 0x75, 0xB6)
RED = RGBColor(0xE7, 0x4C, 0x3C)
PURPLE = RGBColor(0x7E, 0x4F, 0xA8)

EMU_W, EMU_H = Inches(13.333), Inches(7.5)
FONT = "Calibri"

prs = Presentation()
prs.slide_width, prs.slide_height = EMU_W, EMU_H
BLANK = prs.slide_layouts[6]


def bg(slide, color=WHITE):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def accent_bar(slide, x, y, w, h, color=GOLD):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background(); shp.shadow.inherit = False
    return shp


def text(slide, s, x, y, w, h, size=18, color=INK, bold=False, italic=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, line in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        r = p.add_run(); r.text = line
        r.font.size, r.font.color.rgb, r.font.bold, r.font.italic, r.font.name = (
            Pt(size), color, bold, italic, FONT)
    return tb


def bullets(slide, items, x, y, w, h, size=20, gap=12):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, (txt, c) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.line_spacing = 1.05
        d = p.add_run(); d.text = "•  "
        d.font.size, d.font.color.rgb, d.font.bold, d.font.name = Pt(size), GOLD, True, FONT
        r = p.add_run(); r.text = txt
        r.font.size, r.font.color.rgb, r.font.name = Pt(size), c, FONT
    return tb


def picture_centered(slide, path, top, max_w=Inches(10.4), max_h=Inches(4.4)):
    from PIL import Image
    iw, ih = Image.open(path).size
    scale = min(max_w / iw, max_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    slide.shapes.add_picture(str(path), int((EMU_W - w) / 2), top, width=w, height=h)


def header(slide, label, title):
    bg(slide)
    accent_bar(slide, Inches(0.6), Inches(0.55), Inches(0.16), Inches(0.62))
    text(slide, label, Inches(0.95), Inches(0.5), Inches(11.6), Inches(0.4), size=14, color=GOLD, bold=True)
    text(slide, title, Inches(0.95), Inches(0.82), Inches(11.9), Inches(0.8), size=30, color=INK, bold=True)


# ---- 1 · Title ----
s = prs.slides.add_slide(BLANK)
bg(s)
accent_bar(s, 0, 0, EMU_W, Inches(0.22)); accent_bar(s, 0, Inches(7.28), EMU_W, Inches(0.22))
text(s, "KAIST · DIGITAL HISTORY  ·  PROJECT IN PROGRESS", Inches(1), Inches(1.95), Inches(11.3),
     Inches(0.4), size=15, color=GOLD, bold=True, align=PP_ALIGN.CENTER)
text(s, "How the World Talks About AI\n1990 – 2023", Inches(1), Inches(2.45), Inches(11.3),
     Inches(2.0), size=44, color=INK, bold=True, align=PP_ALIGN.CENTER)
text(s, "A history of AI in books and news", Inches(1), Inches(4.5), Inches(11.3),
     Inches(0.6), size=21, color=MUTED, align=PP_ALIGN.CENTER)
text(s, "potchara1411.github.io/Digital-history-project", Inches(1), Inches(5.45), Inches(11.3),
     Inches(0.4), size=15, color=BLUE, align=PP_ALIGN.CENTER)

# ---- 2 · My idea ----
s = prs.slides.add_slide(BLANK)
header(s, "MY IDEA", "Adding data to a famous book")
bullets(s, [
    ("A famous scholar, Kate Crawford, says AI is really about power — but she uses ideas, "
     "not data", INK),
    ("I use data: 30 years of books + 13 years of news from around the world", INK),
    ("My question: WHEN did people’s view of AI change? I use old AI news as evidence", INK),
], Inches(1.15), Inches(2.05), Inches(11.3), Inches(4), size=22, gap=22)

# ---- 3 · Finding 1 ----
s = prs.slides.add_slide(BLANK)
header(s, "FINDING 1", "First AI went down — then it changed its name")
bullets(s, [
    ("In the 1990s, the word “artificial intelligence” went DOWN in books — people lost interest",
     BLUE),
    ("A new word, “machine learning,” became more popular and passed it by 2013", RED),
], Inches(0.95), Inches(1.72), Inches(11.6), Inches(1.0), size=16)
picture_centered(s, FIG / "panel1_ngram.png", Inches(2.9))

# ---- 4 · Finding 2 ----
s = prs.slides.add_slide(BLANK)
header(s, "FINDING 2", "Then AI news exploded")
bullets(s, [
    ("After AlphaGo (2016) and ChatGPT (2022), AI news grew very fast — about 1% of ALL news "
     "by 2023", PURPLE),
    ("There is more news today in general. But even so, AI grew much, much faster", INK),
], Inches(0.95), Inches(1.72), Inches(11.6), Inches(1.0), size=16)
picture_centered(s, FIG / "panel3_share.png", Inches(2.9))

# ---- 5 · The surprise ----
s = prs.slides.add_slide(BLANK)
header(s, "FINDING 3 · THE SURPRISE", "People were never happy about AI")
bullets(s, [
    ("The news about AI was negative EVERY year — even in 2010. People were never very hopeful",
     RED),
    ("The feeling did not change. What changed: AI became (1) a much BIGGER topic, and "
     "(2) a POLITICAL one — countries competing, danger, control", INK),
], Inches(0.95), Inches(1.72), Inches(11.6), Inches(1.0), size=16)
picture_centered(s, FIG / "panel5_tone.png", Inches(2.9))

# ---- 6 · Is it real? ----
s = prs.slides.add_slide(BLANK)
header(s, "IS IT REAL?", "I checked with another source")
bullets(s, [
    ("Is the 2023 rise real, or just a mistake in my data? I compared it with a different "
     "news database", INK),
    ("Both show almost the same result — so the rise is real", PURPLE),
], Inches(0.95), Inches(1.72), Inches(11.6), Inches(1.0), size=16)
picture_centered(s, FIG / "panel4_robustness.png", Inches(2.9))

# ---- 7 · Close ----
s = prs.slides.add_slide(BLANK)
bg(s)
accent_bar(s, 0, 0, EMU_W, Inches(0.22)); accent_bar(s, 0, Inches(7.28), EMU_W, Inches(0.22))
text(s, "See my website — and please share your questions", Inches(1), Inches(2.2), Inches(11.3),
     Inches(1.0), size=30, color=INK, bold=True, align=PP_ALIGN.CENTER)
text(s, "More charts and the full story are there", Inches(1), Inches(3.5), Inches(11.3),
     Inches(0.5), size=18, color=MUTED, align=PP_ALIGN.CENTER)
text(s, "potchara1411.github.io/Digital-history-project", Inches(1), Inches(4.2), Inches(11.3),
     Inches(0.5), size=22, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
text(s, "github.com/Potchara1411/Digital-history-project", Inches(1), Inches(4.95), Inches(11.3),
     Inches(0.4), size=14, color=MUTED, align=PP_ALIGN.CENTER)

NOTES = [
    "Hello. My project is about AI — but not the technology. It is about how people TALK about "
    "AI. I looked at 30 years of books and news. My question is simple: when did AI become a big "
    "topic? And were people ever happy about it? [~20s]",

    "A famous scholar, Kate Crawford, says AI is really about power and control. But she uses "
    "ideas, not data. She does not show WHEN people's view of AI changed. So I use data: 30 years "
    "of books, and 13 years of news from around the world. I use old AI news as evidence about "
    "history. [~45s]",

    "My first finding is a surprise. In the 1990s, the word 'artificial intelligence' went DOWN in "
    "books. People lost interest. Then a new word, 'machine learning,' became more popular. By "
    "2013, it passed 'artificial intelligence.' So the field changed its name. [~40s]",

    "My second finding: after 2016 and 2022 — after AlphaGo and ChatGPT — AI news exploded. In "
    "2023, about 1 percent of ALL news in the world was about AI. Of course, there is more news "
    "today in general. But even so, AI grew much, much faster. People really paid more attention to "
    "AI. [~40s]",

    "Now the surprising part. Many people think: first we were happy about AI, then we became "
    "afraid. But look. The news about AI was negative EVERY year — even in 2010. People were never "
    "really happy about AI. So the FEELING did not change. Two things changed. One: AI became a "
    "much BIGGER topic. Two: AI became a POLITICAL topic — about countries competing, like the US "
    "and China, and about danger and control. [~50s]",

    "Is this real, or just a mistake in my data? To check, I used a different news database. The "
    "two databases show almost the same result. So I am sure: the big rise in 2023 is real. [~35s]",

    "You can see everything on my website. Please look at it. And please share your questions and "
    "opinions — I really want to hear them. Thank you. [~25s]",
]
for slide, note in zip(prs.slides, NOTES):
    slide.notes_slide.notes_text_frame.text = note

prs.save(OUT)
print(f"Saved {OUT.name}  ({len(prs.slides._sldIdLst)} slides)")
