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
    {
        "slug": "job-finder",
        "title": "Job Finder: AI-driven job search",
        "year": "2026",
        "domain": "contentedwife.com/jobs",
        "url": "https://contentedwife.com/jobs/",
        "images": [
            {"src": "images/portfolio/job-finder/04-job-openings.webp", "alt": "Job Openings: postings graded A to E with a match score, the best-fitting target and Hate, Dislike, Like and Dream buttons"},
            {"src": "images/portfolio/job-finder/01-job-profile.webp", "alt": "My Job Profile: sliders from -5 to +5 for what matters in a job, such as on-call, travel, remote work, compensation and stability"},
            {"src": "images/portfolio/job-finder/03-job-targets.webp", "alt": "Job Targets: career directions described in plain words, with the number of postings that fit each"},
            {"src": "images/portfolio/job-finder/06-job-skills.webp", "alt": "Job Skills: how many fitting postings ask for each programming language, and how many require it"},
            {"src": "images/portfolio/job-finder/02-summary-dashboard.webp", "alt": "Summary Dashboard: a world map shaded by the number of saved postings, filterable by region and remote"},
            {"src": "images/portfolio/job-finder/05-job-websites.webp", "alt": "Job Websites: the best places to look for a chosen target, each with a fit score and a reason"},
        ],
        "problem": (
            "Searching for a job means reading long, multi-page listings scattered across many sites, "
            "then losing track of which ones you have already seen. Job Finder hands that reading to AI. "
            "It turns every unstructured posting into a tidy, searchable record, scores it against what "
            "matters to you, and remembers it for good. You look at a ranked shortlist instead of a pile "
            "of tabs, which saves hours every week."
        ),
        "second_heading": "What is new about it",
        "difficulty": [
            "AI reads the posting for you. A messy listing becomes a structured record: company, place, "
            "topic, and the skills it requires or merely prefers.",
            "Ranking by your priorities, not keywords. Slide about twenty factors from -5 to +5 (on-call, "
            "travel, remote, pay, stability, commute and more) and every posting gets a match score and an "
            "A to E grade. Move a slider and the whole ranking updates at once.",
            "Careers described in plain words. You write the directions you are weighing, for example "
            "\"Blockchain developer\", and the AI rates every posting from 0 to 100 against each one.",
            "Nothing is ever forgotten or lost. Every posting you have seen is kept with your verdict (hate, "
            "dislike, like, dream, want to apply), so you never read the same listing twice.",
            "It also reads the market. A map shows where the jobs are, a skills table shows how many fitting "
            "postings require each skill, and the AI recommends which job sites are worth searching for "
            "each target.",
            "A private search that feeds public sites. The listings you liked most are streamed to topic "
            "sites such as the crypto site stas.club and the AI site agentics.actor, so one person's job "
            "hunt becomes a curated job board for everyone else.",
        ],
        "stack": ["AI parsing", "Point-based ranking", "Skills analytics", "Public job feeds"],
    },
    {
        "slug": "erp-2006",
        "title": "Custom ERP for a bottled-water manufacturer",
        "year": "2006",
        "images": [
            {"src": "images/portfolio/erp-2006/01-delivery-routes.webp", "alt": "Delivery routes: orders grouped into routes for Moscow, PET and other deliveries, with totals of bottles, coolers, cups and gas cylinders, and the orders of the selected route below (customer names and addresses blurred)"},
            {"src": "images/portfolio/erp-2006/03-journal-entry.webp", "alt": "An accounting entry: debit and credit accounts from the chart of accounts, exchange rate, amounts in rubles and dollars, and who created, posted and last changed it (names blurred)"},
            {"src": "images/portfolio/erp-2006/05-invoice-form-designer.webp", "alt": "Invoice form designer: the official TORG-12 delivery note laid out on screen, with a list of sections and data fields to place on the form"},
            {"src": "images/portfolio/erp-2006/02-home-finance-expenses.webp", "alt": "Home Finance: a day-by-day list of expenses and income in several currencies, with running daily balances"},
            {"src": "images/portfolio/erp-2006/04-home-finance-by-category.webp", "alt": "Home Finance: yearly expenses by category and month, with totals and the average spent per day"},
        ],
        "problem": (
            "A water producer delivers returnable 19-litre bottles, PET bottles, coolers and cups to homes "
            "and offices across a big city. Every day it has to know who ordered what, which driver takes it "
            "where, what is left in stock, and who has paid. This custom ERP ran that whole chain in one "
            "system: orders turned into delivery routes, stock was tracked, payments were reconciled and "
            "the books were kept to GAAP-style standards."
        ),
        "difficulty": [
            "Orders to routes. Orders are grouped by address into delivery routes, and the "
            "dispatcher sees each route's totals of bottles, coolers, cups and gas cylinders at a glance.",
            "Several kinds of goods and packaging at once. Stock and orders are tracked per item type, "
            "including returnable bottles that come back and have to be counted again.",
            "Proper double-entry accounting in more than one currency. Every posting has a debit and a "
            "credit account, an exchange rate, amounts in rubles and dollars, and a full trail of who "
            "created, posted and changed it. A wrong entry is reversed, never silently overwritten.",
            "Payments reconciliation. Money received is matched to the orders and invoices it pays, so "
            "what is paid and what is still owed is always clear.",
            "Invoice mass printing. Official forms such as the TORG-12 delivery note are laid out in an "
            "on-screen designer, then filled with live data and printed for a whole day of deliveries at once.",
        ],
        "stack": ["GAAP accounting", "Inventory management", "Orders tracking", "Payments reconciliation", "Invoice mass printing"],
    },
]
