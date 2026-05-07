# Emotion Analysis - NLP Project Implementation

Acest proiect implementeaza o aplicatie end-to-end pentru detectia emotiilor din text.
Momentan contine doar partea de cod si documentatia de implementare, fara paper-ul LaTeX.

Emotiile urmarite sunt cele 8 emotii de baza din resursele NRC/Plutchik:
`anger`, `anticipation`, `disgust`, `fear`, `joy`, `sadness`, `surprise`, `trust`.

## Structura

- `emotion_cli.py` - entrypoint CLI usor de rulat din radacina proiectului.
- `src/emotion_analysis/` - codul aplicatiei.
- `data/sample_texts.csv` - exemple mici pentru rularea pe fisier CSV.
- `data/final_eval_texts.csv` - dataset demo etichetat pentru comparatia finala intre metode.
- `tests/` - teste unitare pentru scorare, modelul invatat si pipeline.
- `outputs/` - predictii, metrici si grafice generate de comenzi.
- `../linkuri_extrase/` - resursele colectate din pagina articolului; codul citeste de aici lexiconul NRC Hashtag Emotion.

## Ce face fiecare fisier de cod

Aceasta sectiune este gandita ca o harta rapida pentru corector sau pentru cine vrea sa modifice proiectul.

### Fisiere din radacina folderului `rezolvari`

- `emotion_cli.py`
  Este fisierul care se ruleaza din terminal. El adauga folderul `src/` in `PYTHONPATH` si apeleaza functia `main()` din `src/emotion_analysis/cli.py`. Practic, toate comenzile de tip `py emotion_cli.py predict ...` pornesc de aici.

- `pyproject.toml`
  Contine metadate minimale despre proiectul Python: nume, versiune si faptul ca pachetul sursa se afla in `src/`. Nu adauga dependinte externe.

- `requirements.txt`
  Este lasat explicit pentru predare. Arata ca implementarea nu are dependinte externe si foloseste doar Python standard library.

### Pachetul `src/emotion_analysis/`

- `__init__.py`
  Expune elementele principale ale pachetului: lista de emotii `EMOTIONS`, clasa `EmotionAnalyzer` si functia `run_experiment_suite`. Ajuta daca proiectul este importat ca biblioteca, nu doar rulat din CLI.

- `constants.py`
  Defineste etichetele folosite peste tot in proiect. Lista `EMOTIONS` contine cele 8 emotii NRC/Plutchik: `anger`, `anticipation`, `disgust`, `fear`, `joy`, `sadness`, `surprise`, `trust`.

- `text.py`
  Contine preprocesarea textului: stergere URL-uri, transformare in litere mici, tokenizare, normalizare de tokeni, variante pentru hashtag-uri si reguli simple pentru negatie/intensificatori.

- `resources.py`
  Gaseste si incarca NRC Hashtag Emotion Lexicon din `../linkuri_extrase/`. Transforma fisierul TSV intr-o structura Python usor de folosit: pentru fiecare emotie, un dictionar `termen -> scor`.

- `lexicon_model.py`
  Implementeaza metoda clasica `lexicon`. Pentru fiecare token din text cauta asocieri in lexicon, aduna scorurile pe emotii, aplica reguli simple pentru negatie/intensificatori si returneaza emotia dominanta plus dovezile lexicale.

- `nb_model.py`
  Implementeaza metoda invatata `nb`, un Multinomial Naive Bayes scris manual cu standard library. Modelul este antrenat weak-supervised din termenii etichetati emotional din lexicon si foloseste feature-uri de cuvinte si n-grame de caractere.

- `pipeline.py`
  Coordoneaza metodele disponibile prin clasa `EmotionAnalyzer`. Aceasta poate rula `lexicon`, `nb` sau `hybrid`. Pentru `hybrid`, combina scorurile lexicale si scorurile NB cu o pondere configurabila.

- `io.py`
  Contine functii pentru citirea CSV-urilor de input si scrierea predictiilor in CSV. Este folosit de comenzile `predict-file` si `run-experiments`.

- `metrics.py`
  Calculeaza metricile de evaluare: accuracy, macro-F1, precision/recall/F1 pe fiecare emotie, matrice de confuzie si distributia etichetelor.

- `visualization.py`
  Genereaza grafice SVG simple, fara biblioteci externe. Graficele arata distributia emotiilor si pot fi incluse in raport sau prezentare.

- `experiments.py`
  Ruleaza experimentul final pe `data/final_eval_texts.csv`. Compara metodele `lexicon`, `nb` si `hybrid`, salveaza predictii, metrici, matrice de confuzie si grafice in `outputs/final_experiment/`.

- `cli.py`
  Defineste toate comenzile disponibile in terminal: `predict`, `predict-file`, `evaluate` si `run-experiments`. Tot aici se formateaza output-ul afisat in consola.

### Date, teste si rezultate

- `data/sample_texts.csv`
  Fisier mic de exemple fara etichete, folosit pentru a demonstra comanda `predict-file`.

