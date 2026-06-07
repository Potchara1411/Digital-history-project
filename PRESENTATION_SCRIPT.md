# Presentation script — *From Scientific Optimism to Geopolitical Anxiety*

**Target length:** ~9–10 minutes (12 slides). Times are guidelines; speak naturally,
look up from the script, and let the charts do some of the talking.

The same script is embedded in the PowerPoint as **presenter notes** — in
PowerPoint use *View → Presenter View*, in Keynote the notes panel, or in Google
Slides the notes below each slide.

---

### Slide 1 — Title *(~20s)*
My project is a computational history of artificial intelligence — not the
technology, but the *discourse*. I treat media coverage of AI as a primary source,
and I ask a historian's question: when, and how, did the way we talk about AI
actually change — across more than thirty years?

### Slide 2 — The Gap *(~55s)*
My starting point is Kate Crawford's *Atlas of AI*. She argues powerfully that AI
is a system of power and extraction — a "registry of power." But it's a
*qualitative* argument. She never shows, computationally, *when* public discourse
actually shifted, or *how fast*. That's the gap I set out to fill — with thirty
years of book data and thirteen years of global news data, to locate the turning
points and measure their speed. And I flip the usual digital-humanities question:
instead of "what can AI do for historians," I ask "what can historians do with AI
discourse as a primary source." My second frame: this all looks remarkably like
nuclear anxiety in the 1950s and 60s.

### Slide 3 — Data & Method *(~50s)*
Two kinds of evidence. *Conventional* sources frame the project — Crawford's book,
print archives like *Wired*, *TIME* and *The Economist*, and government policy
documents. *Digital* sources give me the numbers — Google Ngram for books, Media
Cloud for news, and GDELT. The method pairs quantitative pattern detection with
qualitative interpretation — adapting Dr. Woo's work on semantic shifts in Cold War
newspapers. And it's all reproducible: one script, public data.

### Slide 4 — Act I: The Winter and the Rebranding *(~55s)*
Act one — the first surprise: the story starts with *decline*. The blue line,
"artificial intelligence," falls through the 1990s — the AI Winter, when the term
became almost an embarrassment after 1980s hype collapsed. But watch the red line,
"machine learning" — it rises steadily and *overtakes* AI around 2013. The field
didn't quit; it rebranded around concrete, working method. That vocabulary shift is
itself a historical argument.

### Slide 5 — Act II: Back into the Light *(~50s)*
Act two: how AI came back. The technology started *working* — deep learning, around
2012 — and there was public spectacle, above all AlphaGo beating the world's best Go
player in 2016. The news followed: coverage climbs from a few thousand into the tens
of thousands of articles a year. AI moves from the lab bench to the front page.

### Slide 6 — Act III: The ChatGPT Explosion *(~50s)*
Act three: the explosion. ChatGPT, late 2022. But raw article counts can mislead —
maybe there's just more news overall. So I measure AI's *share* of all coverage.
Even controlling for that, it more than *doubled in a single year* — to about 1% of
everything in the press. A genuine shift in collective attention.

### Slide 7 — The Twist: It was never optimism *(~55s)*
Now the twist — and here I push back on the obvious story. The conventional
narrative is optimism turning to fear. But look at the *tone* of AI coverage: it's
negative every single year — around minus five — even back in 2010. There was no
golden age of optimism to fall from. I'm honest about the data: the early years are
small samples, which I've marked hollow. But the pattern is unmistakable.

### Slide 8 — The Argument: scale and salience *(~60s)*
So here's my argument. AI discourse didn't drift from hope to fear; it was wary from
the start. What actually changed was two things. First, *scale* — the explosion of
attention after AlphaGo and ChatGPT. Second, *political salience* — AI went from a
*scientific* keyword, like Deep Blue, to a *geopolitical* one, tied to US–China
competition, existential risk, and regulation. The anxiety isn't new; its scale and
its politics are. And that's the same template societies used for nuclear fear in
the 1950s and 60s — which makes today's AI anxiety historically legible rather than
unprecedented.

### Slide 9 — Robustness check *(~50s)*
A good skeptic should ask: what if that 2023 spike is just a quirk of Media Cloud?
So I test it against a separate dataset, GDELT, using its *normalized* measure. Two
datasets, different teams, different methods — yet they track each other closely and
in 2023 land at almost exactly the same value: 1.04 versus 1.05 percent. The surge
is real.

### Slide 10 — Why we did NOT trust GDELT's raw counts *(~60s)* — **key slide**
This is the slide I'm proudest of. I almost used GDELT as my main news source — but
look at its raw counts: AI events go from 347 in 2013, to 53,000 in 2014, to 3.9
*million* in 2015. A ten-thousand-fold jump in two years. No real phenomenon grows
that fast: GDELT simply expanded its own sources in 2015. The instrument changed,
not the world. So I use only its time-comparable metrics — normalized share and tone.
This source criticism *is* the scholarship: a measurement is only as good as the
instrument's consistency over time.

### Slide 11 — Conclusion *(~50s)*
To conclude: books recorded a quiet rebranding — AI, to machine learning, and back.
News recorded an explosion in scale and political salience after ChatGPT. The shift
was scale and politics, not optimism to fear. By treating AI coverage as a primary
source, I extend Crawford's argument with the quantitative evidence it was missing —
and show how a society negotiates power, fear, and technological change over time.

### Slide 12 — Thank you *(~15s)*
That's my project. The full interactive exhibit, and all the code and data, are
online at these links. Thank you — I'm happy to take any questions.

---

## Likely questions (prep)

- **"Isn't 'optimism to anxiety' contradicted by your own tone data?"** Yes — and
  that's the point. The title is the conventional assumption; my contribution is
  showing it's wrong on sentiment. The real shift is *scale* and *political
  salience*, not hope-to-fear.
- **"Why books *and* news?"** They answer different questions. Books (slow, edited)
  show how the *field* named itself; news (fast) shows *public* attention. Using both
  separates the vocabulary shift from the attention explosion.
- **"Why does Ngram stop at 2019?"** That's the last year of Google's 2019 books
  corpus. News data carries the story to 2023.
- **"Isn't this English-only / Western-biased?"** Yes — Ngram's English corpus and
  Media Cloud's English sources mean this is a history of *Anglophone* AI discourse.
  I treat that limit as part of the argument, not a hidden flaw.
- **"You rejected GDELT — why use it at all?"** I rejected its *raw counts* (distorted
  by source growth). Its *normalized share* and its *tone* are averages/ratios that
  stay comparable across time, so they're valid — with the early-sample caveat.
- **"How does this connect to Crawford?"** She makes the qualitative case that AI is
  about power; I supply the missing *timeline* — computational evidence of when and
  how fast the discourse became a discourse of power and geopolitics.
