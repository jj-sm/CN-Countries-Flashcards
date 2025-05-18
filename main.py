from csv import DictReader
import asyncio
import aiohttp
import os

TEX_FILENAME = 'flashcards.tex'

class FlashFront:
    def __init__(self, country_ISO) -> None:
        self.country_code = country_ISO

    def out_url(self) -> str:
        return f"https://flagcdn.com/w320/{self.country_code.lower()}.png"

    def __repr__(self) -> str:
        return self.out_url()

    def __str__(self) -> str:
        return self.out_url()

    async def save(self):
        """Asynchronously downloads and saves the flag image."""
        url = self.out_url()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=10) as response:
                    response.raise_for_status()
                    os.makedirs("flags", exist_ok=True)
                    with open(f"flags/{self.country_code.lower()}.png", "wb") as f:
                        f.write(await response.read())
            except aiohttp.ClientResponseError as e:
                print(f"Failed to download flag for {self.country_code}: {e.status}")
            except Exception as e:
                print(f"Error downloading flag for {self.country_code}: {e}")


class FlashBack:
    def __init__(self, country_ISO: str, facts_db: str) -> None:
        self.country_code = country_ISO
        self.facts_csv_path = facts_db

    def _find_country_data(self) -> dict:
        """Finds all data for the given country ISO code from the CSV file."""
        try:
            with open(self.facts_csv_path, "r", encoding="utf-8") as f:
                reader = DictReader(f, delimiter=';')
                for row in reader:
                    if row.get("iso") and row["iso"].lower() == self.country_code.lower():
                        return {
                            "cca2": row.get("iso", ""),
                            "name": row.get("country", "N/A"),
                            "capital": row.get("capital", "N/A"),
                            "languages": [lang.strip() for lang in row.get("lang", "N/A").split(",")],
                            "name_cn": row.get("country_cn", "N/A"),
                            "capital_cn": row.get("capital_cn", "N/A"),
                            "languages_cn": row.get("lang_cn", "N/A"),
                            "fact": row.get("fact", "No fact this time :c")
                        }
            return None  # Return None if country not found in CSV
        except Exception as e:
            print(f"Error reading CSV for {self.country_code}: {e}")
            return None

    async def fetch(self) -> dict:
        """Returns country data from CSV."""
        return self._find_country_data()


async def init_db(facts_csv_path: str) -> dict:
    """Initialize Flashcard objects from CSV file."""
    objects = {}

    try:
        with open(facts_csv_path, "r", encoding="utf-8") as f:
            reader = DictReader(f, delimiter=';')
            for row in reader:
                if iso_code := row.get("iso"):
                    objects[iso_code] = {
                        "front": FlashFront(iso_code),
                        "back": FlashBack(iso_code, facts_csv_path)
                    }
    except Exception as e:
        print(f"Error initializing database from CSV: {e}")

    return objects


def generate_flashcard(country_ISO, country_en, country_cn, capital_en, capital_cn, lang_en, lang_cn, fact):
    """Generate a customizable flashcard"""
    fact = fact

    # Escape special LaTeX characters
    def escape_text(text):
        replacements = {
            '%': '\\%',
            '&': '\\&',
            '#': '\\#',
            '$': '\\$',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}'
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    fact = escape_text(fact)
    country_en = escape_text(country_en)
    country_cn = escape_text(country_cn)
    capital_en = escape_text(capital_en)
    capital_cn = escape_text(capital_cn)
    lang_en = escape_text(lang_en)
    lang_cn = escape_text(lang_cn)

    card = fr"""\card{{\centering\includegraphics[width=0.3\textwidth]{{flags/{country_ISO.lower()}.png}}}}{{
\begin{{tabular}}{{m{{3cm}} m{{5cm}}}} \textbf{{{country_en}}} & \textbf{{{country_cn}}} \\[0.5em] \multicolumn{{1}}{{m{{3cm}}}}{{\raggedright {capital_en}\\{capital_cn}\\{lang_en}\\{lang_cn}}} &
\raggedright \textbf{{Fact:}} {fact}
\end{{tabular}}
}}"""

    return card


def tex(cards: list[str]) -> str:
    """Generate Tex code"""
    header = r"""
\documentclass[frontgrid, backgrid,a4,12pt]{flacards}
\usepackage{color}
\usepackage{graphicx}
\usepackage{etoolbox}
\pretocmd{\card}{\def\curhint{}}{}{}

\pagesetup{2}{4}

% Chinese support
\usepackage{xeCJK}

\renewcommand{\cardtextstylef}{\Huge}
\renewcommand{\cardtextstyleb}{\small}
\renewcommand{\brfoot}{}
\renewcommand{\bcfoot}{\let\\\relax\footnotesize\curhint}
\renewcommand{\flhead}{\footnotesize\thecardno}
\renewcommand{\brhead}{\footnotesize\thecardno}

\usepackage{array}
\usepackage{multirow}
\usepackage{ragged2e}

\newcommand{\inputfield}{\rule[-1mm]{3cm}{0.5pt}}
\begin{document}
"""
    footer = r"""
\end{document}"""
    return header + "\n".join(cards) + footer


async def process_country(country_code, cards):
    """Countrycode ISO to generate flashcard."""
    try:
        back_info = await cards["back"].fetch()
        if not back_info:
            return None

        await cards["front"].save()

        card = generate_flashcard(
            country_ISO=country_code,
            country_en=back_info["name"],
            country_cn=back_info["name_cn"],
            capital_en=back_info["capital"],
            capital_cn=back_info["capital_cn"],
            lang_en=", ".join(back_info["languages"]),
            lang_cn=back_info["languages_cn"],
            fact=back_info["fact"]
        )

        print(f"Generated flashcard for {back_info['name']}")
        return card
    except Exception as e:
        print(f"Error processing {country_code}: {str(e)}")
        return None


async def main():
    """Main function to generate flashcards."""
    # Path to CSV
    facts_csv_path = os.path.join(os.path.dirname(__file__), "data", "facts.csv")

    # Initialize database from csv
    flashcard_db = await init_db(facts_csv_path)

    if not flashcard_db:
        print("No countries found in CSV or error reading CSV")
        return

    latex_cards = []
    tasks = [process_country(code, cards) for code, cards in flashcard_db.items()]
    results = await asyncio.gather(*tasks)

    for result in filter(None, results):
        latex_cards.append(result)

    latex_document = tex(latex_cards)

    try:
        with open(TEX_FILENAME, "w", encoding="utf-8") as f:
            f.write(latex_document)
        print(f"Generated {len(latex_cards)} flashcards in {TEX_FILENAME}")
    except IOError as e:
        print(f"Error writing LaTeX file: {e}")


if __name__ == "__main__":
    asyncio.run(main())
    print("Done!")
    print("Remember this requires XeLaTeX to compile!")