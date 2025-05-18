# CN-Countries-Flashcards
This python script creates country flashcards to learn chinese.

**Example**

<p align="center">
  <img width="270" alt="Front" src="https://github.com/user-attachments/assets/00c51bd9-f440-414b-af46-39be823138ed" style="margin-right: 10px;" />
  <img width="268" alt="Back" src="https://github.com/user-attachments/assets/4bb7d42a-9986-470d-843b-8de12599ea12" />
</p>



## Credits

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

>[!CAUTION]
>Keep in mind that for countries with special flag aspect ratios, the script my generate super big flags, for example Nepal or Switzerland flags have different aspect ratios
>and the output pdf will have a really big flag. To correct this, go to the generated `.tex` file and manually change the width for those flags here `{\centering\includegraphics[width=0.3\textwidth]{flags/af.png}}` $\to$ change the `[width=0.3\...` and play with the values until you're happy with the result.
> ```tex
>\card{\centering\includegraphics[width=0.3\textwidth]{flags/af.png}}{
>\begin{tabular}{m{3cm} m{5cm}} \textbf{Afganistan} & \textbf{阿富汗} \\[0.5em] \multicolumn{1}{m{3cm}}{\raggedright Kabul\\喀布尔\\Pashto / Dari\\普什图语 / 达里语} &
>\raggedright \textbf{Fact:} La cometa es un símbolo cultural en Afganistán? Hay competencias tradicionales de corte de cometas… ¡como batallas aéreas con hilo!
>\end{tabular}
>}
> ```




## Future Work

One sketch of the project was to auto generate the translations using `googletrans` library in Python. However, it generated multiple uncompleted translations. Still, this option is 
worth looking in the future.


