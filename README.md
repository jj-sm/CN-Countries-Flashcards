# CN-Countries-Flashcards
This python script creates country flashcards to learn chinese.

**Example**

<p align="center">
  <img width="270" alt="Front" src="https://github.com/user-attachments/assets/00c51bd9-f440-414b-af46-39be823138ed" style="margin-right: 10px;" />
  <img width="268" alt="Back" src="https://github.com/user-attachments/assets/4bb7d42a-9986-470d-843b-8de12599ea12" />
</p>



## Acknowledgement

- Python and Tex coded by me [Juan José Sánchez](https://github.com/jj-sm)
- CSV data created and revised by Gabriel Baracaldo

## How to install?

- Git clone this repo. Make sure you have installed the following pip packages:
  - `requests`
  - `asyncio`
  - `aiohttp`
  - `csv`
- Run `main.py`
- After it runs smoothly, run `xelatex flashcards.tex` to compile the final PDF.
 

>[!NOTE]
>This execution was tested with `Python3.1X`

>[!CAUTION]
>This `TeX` project compiles with `XeLaTeX` (For CN support)

## How does it work?
It fetches the flags from the `data/facts.csv` which contains the following headers:

```csv
iso;country;country_cn;capital;capital_cn;lang;lang_cn;fact
```

From this data, using the country ISO it fetches the flag image from `https://flagcdn.com/w320/{iso_code}.png` and saves it under `flags/` route.

Finally, it fetches the other fields from the `csv` to fill the back of the flashcard.


## Future Work

One sketch of the project was to auto generate the translations using `googletrans` library in Python. However, it generated multiple uncompleted translations. Still, this option is 
worth looking in the future.


