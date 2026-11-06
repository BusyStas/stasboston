"""Projects shown on /portfolio, in display order.

To add a screenshot: put the file in static/images/portfolio/<slug>/ and append
{"src": "images/portfolio/<slug>/<file>", "alt": "what it shows"} to the project's "images".
While a project has no screenshots yet, its cover art is shown as a single picture.
"""

PROJECTS = [
    {
        "slug": "astrotoken",
        "title": "AI-native astrology and numerology",
        "year": "2026",
        "domain": "astrotoken.info",
        "url": "https://astrotoken.info",
        "images": [
            {"src": "images/portfolio/astrotoken/01-home.webp", "alt": "AstroToken home page: twelve zodiac signs, a feature menu on the left and cards for each reading"},
            {"src": "images/portfolio/astrotoken/02-zodiac-sign.webp", "alt": "The Sagittarius reading: ruling planet, character, strengths, challenges and love"},
            {"src": "images/portfolio/astrotoken/03-name-meaning.webp", "alt": "Name meaning for Stas: native and English forms of the name, then origin, character and destiny"},
            {"src": "images/portfolio/astrotoken/04-zodiac-compatibility.webp", "alt": "Zodiac compatibility of a Gemini man and a Virgo woman: strengths, friction, money and family life"},
            {"src": "images/portfolio/astrotoken/05-business-by-ticker.webp", "alt": "Business review for the stock ticker MSFT: IPO date found by AI, founding sign, name number, character and good and hard years"},
        ],
        "problem": (
            "Most astrology and numerology sites either publish thin, generic text or pay for an AI call "
            "on every visit, so the bill grows with traffic. AstroToken starts with no content at all. "
            "The first visitor who asks for a reading triggers one AI call; the result is saved, and "
            "everyone after that reads the saved text. AI spend converges to zero as the audience grows, "
            "while the library of zodiac, name, compatibility and birth-chart readings keeps growing "
            "by itself. It also reviews businesses: enter a stock ticker, or a company name and founding "
            "date, and get a character profile and a ten-year outlook."
        ),
        "difficulty": [
            "Get-or-generate pipeline: cache first, then database, and only then the AI. Ordinary page "
            "views can only read, so crawlers and refreshes never trigger a paid call.",
            "Each reading is written once for all ten languages in a single generation, so every "
            "translation says the same thing.",
            "Cost guards: per-visitor and daily limits on new readings, plus an automatic retry when the "
            "AI answer is cut off.",
            "Business reviews with a fixed cost: the AI reading depends only on the company's founding sign "
            "and its name number, so there are 144 per language however many companies people look up. "
            "The company name, dates and the year-by-year table are calculated in code.",
            "Ticker lookups have no data feed: the AI finds the company, exchange and IPO date once and saves "
            "it. The page says the date was found by AI, shows how confident it is and lets the visitor "
            "correct it.",
            "Name meanings need a dictionary that builds itself: the AI detects the name's language and "
            "origin and derives its local and English forms before the meaning is written and stored.",
            "A serverless database that pauses when idle: fixed content is served from an edge cache so "
            "visitors never wait for it to wake up.",
            "Birth charts (sun, moon and rising sign) are calculated offline from planetary positions and "
            "a built-in city and time-zone list, with no external service.",
        ],
        "stack": ["Python / Flask", "Claude API", "Google Cloud Run", "SQL database", "Cloudflare R2"],
    },
]