- `data/final_eval_texts.csv`
  Dataset demo etichetat manual, cu texte scurte din trei domenii: `social`, `news`, `blog`. Este folosit pentru comparatia finala intre metode.

- `tests/test_core.py`
  Teste unitare pentru scorarea lexicala, modelul Naive Bayes, metoda hybrid, metrici, validarea ponderii hybrid si generarea output-urilor experimentale.

- `outputs/predictions.csv`
  Predictii generate pe `data/sample_texts.csv`.

- `outputs/final_experiment/`
  Folder generat de `py emotion_cli.py run-experiments`. Contine tabelele si graficele care pot fi folosite in paper/prezentare.

## Metode implementate

1. `lexicon` - metoda clasica.
   Foloseste NRC Hashtag Emotion Lexicon, unde fiecare termen are o asociere ponderata cu una dintre cele 8 emotii. Textul este tokenizat, termenii gasiti in lexicon contribuie la scorurile emotiilor, iar scorurile sunt normalizate. Sunt incluse reguli simple pentru negatie si intensificatori.

2. `nb` - metoda invatata.
   Antreneaza un model Multinomial Naive Bayes scris doar cu Python standard library. Datele de antrenare sunt generate din termenii etichetati emotional din NRC Hashtag Emotion Lexicon. Modelul foloseste feature-uri de cuvinte si n-grame de caractere.

3. `hybrid` - metoda combinata.
   Combina scorul lexical cu predictia Naive Bayes. Implicit, scorul final este 85% lexicon si 15% model invatat, iar ponderea se poate schimba cu `--hybrid-weight`. Astfel, sistemul pastreaza interpretabilitatea lexicala si adauga un semnal invatat fara sa suprascrie complet resursa NRC.

## Rulare

Nu sunt dependinte externe:

```powershell
py emotion_cli.py predict --text "I am happy but also a little afraid." --method hybrid
```

Rulare doar cu metoda clasica:

```powershell
py emotion_cli.py predict --text "The announcement was shocking and exciting." --method lexicon
```

Rulare doar cu modelul invatat:

```powershell
py emotion_cli.py predict --text "I feel furious about this delay." --method nb
```

Output JSON:

```powershell
py emotion_cli.py predict --text "I trust the team and I feel hopeful." --json
```

Predictii pe CSV:

```powershell
py emotion_cli.py predict-file --input data/sample_texts.csv --output outputs/predictions.csv --method hybrid
```

CSV-ul de intrare trebuie sa aiba coloana `text`. Daca textul este in alta coloana:

```powershell
py emotion_cli.py predict-file --input my_data.csv --text-column message --output outputs/my_predictions.csv
```

Evaluarea modelului Naive Bayes pe un split held-out din lexicon:

```powershell
py emotion_cli.py evaluate
```

Rularea experimentului final, cu comparatie intre `lexicon`, `nb` si `hybrid`:

```powershell
py emotion_cli.py run-experiments
```

Pentru a testa alta pondere in metoda hybrid:

```powershell
py emotion_cli.py run-experiments --hybrid-weight 0.75
```

Comanda genereaza in `outputs/final_experiment/`:

- `metrics.json` - toate metricile, inclusiv per-label si pe domeniu.
- `method_comparison.csv` - tabel comparativ pentru metode.
- `predictions_lexicon.csv`, `predictions_nb.csv`, `predictions_hybrid.csv` - predictii complete.
- `confusion_lexicon.csv`, `confusion_nb.csv`, `confusion_hybrid.csv` - matrice de confuzie.
- `gold_distribution.svg` si `predicted_distribution_*.svg` - grafice simple pentru raport/prezentare.

## Resursa lexicala

Implicit, codul cauta lexiconul aici:

```text
../linkuri_extrase/archives/061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2.txt
```

Se poate da si explicit:

```powershell
py emotion_cli.py --lexicon "path\to\NRC-Hashtag-Emotion-Lexicon-v0.2.txt" predict --text "I am excited."
```

Lexiconul NRC este folosit pentru scop educational/research. Pentru paper si prezentare, trebuie citate resursele NRC mentionate in README-ul lexiconului din `../linkuri_extrase`.

## Testare

```powershell
$env:PYTHONPATH="src"; py -m unittest discover -s tests
```

## Flux recomandat pentru proiectul final

1. Ruleaza testele.
2. Ruleaza `py emotion_cli.py run-experiments`.
3. Alege metoda finala in functie de `method_comparison.csv`; pe datasetul demo curent, metoda lexicala este baseline-ul cel mai puternic.
4. Foloseste graficele SVG din acelasi folder in prezentare.

## Note pentru paper

- Comparatie intre `lexicon`, `nb` si `hybrid`.
- Analiza pe tipuri de text: stiri, bloguri, social media.
- Interpretabilitate: pentru metoda lexicala se pot raporta termenii care au contribuit la scor.
- Limite: lexiconul este in engleza, social-media oriented, iar modelul NB este weakly supervised, nu antrenat pe texte lungi adnotate manual.
