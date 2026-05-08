# Emotion Analysis - Detectarea emotiilor in text

Acest repository contine implementarea proiectului de NLP pentru tema **Emotion analysis - detect the emotions in a text**. Partea de cod construieste un sistem complet care citeste texte, detecteaza emotia dominanta, compara mai multe metode de predictie si salveaza rezultate in fisiere CSV/JSON/SVG.

Documentul de fata explica structura proiectului si rolul fiecarui fisier important. Folderul `latex/` si fisierul PowerPoint sunt excluse intentionat din aceasta documentatie, deoarece cerinta de aici este pentru partea de cod, date, rezultate si resurse auxiliare.

## Pe Scurt

Proiectul implementeaza trei metode de analiza emotionala:

- `lexicon`: metoda bazata pe NRC Hashtag Emotion Lexicon.
- `nb`: model Naive Bayes antrenat din asocieri emotionale din lexicon.
- `hybrid`: combinatie intre scorurile lexiconului si scorurile Naive Bayes.

Sistemul lucreaza cu 8 emotii de tip Plutchik:

- `anger`
- `anticipation`
- `disgust`
- `fear`
- `joy`
- `sadness`
- `surprise`
- `trust`

Datasetul principal de evaluare se afla in `cod/data/final_eval_texts.csv` si contine peste 500 de exemple. Output-urile finale sunt generate in `cod/outputs/final_experiment/`.

## Structura Generala

```text
.
|-- README.md
|-- cerinte.md
|-- cerinte_proiect.md
|-- pagina.html
|-- cod/
|   |-- emotion_cli.py
|   |-- EXPLICATII.md
|   |-- pyproject.toml
|   |-- requirements.txt
|   |-- data/
|   |-- outputs/
|   |-- src/
|   |   `-- emotion_analysis/
|   `-- tests/
|-- linkuri_extrase/
|-- semeval-code-quality/
`-- tools/
    `-- SemEval-2026-Task13/
```

Nu sunt documentate aici:

- `latex/`: documentul stiintific LaTeX si fisierele generate de compilare.
- `prezentare powerpoint.pptx`: prezentarea PowerPoint.

## Cum Rulezi Proiectul

Intra in folderul de cod:

```powershell
cd "C:\Users\matei\Desktop\NLP Final\cod"
```

Ruleaza o predictie pentru un singur text:

```powershell
python emotion_cli.py predict --text "I am happy but also a little afraid." --method hybrid
```

Ruleaza predictii pentru fisierul de exemple:

```powershell
python emotion_cli.py predict-file --input data/sample_texts.csv --output outputs/predictions.csv --method hybrid
```

Ruleaza experimentul complet pe datasetul final:

```powershell
python emotion_cli.py run-experiments
```

Ruleaza testele:

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
```

## Dependinte

Partea principala a proiectului din `cod/` foloseste doar biblioteca standard Python. Nu are nevoie de `numpy`, `pandas`, `scikit-learn` sau alte librarii pentru rularea sistemului de emotion analysis.

Fisierul `semeval-code-quality/scripts/detect_code_file.py` este separat de proiectul de emotion analysis si foloseste dependinte externe precum `pandas` si `scikit-learn`, deoarece antreneaza un detector local pe datele SemEval.

## Fluxul Principal

1. Textul este citit din linia de comanda sau dintr-un CSV.
2. Textul este normalizat si impartit in tokeni.
3. Modelul bazat pe lexicon cauta termeni emotionali in NRC Hashtag Emotion Lexicon.
4. Modelul Naive Bayes calculeaza probabilitati pe baza trasaturilor de cuvant si caractere.
5. Modelul hybrid combina scorurile lexiconului cu scorurile Naive Bayes.
6. Emotia cu scorul cel mai mare devine `dominant_emotion`.
7. Rezultatele sunt salvate in CSV, JSON si SVG pentru analiza si prezentare.

## Folderul `cod/`

Folderul `cod/` este partea principala a proiectului. Aici se afla implementarea efectiva, datele de intrare, output-urile, configuratia si testele.

### `cod/emotion_cli.py`

Fisier wrapper pentru pornirea aplicatiei din linia de comanda.

Rol:

- Adauga automat folderul `cod/src` in `sys.path`.
- Importa functia `main()` din `emotion_analysis.cli`.
- Permite rularea simpla cu `python emotion_cli.py ...`, fara instalarea pachetului.

Acest fisier nu contine logica de analiza emotionala. El doar face legatura intre terminal si pachetul Python din `src/`.

### `cod/EXPLICATII.md`

Document explicativ mai vechi pentru implementare.

Rol:

- Ofera explicatii despre componentele proiectului.
- Poate fi folosit ca material auxiliar langa README.
- Nu este folosit de cod la rulare.

README-ul de fata este documentul principal si mai complet pentru structura proiectului.

### `cod/pyproject.toml`

Fisier de configurare Python pentru pachet.

Rol:

- Defineste numele proiectului: `emotion-analysis-nlp-project`.
- Defineste versiunea: `0.1.0`.
- Specifica faptul ca proiectul cere Python `>=3.10`.
- Indica faptul ca pachetul se gaseste in `cod/src`.

Este util daca proiectul este instalat ca pachet Python.

### `cod/requirements.txt`

Fisier pentru dependinte.

Rol:

- Mentioneaza ca partea principala nu are dependinte externe.
- Confirma ca implementarea de emotion analysis foloseste doar Python standard library.

### `cod/data/`

Folderul cu date de intrare.

#### `cod/data/final_eval_texts.csv`

Datasetul principal de evaluare.

Coloane:

- `id`: identificator unic pentru fiecare exemplu.
- `domain`: tipul textului, de exemplu `social`, `news`, `blog`.
- `label`: emotia corecta asteptata.
- `text`: textul care trebuie clasificat.

Rol:

- Este folosit de comanda `run-experiments`.
- Permite evaluarea metodelor `lexicon`, `nb` si `hybrid`.
- Contine peste 500 de exemple pentru o evaluare mai serioasa.
- Este baza pentru fisierele generate in `cod/outputs/final_experiment/`.

#### `cod/data/sample_texts.csv`

Dataset mic pentru testare rapida.

Coloane:

- `id`: identificator pentru exemplu.
- `text`: textul pe care sistemul trebuie sa il analizeze.

Rol:

- Este folosit de comanda `predict-file`.
- Produce fisierul `cod/outputs/predictions.csv`.
- Este util pentru demonstratii rapide, fara etichete gold.

### `cod/outputs/`

Folderul cu rezultate generate.

#### `cod/outputs/predictions.csv`

Fisier generat prin comanda `predict-file`.

Rol:

- Contine predictiile pentru textele din `sample_texts.csv`.
- Include emotia dominanta, scorurile pentru fiecare emotie, increderea si acoperirea lexiconului.

Coloane importante:

- `ID`: identificatorul randului.
- `source_id`: id-ul original din fisierul sursa.
- `text`: textul analizat.
- `method`: metoda folosita.
- `dominant_emotion`: emotia aleasa de model.
- `prediction`: aceeasi eticheta ca `dominant_emotion`, pastrata pentru compatibilitate cu formate de evaluare.
- `confidence`: scorul emotiei dominante.
- `coverage`: proportia tokenilor acoperiti de lexicon.
- `score_anger`, `score_anticipation`, ..., `score_trust`: scoruri normalizate pentru fiecare emotie.

### `cod/outputs/final_experiment/`

Folderul cu toate artefactele experimentului final.

#### `cod/outputs/final_experiment/metrics.json`

Fisier JSON cu rezumatul complet al experimentului.

Rol:

- Pastreaza datasetul folosit.
- Pastreaza numarul de randuri.
- Pastreaza greutatea metodei hybrid.
- Pastreaza metricile pentru fiecare metoda.
- Pastreaza distributii si rezultate pe domenii.

#### `cod/outputs/final_experiment/method_comparison.csv`

Tabel comparativ intre metode.

Rol:

- Compara `lexicon`, `nb` si `hybrid`.
- Include `accuracy`, `macro_precision`, `macro_recall`, `macro_f1` si `total`.
- Este unul dintre cele mai importante fisiere pentru raportarea rezultatelor.

#### `cod/outputs/final_experiment/domain_metrics.csv`

Metrici impartite pe domeniu.

Rol:

- Arata performanta fiecarei metode separat pe `social`, `news` si `blog`.
- Ajuta la analiza daca modelul functioneaza mai bine pe un anumit tip de text.

#### `cod/outputs/final_experiment/predictions_lexicon.csv`

Predictiile complete produse de metoda bazata pe lexicon.

Rol:

- Arata ce emotie a prezis metoda `lexicon` pentru fiecare rand din datasetul final.
- Include scoruri pentru toate emotiile.
- Include eticheta corecta `label`, astfel incat predictia poate fi comparata cu raspunsul asteptat.

#### `cod/outputs/final_experiment/predictions_nb.csv`

Predictiile complete produse de modelul Naive Bayes.

Rol:

- Arata rezultatele metodei `nb`.
- Este util pentru a vedea unde modelul invatat din lexicon greseste sau generalizeaza diferit fata de metoda rule-based.

#### `cod/outputs/final_experiment/predictions_hybrid.csv`

Predictiile complete produse de metoda hybrid.

Rol:

- Arata rezultatul combinatiei dintre `lexicon` si `nb`.
- Este fisierul principal pentru analiza metodei finale propuse.

#### `cod/outputs/final_experiment/confusion_lexicon.csv`

Matricea de confuzie pentru metoda `lexicon`.

Rol:

- Randurile reprezinta etichetele reale.
- Coloanele reprezinta etichetele prezise.
- Arata ce emotii sunt confundate intre ele.

#### `cod/outputs/final_experiment/confusion_nb.csv`

Matricea de confuzie pentru metoda `nb`.

Rol:

- Evidentiaza greselile modelului Naive Bayes.
- Ajuta la intelegerea limitelor modelului invatat din termeni de lexicon.

#### `cod/outputs/final_experiment/confusion_hybrid.csv`

Matricea de confuzie pentru metoda `hybrid`.

Rol:

- Arata erorile metodei finale.
- Este utila pentru sectiunea de error analysis.

#### `cod/outputs/final_experiment/gold_distribution.csv`

Distributia etichetelor reale.

Rol:

- Arata cate exemple exista pentru fiecare emotie in dataset.
- Confirma echilibrarea datasetului.

#### `cod/outputs/final_experiment/gold_distribution.svg`

Grafic SVG pentru distributia etichetelor reale.

Rol:

- Vizualizeaza distributia din `gold_distribution.csv`.
- Poate fi folosit in raport sau prezentare.

#### `cod/outputs/final_experiment/predicted_distribution_lexicon.csv`

Distributia emotiilor prezise de metoda `lexicon`.

Rol:

- Arata daca metoda bazata pe lexicon favorizeaza anumite emotii.

#### `cod/outputs/final_experiment/predicted_distribution_nb.csv`

Distributia emotiilor prezise de metoda `nb`.

Rol:

- Arata comportamentul modelului Naive Bayes pe tot datasetul.

#### `cod/outputs/final_experiment/predicted_distribution_hybrid.csv`

Distributia emotiilor prezise de metoda `hybrid`.

Rol:

- Arata echilibrul predictiilor metodei finale.

#### `cod/outputs/final_experiment/predicted_distribution_lexicon.svg`

Grafic SVG pentru distributia predictiilor `lexicon`.

#### `cod/outputs/final_experiment/predicted_distribution_nb.svg`

Grafic SVG pentru distributia predictiilor `nb`.

#### `cod/outputs/final_experiment/predicted_distribution_hybrid.svg`

Grafic SVG pentru distributia predictiilor `hybrid`.

Rol comun pentru fisierele SVG:

- Ofera vizualizari rapide ale distributiei predictiilor.
- Sunt generate automat de `visualization.py`.

## Folderul `cod/src/emotion_analysis/`

Acesta este pachetul principal Python.

### `cod/src/emotion_analysis/__init__.py`

Fisierul de initializare al pachetului.

Rol:

- Marcheaza folderul `emotion_analysis` ca pachet Python.
- Expune public `EMOTIONS`, `EmotionAnalyzer` si `run_experiment_suite`.
- Permite importuri simple din alte fisiere.

### `cod/src/emotion_analysis/constants.py`

Defineste constantele globale.

Contine:

- `EMOTIONS`: cele 8 emotii folosite in proiect.
- `SENTIMENTS`: etichete generale pozitive/negative, pastrate pentru extensii.

Rol:

- Evita duplicarea listei de emotii in mai multe fisiere.
- Pastreaza ordinea stabila a etichetelor in CSV-uri, metrici si grafice.

### `cod/src/emotion_analysis/text.py`

Modul pentru preprocesarea textului.

Contine:

- expresii regulate pentru URL-uri si tokenizare;
- lista de negatii;
- lista de intensificatori;
- functii pentru normalizarea textului si a tokenilor.

Functii principale:

- `normalize_text(text)`: transforma textul in lowercase si inlocuieste URL-urile.
- `normalize_token(token)`: curata semnele de punctuatie si reduce repetitiile exagerate de caractere.
- `tokenize(text)`: imparte textul in tokeni.
- `token_variants(token)`: genereaza variante pentru hashtag-uri si forme posesive.
- `has_recent_negation(tokens, index)`: verifica daca exista o negatie aproape de token.
- `has_recent_intensifier(tokens, index)`: verifica daca exista un intensificator aproape de token.

Rol:

- Asigura aceeasi preprocesare pentru toate modelele.
- Ajuta modelul lexical sa tina cont de contexte precum `not happy` sau `very happy`.

### `cod/src/emotion_analysis/resources.py`

Modul pentru incarcarea resurselor externe.

Contine:

- calea implicita catre NRC Hashtag Emotion Lexicon;
- clasa `LexiconEntry`;
- functii pentru gasirea si incarcarea lexiconului.

Functii principale:

- `project_root()`: returneaza radacina proiectului de cod.
- `workspace_root()`: returneaza radacina workspace-ului.
- `default_lexicon_path()`: cauta lexiconul in locatia asteptata sau citeste variabila `EMOTION_LEXICON_PATH`.
- `resolve_lexicon_path(path)`: valideaza existenta fisierului de lexicon.
- `load_hashtag_lexicon(...)`: incarca lexiconul ca dictionar pe emotii.
- `load_hashtag_entries(...)`: incarca intrari individuale de tip `LexiconEntry`.

Rol:

- Conecteaza codul proiectului cu resursele extrase in `linkuri_extrase/`.
- Permite folosirea unei cai custom prin `--lexicon` sau `EMOTION_LEXICON_PATH`.

### `cod/src/emotion_analysis/lexicon_model.py`

Modelul rule-based bazat pe lexicon.

Clase:

- `LexiconHit`: pastreaza o potrivire gasita in lexicon.
- `WeightedEmotionLexicon`: modelul care calculeaza scorurile emotionale.

Functii:

- `recent_context_multiplier(tokens, token_index)`: modifica greutatea unui termen daca apare langa negatii sau intensificatori.
- `normalize_emotion_totals(emotion_totals)`: transforma scorurile brute in scoruri normalizate.
- `summarize_lexicon_hits(hits)`: pastreaza cele mai importante dovezi lexicale.

Rol:

- Cauta tokenii textului in lexiconul NRC.
- Aduna scoruri pentru fiecare emotie.
- Returneaza emotia dominanta, increderea, acoperirea lexiconului si dovezile gasite.

### `cod/src/emotion_analysis/nb_model.py`

Modelul Naive Bayes.

Clase:

- `TrainingExample`: reprezinta un exemplu de antrenare cu text, eticheta si greutate.
- `NaiveBayesNotFittedError`: eroare ridicata daca modelul este folosit inainte de antrenare.
- `EmotionNaiveBayes`: implementarea modelului Naive Bayes.

Functii importante:

- `train_nb_from_lexicon(...)`: construieste exemple de antrenare din NRC lexicon si antreneaza modelul.
- `evaluate_nb_from_lexicon(...)`: evalueaza modelul pe o impartire train/test a intrarilor din lexicon.
- `count_emotion_token_features(text)`: extrage trasaturi de cuvant si n-grame de caractere.
- `nrc_entry_to_training_example(entry)`: transforma o intrare de lexicon in exemplu de training.
- `looks_like_training_phrase(term)`: filtreaza termeni inutili, linkuri si mention-uri.
- `normalize_log_emotion_scores(log_scores)`: transforma scorurile logaritmice in probabilitati.

Rol:

- Ofera o metoda invatata, nu doar bazata pe potriviri exacte.
- Poate generaliza prin trasaturi de caractere, de exemplu pentru forme similare ale cuvintelor.

### `cod/src/emotion_analysis/pipeline.py`

Modulul de orchestrare a modelelor.

Clasa principala:

- `EmotionAnalyzer`

Rol:

- Ofera interfata unica pentru `lexicon`, `nb` si `hybrid`.
- Creeaza modelul lexical.
- Creeaza modelul Naive Bayes la nevoie, prin lazy loading.
- Combina scorurile pentru metoda `hybrid`.

Metoda principala:

- `analyze(text, method="hybrid")`: returneaza predictia si scorurile pentru un text.

Parametru important:

- `hybrid_lexicon_weight`: controleaza cat de mult conteaza scorul lexical in metoda hybrid.

### `cod/src/emotion_analysis/io.py`

Modul pentru citire si scriere CSV.

Constante:

- `ID_COLUMN = "ID"`
- `SOURCE_ID_COLUMN = "source_id"`
- `PREDICTION_COLUMN = "prediction"`

Functii:

- `read_text_rows(path, text_column="text")`: citeste randuri dintr-un CSV si verifica existenta coloanei de text.
- `write_prediction_rows(path, rows)`: scrie predictii in CSV.
- `flatten_prediction(source_row, prediction)`: transforma rezultatul intern al modelului intr-un rand plat pentru CSV.

Rol:

- Tine formatul output-urilor stabil.
- Evita duplicarea logicii de scriere CSV intre CLI si experimente.

### `cod/src/emotion_analysis/metrics.py`

Modul pentru metrici de evaluare.

Functii:

- `classification_metrics(gold_labels, predicted_labels)`: calculeaza accuracy, macro precision, macro recall, macro F1, metrici per eticheta si matricea de confuzie.
- `confusion_matrix(gold_labels, predicted_labels)`: construieste matricea de confuzie.
- `label_distribution(labels)`: numara aparitiile fiecarei emotii.

Rol:

- Evalueaza modelele intr-un mod consecvent.
- Produce datele folosite de `experiments.py`.

### `cod/src/emotion_analysis/visualization.py`

Modul pentru grafice SVG.

Contine:

- paleta de culori pentru fiecare emotie;
- functia de scriere a graficelor de distributie.

Functii:

- `write_distribution_svg(path, distribution, title=...)`: genereaza un grafic bar chart in SVG.
- `escape_xml(value)`: protejeaza caracterele speciale pentru XML/SVG.

Rol:

- Genereaza automat grafice pentru distributia etichetelor reale si a predictiilor.
- Nu depinde de librarii externe precum `matplotlib`.

### `cod/src/emotion_analysis/experiments.py`

Modulul pentru rularea experimentelor finale.

Functia principala:

- `run_experiment_suite(...)`

Rol:

- Citeste datasetul final.
- Valideaza etichetele.
- Ruleaza metodele `lexicon`, `nb` si `hybrid`.
- Calculeaza metrici.
- Scrie predictii, matrice de confuzie, distributii, grafice si JSON final.

Functii auxiliare:

- `check_labels(...)`: verifica daca etichetele din dataset sunt valide.
- `check_methods(...)`: verifica metodele cerute.
- `semeval_row_id(row)`: alege identificatorul randului.
- `scores_by_domain(...)`: calculeaza metrici pe domenii.
- `write_preds_csv(...)`: scrie fisierele de predictii ale experimentului.
- `write_compare_csv(...)`: scrie comparatia intre metode.
- `write_domain_csv(...)`: scrie metricile pe domenii.
- `write_conf_csv(...)`: scrie matricea de confuzie.
- `write_dist_csv(...)`: scrie distributii in CSV.

Fisiere generate:

- `metrics.json`
- `method_comparison.csv`
- `domain_metrics.csv`
- `predictions_lexicon.csv`
- `predictions_nb.csv`
- `predictions_hybrid.csv`
- `confusion_lexicon.csv`
- `confusion_nb.csv`
- `confusion_hybrid.csv`
- distributii CSV si SVG

### `cod/src/emotion_analysis/cli.py`

Interfata de linie de comanda.

Comenzi disponibile:

- `predict`: analizeaza un singur text.
- `predict-file`: analizeaza un fisier CSV.
- `evaluate`: evalueaza modelul Naive Bayes pe o impartire din lexicon.
- `run-experiments`: ruleaza experimentul complet pe datasetul final.

Functii:

- `build_parser()`: construieste parserul `argparse`.
- `main(argv=None)`: executa comanda ceruta.
- `print_prediction(...)`: afiseaza predictia pentru un text.
- `print_evaluation(...)`: afiseaza evaluarea NB.
- `print_experiment_summary(...)`: afiseaza sumarul experimentului.
- `top_scores(...)`: sorteaza scorurile emotiilor.

Rol:

- Face proiectul usor de folosit din terminal.
- Leaga codul intern de comenzile pe care le ruleaza utilizatorul.

## Detaliu Tehnic Pentru Fisierele Python

Aceasta sectiune intra mai adanc in partea de cod Python. Scopul ei este sa explice nu doar ce face fiecare fisier, ci si de ce exista, ce date primeste, ce date returneaza si cum interactioneaza cu celelalte module.

### Fluxul De Importuri

```text
cod/emotion_cli.py
`-- emotion_analysis.cli
    |-- emotion_analysis.experiments
    |-- emotion_analysis.io
    |-- emotion_analysis.nb_model
    `-- emotion_analysis.pipeline
        |-- emotion_analysis.lexicon_model
        |   |-- emotion_analysis.resources
        |   `-- emotion_analysis.text
        `-- emotion_analysis.nb_model
            |-- emotion_analysis.resources
            `-- emotion_analysis.text
```

Interpretare:

- `emotion_cli.py` este doar punctul de pornire.
- `cli.py` transforma comenzile din terminal in apeluri de functii.
- `pipeline.py` decide ce model se foloseste.
- `lexicon_model.py` si `nb_model.py` sunt cele doua componente de predictie.
- `experiments.py` ruleaza evaluarea completa.
- `io.py`, `metrics.py` si `visualization.py` sunt module suport.

### `cod/emotion_cli.py` In Detaliu

Acest fisier este un wrapper minim, dar important pentru rularea proiectului.

Problema pe care o rezolva:

- Codul sursa este in `cod/src/emotion_analysis/`.
- Daca rulezi direct `python emotion_cli.py`, Python nu stie automat unde este pachetul `emotion_analysis`.
- Fisierul adauga `cod/src` in `sys.path`, apoi importa `main()`.

Componente:

- `ROOT = Path(__file__).resolve().parent`: gaseste folderul `cod`.
- `SRC = ROOT / "src"`: construieste calea catre codul sursa.
- `sys.path.insert(0, str(SRC))`: permite importul pachetului local.
- `from emotion_analysis.cli import main`: aduce functia principala CLI.
- `raise SystemExit(main())`: ruleaza programul si returneaza codul de iesire corect.

De ce este util:

- Nu trebuie sa instalezi pachetul cu `pip install -e .`.
- Proiectul poate fi testat rapid de profesor direct din folderul `cod/`.
- Linia de comanda ramane simpla.

### `cod/src/emotion_analysis/__init__.py` In Detaliu

Acest fisier defineste interfata publica a pachetului.

Exporturi:

- `EMOTIONS`: lista stabila de emotii.
- `EmotionAnalyzer`: clasa principala pentru predictie.
- `run_experiment_suite`: functia principala pentru experimente.

De ce conteaza:

- Permite importuri curate, de exemplu:

```python
from emotion_analysis import EmotionAnalyzer
```

in loc de:

```python
from emotion_analysis.pipeline import EmotionAnalyzer
```

Acest fisier nu contine algoritmi. Rolul lui este de organizare si expunere a API-ului.

### `cod/src/emotion_analysis/constants.py` In Detaliu

Acest modul centralizeaza etichetele.

Constanta `EMOTIONS`:

```python
EMOTIONS = (
    "anger",
    "anticipation",
    "disgust",
    "fear",
    "joy",
    "sadness",
    "surprise",
    "trust",
)
```

Rol tehnic:

- Stabileste ordinea coloanelor `score_anger`, `score_anticipation`, etc.
- Stabileste ordinea randurilor/coloanelor din matricea de confuzie.
- Stabileste ordinea graficelor SVG.
- Reduce riscul de a scrie gresit o eticheta in mai multe fisiere.

Unde este folosita:

- `lexicon_model.py`: initializeaza scoruri pentru fiecare emotie.
- `nb_model.py`: creeaza clasele modelului Naive Bayes.
- `metrics.py`: calculeaza metrici pentru aceleasi etichete.
- `io.py`: scrie scorurile pe coloane.
- `experiments.py`: valideaza labelurile datasetului.
- `visualization.py`: deseneaza distributiile.
- `cli.py`: afiseaza metrici si scoruri.

Constanta `SENTIMENTS`:

- Nu este esentiala pentru experimentul curent.
- Este pastrata pentru extensii posibile de tip pozitiv/negativ.

### `cod/src/emotion_analysis/text.py` In Detaliu

Acest fisier pregateste textul pentru modele. Este important pentru ca aceeasi propozitie poate aparea cu majuscule, linkuri, hashtaguri sau repetitii de caractere.

Exemple de probleme rezolvate:

- `HAPPY!!!` devine token comparabil cu `happy`.
- `soooo happy` reduce repetitia exagerata.
- `#happy` poate fi interpretat si ca `happy`.
- `https://...` este eliminat din analiza emotionala.
- `not happy` este tratat diferit fata de `happy`.

Expresii regulate:

- `URL_PATTERN`: detecteaza URL-uri care in general nu ajuta la emotie.
- `TOKEN_PATTERN`: extrage cuvinte, hashtaguri si semne precum `!` sau `?`.
- `LONG_CHAR_RUN`: detecteaza acelasi caracter repetat de minimum 3 ori.

Setul `NEGATIONS`:

- Include negatii in engleza si cateva forme romanesti.
- Exemple: `not`, `never`, `can't`, `nu`, `nimic`.
- Este folosit pentru a reduce scorul emotional al termenilor apropiati.

Setul `INTENSIFIERS`:

- Include cuvinte care intensifica emotia.
- Exemple: `very`, `really`, `extremely`, `foarte`, `super`.
- Este folosit pentru a creste scorul termenilor apropiati.

Functia `normalize_text(text)`:

- Input: text brut.
- Output: text lowercase, cu URL-urile inlocuite.
- Este primul pas in tokenizare.

Functia `normalize_token(token)`:

- Input: un token extras prin regex.
- Output: token curatat.
- Elimina ghilimele, punctuatie laterala si normalizeaza repetitiile.

Functia `tokenize(text)`:

- Input: text brut.
- Output: lista de tokeni normalizati.
- Omite tokenul `url`, deoarece linkurile nu sunt utile pentru predictie.

Functia `token_variants(token)`:

- Input: un token.
- Output: variante posibile ale tokenului.
- Pentru `#joy`, produce si `joy`.
- Pentru `mother's`, produce si `mother`.

Functia `has_recent_negation(tokens, index)`:

- Input: lista de tokeni si pozitia unui token.
- Output: `True` daca exista negatie inaintea tokenului, intr-o fereastra mica.
- Este folosita de modelul lexical pentru a reduce scorul.

Functia `has_recent_intensifier(tokens, index)`:

- Input: lista de tokeni si pozitia unui token.
- Output: `True` daca exista intensificator inaintea tokenului.
- Este folosita de modelul lexical pentru a mari scorul.

Legatura cu restul proiectului:

- `lexicon_model.py` foloseste tokenizarea si contextul de negatie/intensificare.
- `nb_model.py` foloseste tokenizarea pentru feature extraction.

### `cod/src/emotion_analysis/resources.py` In Detaliu

Acest fisier rezolva legatura dintre cod si lexiconul NRC descarcat local.

Problema pe care o rezolva:

- Lexiconul nu este in `cod/`, ci in `linkuri_extrase/archives/...`.
- Proiectul trebuie sa gaseasca lexiconul indiferent daca este rulat din `cod/` sau din radacina workspace-ului.
- Utilizatorul trebuie sa poata oferi o cale custom.

Constanta `DEFAULT_LEXICON_RELATIVE`:

- Pastreaza calea relativa catre `NRC-Hashtag-Emotion-Lexicon-v0.2.txt`.
- Aceasta este resursa principala pentru modelul lexical si pentru antrenarea NB.

Clasa `LexiconEntry`:

- Este un `dataclass` imutabil.
- Campuri:
  - `emotion`: una dintre cele 8 emotii.
  - `term`: termenul asociat emotiei.
  - `score`: scorul numeric din lexicon.

Functia `project_root()`:

- Returneaza folderul `cod`.
- Este folosita pentru cai relative.

Functia `workspace_root()`:

- Returneaza radacina proiectului mare, adica folderul care contine `cod/` si `linkuri_extrase/`.
- Este necesara deoarece lexiconul se afla in afara folderului `cod/`.

Functia `default_lexicon_path()`:

- Verifica mai intai variabila de mediu `EMOTION_LEXICON_PATH`.
- Daca nu exista, cauta lexiconul in locatia standard.
- Returneaza calea cea mai probabila catre lexicon.

Functia `resolve_lexicon_path(path)`:

- Accepta o cale explicita sau foloseste calea implicita.
- Daca primeste cale relativa, incearca sa o rezolve fata de `cod/` si fata de workspace.
- Ridica `FileNotFoundError` daca lexiconul nu exista.

Functia `load_hashtag_entries(...)`:

- Citeste fisierul NRC linie cu linie.
- Asteapta format cu 3 coloane separate prin tab:
  - emotie;
  - termen;
  - scor.
- Ignora linii invalide.
- Ignora emotii care nu sunt in `EMOTIONS`.
- Poate limita numarul de intrari pe emotie.
- Poate filtra dupa scor minim.
- Normalizeaza termenii folosind `normalize_token`.
- Returneaza lista de `LexiconEntry`.

Functia `load_hashtag_lexicon(...)`:

- Foloseste `load_hashtag_entries`.
- Returneaza dictionar de forma:

```python
{
    "joy": {"happy": 2.4, "smile": 1.8},
    "anger": {"furious": 2.1},
    ...
}
```

De ce exista doua functii de incarcare:

- `load_hashtag_entries` este utila pentru training NB, unde fiecare termen devine exemplu.
- `load_hashtag_lexicon` este utila pentru modelul rule-based, unde cautarea rapida pe emotie conteaza.

### `cod/src/emotion_analysis/lexicon_model.py` In Detaliu

Acest fisier implementeaza metoda `lexicon`.

Ideea metodei:

- Daca textul contine termeni asociati unei emotii in lexiconul NRC, acea emotie primeste scor.
- Termenii cu scor mai mare in lexicon contribuie mai mult.
- Negatiile reduc contributia.
- Intensificatorii cresc contributia.

Clasa `LexiconHit`:

- Pastreaza o dovada gasita in text.
- Campuri:
  - `emotion`: emotia gasita.
  - `term`: termenul din lexicon.
  - `token_index`: pozitia tokenului in text.
  - `contribution`: scorul adaugat.

Clasa `WeightedEmotionLexicon`:

- Este modelul propriu-zis.
- Poate primi direct un dictionar de lexicon, util in teste.
- Daca nu primeste dictionar, incarca lexiconul din fisier.

Constructorul `__init__`:

- Parametri:
  - `lexicon`: lexicon deja incarcat, optional.
  - `lexicon_path`: cale catre fisierul NRC, optional.
  - `max_entries_per_emotion`: limita de intrari pe emotie.
- Creeaza `self.lexicon`.

Metoda `score(text)`:

- Input: text brut.
- Output: dictionar cu predictia completa.
- Pasi:
  - tokenizare;
  - initializare scoruri brute cu 0 pentru fiecare emotie;
  - parcurgere tokeni;
  - generare variante de token;
  - cautare in lexicon pentru fiecare emotie;
  - aplicare multiplicator de context;
  - normalizare scoruri;
  - alegere emotie dominanta;
  - calcul coverage;
  - sumarizare dovezi.

Chei importante in output:

- `method`: mereu `lexicon`.
- `text`: textul original.
- `tokens`: tokenii folositi.
- `raw_scores`: scoruri inainte de normalizare.
- `scores`: scoruri normalizate.
- `dominant_emotion`: emotia castigatoare.
- `confidence`: scorul emotiei castigatoare.
- `coverage`: procentul tokenilor care au potriviri in lexicon.
- `matches`: dovezi lexicale.

Functia `recent_context_multiplier(tokens, token_index)`:

- Porneste de la `1.0`.
- Daca exista negatie recenta, inmulteste cu `0.35`.
- Daca exista intensificator recent, inmulteste cu `1.35`.
- Returneaza multiplicatorul final.

Functia `normalize_emotion_totals(emotion_totals)`:

- Elimina scorurile negative prin `max(score, 0.0)`.
- Calculeaza suma totala.
- Daca totalul este 0, returneaza 0 pentru toate emotiile.
- Altfel imparte fiecare scor la total.

Functia `summarize_lexicon_hits(hits)`:

- Grupeaza potrivirile dupa `(emotion, term)`.
- Aduna contributiile repetate.
- Sorteaza descrescator.
- Pastreaza primele dovezi.

Avantaje:

- Este interpretabil.
- Arata dovezi prin `matches`.
- Nu are nevoie de training greu.

Limitari:

- Depinde de acoperirea lexiconului.
- Poate rata formulari emotionale care nu contin termeni din lexicon.
- Poate confunda emotii apropiate lexical.

### `cod/src/emotion_analysis/nb_model.py` In Detaliu

Acest fisier implementeaza metoda `nb`, adica un model Naive Bayes antrenat din lexicon.

Ideea metodei:

- Lexiconul NRC contine termeni si scoruri emotionale.
- Fiecare termen poate fi transformat intr-un exemplu slab-supervizat.
- Modelul invata trasaturi de cuvant si caractere pentru fiecare emotie.
- Apoi poate prezice emotii pentru texte noi.

Clasa `TrainingExample`:

- Campuri:
  - `text`: textul exemplului.
  - `label`: emotia corecta.
  - `weight`: greutatea exemplului.
- Greutatea permite ca termenii cu scor NRC mai mare sa conteze mai mult.

Clasa `NaiveBayesNotFittedError`:

- Eroare custom pentru cazul in care se cere predictie fara antrenare.
- Ajuta la mesaje mai clare decat o eroare generica.

Clasa `EmotionNaiveBayes`:

- Implementeaza clasificatorul.
- Parametru:
  - `alpha`: smoothing pentru probabilitati.

Campuri importante:

- `labels`: lista de emotii.
- `vocabulary`: setul de trasaturi invatate.
- `class_feature_counts`: cate aparitii are fiecare trasatura pentru fiecare clasa.
- `class_totals`: totalul ponderat de trasaturi pe clasa.
- `class_priors`: probabilitatile apriori ale claselor.
- `_fitted`: marcheaza daca modelul a fost antrenat.

Metoda `fit(examples)`:

- Input: lista sau iterator de `TrainingExample`.
- Ignora exemple cu label necunoscut.
- Extrage trasaturi prin `count_emotion_token_features`.
- Aplica greutatea exemplului.
- Actualizeaza frecventele pe clasa.
- Calculeaza priorurile cu smoothing.
- Marcheaza modelul ca antrenat.
- Returneaza `self`, ca sa permita chaining.

Metoda `predict_proba(text)`:

- Verifica daca modelul este antrenat.
- Extrage trasaturi din text.
- Pentru fiecare emotie calculeaza un scor logaritmic.
- Foloseste smoothing pentru trasaturi nevazute.
- Converteste scorurile logaritmice in probabilitati normalizate.

Metoda `predict(text)`:

- Apeleaza `predict_proba`.
- Alege emotia cu probabilitatea maxima.
- Returneaza dictionar compatibil cu restul pipeline-ului.

Functia `train_nb_from_lexicon(...)`:

- Incarca intrari din NRC.
- Filtreaza termenii nepotriviti.
- Transforma intrarile in `TrainingExample`.
- Antreneaza si returneaza un `EmotionNaiveBayes`.

Functia `evaluate_nb_from_lexicon(...)`:

- Imparte intrarile lexiconului in train/test.
- Antreneaza modelul pe train.
- Prezice pe test.
- Calculeaza accuracy, macro F1, metrici pe etichete si matrice de confuzie.
- Este folosita de comanda CLI `evaluate`.

Functia `count_emotion_token_features(text)`:

- Extrage feature-uri pentru NB.
- Pentru fiecare token adauga:
  - `word=<token>` cu greutate 2;
  - daca este hashtag, adauga si forma fara `#`;
  - n-grame de caractere de lungime 3, 4 si 5.

De ce foloseste n-grame de caractere:

- Ajuta la forme apropiate ale aceluiasi cuvant.
- Ajuta cand textul contine hashtaguri sau forme usor modificate.
- Reduce dependenta de potriviri exacte.

Functia `nrc_entry_to_training_example(entry)`:

- Converteste o intrare NRC intr-un exemplu de training.
- Inlocuieste `_` cu spatiu.
- Limiteaza scorul intre 0 si 3.
- Seteaza greutatea ca `1.0 + usable_score`.

Functia `looks_like_training_phrase(term)`:

- Elimina mention-uri, linkuri si termeni fara suficiente litere.
- Previne folosirea unor intrari zgomotoase din lexicon.

Functia `normalize_log_emotion_scores(log_scores)`:

- Aplica o forma stabila numeric de softmax.
- Scade scorul maxim inainte de exponentiere.
- Returneaza probabilitati care insumeaza 1.

Avantaje:

- Poate generaliza mai bine decat lexiconul pur.
- Nu are nevoie de dataset extern manual etichetat.
- Ramane usor de explicat in proiect.

Limitari:

- Trainingul este slab-supervizat, deoarece exemplele vin din termeni de lexicon, nu din propozitii reale.
- Poate invata biasurile lexiconului.

### `cod/src/emotion_analysis/pipeline.py` In Detaliu

Acest fisier ofera interfata principala pentru predictii.

Clasa `EmotionAnalyzer`:

- Este clasa pe care o folosesti cand vrei sa analizezi texte.
- Ascunde detaliile despre cum se incarca lexiconul si cum se antreneaza NB.

Constructorul:

- Parametri:
  - `lexicon_path`: cale custom catre lexicon.
  - `lexicon_max_entries`: limita pentru modelul lexical.
  - `nb_max_per_emotion`: limita pentru trainingul NB.
  - `hybrid_lexicon_weight`: cat conteaza lexiconul in metoda hybrid.
  - `lexicon_model`: model lexical injectat, util pentru teste.
  - `nb_model`: model NB injectat, util pentru teste.

Validare:

- `hybrid_lexicon_weight` trebuie sa fie intre 0 si 1.
- Daca este in afara intervalului, se ridica `ValueError`.

Metoda `analyze(text, method="hybrid")`:

- Accepta metodele:
  - `lexicon`;
  - `nb`;
  - `hybrid`.
- Pentru `lexicon`, apeleaza `self.lexicon_model.score(text)`.
- Pentru `nb`, apeleaza `self._nb_model().predict(text)`.
- Pentru `hybrid`, ruleaza ambele modele si combina scorurile.

Formula hybrid:

```text
score_final = hybrid_lexicon_weight * score_lexicon
            + (1 - hybrid_lexicon_weight) * score_nb
```

Output hybrid:

- `method`: `hybrid`.
- `text`: textul analizat.
- `tokens`: tokenii din analiza lexicala.
- `scores`: scorurile finale combinate.
- `dominant_emotion`: emotia cu scor maxim.
- `confidence`: scorul emotiei dominante.
- `coverage`: acoperirea lexiconului.
- `matches`: dovezile lexicale.
- `components`: scorurile separate ale modelelor.

Metoda `_nb_model()`:

- Creeaza modelul NB doar cand este necesar.
- Daca utilizatorul ruleaza doar metoda `lexicon`, NB nu este antrenat.
- Aceasta strategie economiseste timp la predictii simple.

De ce exista acest fisier:

- Fara `pipeline.py`, CLI-ul ar trebui sa stie prea multe despre fiecare model.
- Pipeline-ul pastreaza o interfata comuna pentru toate metodele.

### `cod/src/emotion_analysis/io.py` In Detaliu

Acest fisier pastreaza contractul fisierelor CSV.

Problema pe care o rezolva:

- Predictiile sunt dictionare interne complexe.
- CSV-ul are nevoie de coloane plate si stabile.
- Experimentele si CLI-ul trebuie sa scrie acelasi tip de output.

Constante:

- `ID_COLUMN = "ID"`: coloana principala de identificare.
- `SOURCE_ID_COLUMN = "source_id"`: id-ul original al randului.
- `PREDICTION_COLUMN = "prediction"`: eticheta prezisa.

Functia `read_text_rows(path, text_column="text")`:

- Deschide CSV-ul cu `utf-8-sig`, util pentru fisiere cu BOM.
- Foloseste `csv.DictReader`.
- Verifica existenta coloanei de text.
- Returneaza lista de dictionare.

Erori posibile:

- Daca fisierul nu are coloana `text`, ridica `ValueError`.

Functia `write_prediction_rows(path, rows)`:

- Creeaza folderul parinte daca nu exista.
- Scrie coloanele intr-o ordine fixa.
- Scrie scoruri pentru toate cele 8 emotii.
- Completeaza cu string gol campurile lipsa.

Functia `flatten_prediction(source_row, prediction)`:

- Ia randul original si predictia interna.
- Alege id-ul din `ID`, `id` sau `source_id`.
- Pune emotia dominanta si in `dominant_emotion`, si in `prediction`.
- Rotunjeste `confidence`, `coverage` si scorurile emotionale.
- Returneaza un dictionar gata de scris in CSV.

De ce exista `ID` si `source_id`:

- `ID` este util pentru compatibilitate cu formate de evaluare.
- `source_id` pastreaza legatura cu randul original.

### `cod/src/emotion_analysis/metrics.py` In Detaliu

Acest fisier calculeaza metricile pentru evaluare.

Functia `classification_metrics(gold_labels, predicted_labels, labels=EMOTIONS)`:

- Input:
  - lista de etichete reale;
  - lista de etichete prezise;
  - lista de etichete permise.
- Verifica daca listele au aceeasi lungime.
- Construieste matricea de confuzie.
- Calculeaza:
  - `accuracy`;
  - `macro_precision`;
  - `macro_recall`;
  - `macro_f1`;
  - metrici per emotie;
  - totalul exemplelor.

Formula accuracy:

```text
accuracy = predictii_corecte / numar_total_exemple
```

Formula precision pentru o emotie:

```text
precision = TP / (TP + FP)
```

Formula recall pentru o emotie:

```text
recall = TP / (TP + FN)
```

Formula F1:

```text
F1 = 2 * precision * recall / (precision + recall)
```

De ce macro F1:

- Datasetul poate avea mai multe clase.
- Macro F1 trateaza fiecare emotie egal.
- Este mai informativ decat accuracy cand unele emotii sunt mai greu de prezis.

Functia `confusion_matrix(...)`:

- Creeaza dictionar de forma:

```python
{
    "joy": {"joy": 10, "sadness": 2, ...},
    "anger": {"anger": 8, "fear": 1, ...},
}
```

- Ignora etichetele care nu sunt in lista permisa.

Functia `label_distribution(labels)`:

- Numara cate aparitii are fiecare emotie.
- Este folosita pentru distributii gold si predicted.

### `cod/src/emotion_analysis/visualization.py` In Detaliu

Acest fisier genereaza grafice fara dependinte externe.

De ce SVG:

- Este text simplu, deci poate fi generat cu Python standard library.
- Poate fi deschis in browser.
- Poate fi inclus in raport sau prezentare.
- Nu necesita `matplotlib`.

Constanta `COLORS`:

- Asociaza fiecare emotie cu o culoare.
- Pastreaza aceeasi culoare in toate graficele.

Functia `write_distribution_svg(path, distribution, title=...)`:

- Creeaza folderul de output daca nu exista.
- Seteaza dimensiunea graficului.
- Calculeaza latimea barelor in functie de valoarea maxima.
- Scrie manual elemente SVG:
  - fundal;
  - titlu;
  - etichete;
  - bare gri de fundal;
  - bare colorate;
  - valori numerice.

Functia `escape_xml(value)`:

- Inlocuieste caractere speciale:
  - `&`
  - `<`
  - `>`
  - `"`
- Previne stricarea fisierului SVG daca titlul contine caractere speciale.

### `cod/src/emotion_analysis/experiments.py` In Detaliu

Acest fisier este motorul evaluarii finale.

Functia `run_experiment_suite(...)`:

- Este functia centrala pentru experiment.
- Citeste datasetul etichetat.
- Ruleaza una sau mai multe metode.
- Scrie toate fisierele de rezultat.

Parametri principali:

- `input_path`: calea catre datasetul de evaluare.
- `output_dir`: folderul unde se salveaza artefactele.
- `text_column`: coloana cu text.
- `label_column`: coloana cu eticheta reala.
- `domain_column`: coloana cu domeniul textului.
- `methods`: metodele rulate, implicit `lexicon`, `nb`, `hybrid`.
- `lexicon_path`: cale custom catre lexicon.
- `hybrid_lexicon_weight`: greutatea lexicala pentru metoda hybrid.
- `analyzer`: permite injectarea unui `EmotionAnalyzer`, util in teste.

Pasi interni:

1. Citeste randurile din CSV cu `read_text_rows`.
2. Verifica etichetele cu `check_labels`.
3. Verifica metodele cu `check_methods`.
4. Creeaza folderul de output.
5. Creeaza sau primeste un `EmotionAnalyzer`.
6. Extrage lista de etichete reale.
7. Scrie distributia gold in CSV si SVG.
8. Pentru fiecare metoda:
   - ruleaza predictia pe fiecare rand;
   - transforma predictia in rand CSV;
   - calculeaza metricile;
   - calculeaza distributia predictiilor;
   - calculeaza metrici pe domenii;
   - scrie predictii, confuzie, distributii si grafice.
9. Scrie comparatia intre metode.
10. Scrie `metrics.json`.
11. Returneaza sumarul experimentului.

Functia `check_labels(rows, label_column)`:

- Verifica daca datasetul nu este gol.
- Strange labelurile invalide.
- Ridica `ValueError` daca exista emotii in afara listei `EMOTIONS`.

Functia `check_methods(methods)`:

- Verifica daca metodele cerute sunt in `DEFAULT_METHODS`.
- Previne rularea accidentala cu nume gresite.

Functia `semeval_row_id(row)`:

- Alege un ID din `ID`, `id` sau `source_id`.
- Ajuta la compatibilitatea cu formate de evaluare diferite.

Functia `scores_by_domain(rows, preds, label_column, domain_column)`:

- Grupeaza etichetele reale si predictiile dupa domeniu.
- Calculeaza metrici separate pentru fiecare domeniu.
- Returneaza dictionar cu rezultate pentru `social`, `news`, `blog` sau alte domenii existente.

Functia `write_preds_csv(path, rows)`:

- Scrie fisierul `predictions_<method>.csv`.
- Pastreaza coloane de baza:
  - `ID`;
  - `source_id`;
  - `domain`;
  - `label`;
  - `text`;
  - `method`;
  - `dominant_emotion`;
  - `prediction`;
  - `confidence`;
  - `coverage`.
- Adauga toate coloanele `score_<emotion>`.
- Adauga extra columns daca apar in randuri.

Functia `write_compare_csv(path, rows)`:

- Scrie `method_comparison.csv`.
- Este folosita pentru compararea finala intre metode.

Functia `write_domain_csv(path, summary)`:

- Scrie `domain_metrics.csv`.
- Parcurge rezultatele fiecarei metode si fiecare domeniu.

Functia `write_conf_csv(path, confusion)`:

- Scrie matricea de confuzie.
- Prima coloana este `gold\predicted`.
- Urmatoarele coloane sunt emotiile in ordinea din `EMOTIONS`.

Functia `write_dist_csv(path, distribution)`:

- Scrie doua coloane:
  - `emotion`;
  - `count`.

De ce acest fisier este important:

- Leaga toate componentele intr-un experiment reproductibil.
- Produce fisierele pe care le folosesti in raport si prezentare.
- Este dovada principala ca implementarea nu face doar predictii izolate, ci si evaluare.

### `cod/src/emotion_analysis/cli.py` In Detaliu

Acest fisier transforma proiectul intr-o aplicatie de terminal.

Functia `build_parser()`:

- Creeaza parserul principal `argparse`.
- Adauga argumentul global `--lexicon`.
- Defineste subcomenzile:
  - `predict`;
  - `predict-file`;
  - `evaluate`;
  - `run-experiments`.

Comanda `predict`:

- Input:
  - `--text`;
  - `--method`;
  - `--hybrid-weight`;
  - `--top`;
  - `--json`.
- Output:
  - afisare text in terminal sau JSON.
- Utilizare:

```powershell
python emotion_cli.py predict --text "I am very happy" --method hybrid
```

Comanda `predict-file`:

- Input:
  - `--input`;
  - `--output`;
  - `--text-column`;
  - `--method`;
  - `--hybrid-weight`.
- Output:
  - CSV cu predictii.
- Utilizare:

```powershell
python emotion_cli.py predict-file --input data/sample_texts.csv --output outputs/predictions.csv --method hybrid
```

Comanda `evaluate`:

- Evalueaza modelul NB pe un split din lexicon.
- Nu foloseste `final_eval_texts.csv`.
- Este utila pentru verificarea modelului invatat din lexicon.

Comanda `run-experiments`:

- Ruleaza evaluarea completa pe datasetul etichetat.
- Genereaza toate fisierele din `outputs/final_experiment/`.
- Este comanda principala pentru proiectul final.

Functia `main(argv=None)`:

- Parseaza argumentele.
- Decide ce comanda se ruleaza.
- Creeaza `EmotionAnalyzer` cand este nevoie.
- Returneaza cod de iesire.

Functia `print_prediction(result, top=3)`:

- Afiseaza:
  - metoda;
  - emotia dominanta;
  - confidence;
  - coverage;
  - top scoruri;
  - dovezi lexicale, daca exista.

Functia `print_evaluation(metrics)`:

- Afiseaza rezultatele evaluarii NB.
- Include metrici per emotie.

Functia `print_experiment_summary(summary, output_dir)`:

- Afiseaza sumarul experimentului final.
- Include pentru fiecare metoda:
  - accuracy;
  - macro precision;
  - macro recall;
  - macro F1;
  - total.

Functia `top_scores(scores, limit)`:

- Sorteaza emotiile dupa scor.
- Returneaza primele `limit` emotii.

De ce CLI-ul este important:

- Profesorul poate rula proiectul fara sa scrie cod Python.
- Comenzile sunt reproductibile.
- Output-urile sunt generate la fel de fiecare data.

### `cod/tests/test_core.py` In Detaliu

Acest fisier testeaza componentele centrale ale proiectului.

Clasa `EmotionAnalysisTests`:

- Extinde `unittest.TestCase`.
- Contine teste unitare si un test mic de integrare.

Testul `test_lexicon_scores_known_words`:

- Creeaza un lexicon artificial mic.
- Verifica daca `happy` bate `furious` cand textul este `I am very happy, not furious.`
- Testeaza:
  - modelul lexical;
  - intensificatorul `very`;
  - negatia `not`;
  - alegerea emotiei dominante.

Testul `test_nb_learns_simple_examples`:

- Antreneaza NB pe trei exemple simple:
  - joy;
  - anger;
  - fear.
- Verifica daca textul `angry and furious` este clasificat ca `anger`.
- Testeaza ca trainingul si predictia NB functioneaza.

Testul `test_pipeline_hybrid_with_injected_nb`:

- Creeaza un model lexical artificial.
- Creeaza un model NB mic.
- Injecteaza ambele in `EmotionAnalyzer`.
- Verifica metoda `hybrid`.
- Testul evita dependenta de lexiconul real, deci ruleaza rapid.

Testul `test_metrics_macro_f1`:

- Creeaza liste mici de etichete reale si prezise.
- Verifica accuracy.
- Verifica o celula din matricea de confuzie.

Testul `test_invalid_hybrid_weight_is_rejected`:

- Incearca sa creeze `EmotionAnalyzer(hybrid_lexicon_weight=1.5)`.
- Verifica daca se ridica `ValueError`.
- Protejeaza validarea parametrilor.

Testul `test_experiment_suite_writes_outputs`:

- Creeaza temporar un dataset CSV.
- Ruleaza `run_experiment_suite` doar cu metoda `hybrid`.
- Verifica daca accuracy este 1.0 pe exemplul controlat.
- Verifica daca se scriu:
  - `metrics.json`;
  - `predicted_distribution_hybrid.svg`.

De ce testele sunt importante:

- Confirma ca modelele de baza functioneaza.
- Confirma ca pipeline-ul poate fi folosit fara lexicon real prin dependency injection.
- Confirma ca experimentul produce fisiere.
- Ofera siguranta cand se modifica datasetul sau codul.

## Folderul `cod/tests/`

Folderul cu teste automate.

### `cod/tests/test_core.py`

Teste de regresie pentru componentele principale.

Teste incluse:

- verifica daca modelul lexical recunoaste cuvinte emotionale cunoscute;
- verifica daca Naive Bayes invata exemple simple;
- verifica metoda hybrid cu modele injectate;
- verifica metricile si matricea de confuzie;
- verifica respingerea unei greutati hybrid invalide;
- verifica faptul ca experimentul scrie fisiere de output.

Rol:

- Confirma ca partea principala a proiectului functioneaza dupa modificari.
- Protejeaza impotriva stricarii pipeline-ului.

## Folderul `linkuri_extrase/`

Folderul `linkuri_extrase/` contine resurse colectate din pagina proiectului si din linkurile asociate. Aceste fisiere sunt folosite ca material de documentare si ca sursa pentru lexiconul NRC.

### Fisiere principale din `linkuri_extrase/`

#### `linkuri_extrase/README.md`

Document local despre procesul de extragere a linkurilor si resurselor.

#### `linkuri_extrase/pagina_originala.html`

Copie a paginii originale din care au fost extrase linkurile.

#### `linkuri_extrase/manifest_links.csv`

Lista principala cu linkuri identificate.

Rol:

- Pastreaza inventarul linkurilor gasite in pagina.
- Ajuta la auditarea surselor.

#### `linkuri_extrase/internal_links.csv`

Lista cu linkuri interne.

Rol:

- Diferentiaza linkurile interne de cele externe.

#### `linkuri_extrase/secondary_links.csv`

Lista mare cu linkuri secundare extrase din pagini/resurse.

Rol:

- Pastreaza surse suplimentare gasite prin explorarea linkurilor initiale.

#### `linkuri_extrase/secondary_resource_links_not_downloaded.csv`

Lista cu resurse secundare care nu au fost descarcate.

Rol:

- Documenteaza ce surse au fost identificate, dar nu au ajuns local.

#### `linkuri_extrase/download_results.csv`

Rezultatele procesului de descarcare.

Rol:

- Arata ce fisiere au fost descarcate cu succes si ce descarcari au esuat.

#### `linkuri_extrase/text_extraction_results.csv`

Rezultatele extragerii de text din fisiere HTML/PDF/arhive.

Rol:

- Arata pentru ce resurse a fost extras text.

#### `linkuri_extrase/archive_inventory.csv`

Inventarul fisierelor gasite in arhive.

Rol:

- Documenteaza continutul arhivelor `.zip` descarcate.

#### `linkuri_extrase/github_repo_inventory.csv`

Inventarul fisierelor din repository-urile GitHub descarcate ca resurse.

Rol:

- Ajuta la urmarirea continutului clonat in `github_repos/`.

#### `linkuri_extrase/acl_fallback_downloads.csv`

Lista descarcarilor fallback pentru resurse ACL Anthology.

Rol:

- Pastreaza evidenta surselor descarcate prin metode alternative.

#### `linkuri_extrase/manual_review.md`

Note pentru verificare manuala.

Rol:

- Marcheaza resurse sau situatii care necesita inspectie manuala.

#### `linkuri_extrase/audit_final.md`

Rezumatul final al auditului resurselor.

Rol:

- Sintetizeaza starea colectarii si extragerii resurselor.

### `linkuri_extrase/raw/`

Contine fisierele descarcate in forma bruta.

Tipuri de fisiere:

- `.html` / `.htm`: pagini web descarcate.
- `.pdf`: articole, postere sau slide-uri.
- `.zip`: arhive cu lexiconuri sau dataseturi.
- `.bib` / `.txt`: citari BibTeX sau fisiere text.

Rol:

- Pastreaza sursele originale.
- Permite verificarea ulterioara a materialelor.
- Nu este cod executabil.

Exemple importante:

- `013_saifmohammad.com_NRC-Emotion-Lexicon.htm`: pagina despre NRC Emotion Lexicon.
- `061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2.zip`: arhiva din care provine lexiconul folosit de cod.
- `016_saifmohammad.com_Mohammad-Turney-NAACL10-EmotionWorkshop.pdf`: articol/resursa despre emotii si lexiconuri.

### `linkuri_extrase/text/`

Contine text extras din resursele brute.

Subfoldere si fisiere:

- `text/html/`: text extras din pagini HTML.
- `text/pdf/`: text extras din fisiere PDF.
- fisiere `.txt`, `.bib`: variante text ale resurselor descarcate.

Rol:

- Face continutul resurselor mai usor de cautat si citit.
- Ajuta la documentarea proiectului si la intelegerea surselor NRC.

### `linkuri_extrase/archives/`

Contine arhive dezarhivate.

Rol:

- Pastreaza continutul lexiconurilor si dataseturilor descarcate.
- Include fisierul folosit efectiv de proiect:

```text
linkuri_extrase/archives/061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2/
`-- NRC-Hashtag-Emotion-Lexicon-v0.2/
    `-- NRC-Hashtag-Emotion-Lexicon-v0.2.txt
```

Fisierul `NRC-Hashtag-Emotion-Lexicon-v0.2.txt` este resursa citita de `resources.py`.

### `linkuri_extrase/github_repos/`

Contine repository-uri GitHub descarcate ca resurse.

Rol:

- Pastreaza cod si date auxiliare din proiecte relevante pentru analiza emotiilor.
- Nu este parte directa din pipeline-ul `cod/`.
- Este folosit ca material de documentare si comparatie.

## Folderul `semeval-code-quality/`

Acest folder contine un skill si utilitare locale inspirate de repository-ul SemEval-2026 Task 13. El nu este necesar pentru predictia emotiilor, dar a fost adaugat ca instrument auxiliar de verificare si analiza a codului.

### `semeval-code-quality/SKILL.md`

Fisier de instructiuni pentru skill.

Rol:

- Defineste reguli pentru review si refactorizare de cod.
- Foloseste idei din SemEval-2026 Task 13 despre detectarea codului generat.
- Pastreaza limite clare: nu promite ocolirea detectorilor si nu recomanda stricarea stilului de cod.

### `semeval-code-quality/agents/openai.yaml`

Configuratie pentru agent/skill.

Rol:

- Pastreaza configuratia asociata skillului.
- Nu este folosit de pipeline-ul de emotion analysis.

### `semeval-code-quality/references/semeval_task13.md`

Rezumat local al repository-ului SemEval-2026 Task 13.

Rol:

- Noteaza taskurile A/B/C.
- Noteaza formatele de label.
- Noteaza diferentele dintre README, `format_checker.py` si `scorer.py`.
- Serveste ca referinta rapida fara a reciti tot repository-ul extern.

### `semeval-code-quality/scripts/semeval_check.py`

Script pentru validarea si evaluarea fisierelor de predictii.

Rol:

- Verifica daca un CSV de predictii are coloane de ID si predictie.
- Suporta variante precum `ID`/`id` si `prediction`/`label`.
- Poate calcula accuracy, macro precision, macro recall si macro F1 daca primeste si un fisier gold.

Utilizare tipica:

```powershell
python semeval-code-quality/scripts/semeval_check.py --predictions path/to/predictions.csv
```

### `semeval-code-quality/scripts/detect_code_file.py`

Script local care antreneaza un detector simplu pe Task A din SemEval si clasifica fisiere de cod.

Rol:

- Citeste `tools/SemEval-2026-Task13/task_A/task_a_trial.parquet`.
- Antreneaza un model `TfidfVectorizer + LogisticRegression`.
- Clasifica fisiere `.py` ca `human` sau `machine` conform modelului local.

Important:

- Nu este detectorul oficial SemEval.
- Nu garanteaza clasificarea de catre alte site-uri sau alte modele.
- Este un instrument local de analiza, separat de proiectul de emotion analysis.

## Folderul `tools/SemEval-2026-Task13/`

Acesta este repository-ul extern SemEval-2026 Task 13 clonat local pentru referinta.

### `tools/SemEval-2026-Task13/README.md`

Documentatia originala a taskului SemEval.

Rol:

- Explica taskurile.
- Explica formatul dataseturilor.
- Explica formatul de submission.
- Ofera context pentru detectarea codului generat.

### `tools/SemEval-2026-Task13/LICENSE`

Licenta repository-ului extern.

Rol:

- Specifica drepturile si conditiile de utilizare ale codului SemEval.

### `tools/SemEval-2026-Task13/format_checker.py`

Script oficial/local pentru verificarea formatului de submission.

Rol:

- Verifica extensia CSV.
- Verifica existenta coloanelor asteptate.
- Verifica labelurile valide pentru task.

### `tools/SemEval-2026-Task13/scorer.py`

Script de scoring.

Rol:

- Compara predictiile cu etichetele reale.
- Calculeaza metrici precum Macro-F1, accuracy, macro precision si macro recall.

### `tools/SemEval-2026-Task13/baselines/train.py`

Script baseline pentru antrenarea unui model.

Rol:

- Foloseste CodeBERT/HuggingFace.
- Incarca date de training.
- Antreneaza un classifier pentru taskurile SemEval.

### `tools/SemEval-2026-Task13/baselines/predict.py`

Script baseline pentru predictii.

Rol:

- Incarca un model antrenat.
- Ruleaza inferenta pe date de intrare.
- Scrie predictii in format CSV.

### `tools/SemEval-2026-Task13/baselines/Kaggle_starters/`

Notebook-uri starter pentru Kaggle.

Fisiere:

- `Task-A-Starter.ipynb`
- `Task-B-Starter.ipynb`
- `Task-C-Starter.ipynb`

Rol:

- Exemple de pornire pentru fiecare task SemEval.
- Nu sunt folosite de pipeline-ul de emotion analysis.

### `tools/SemEval-2026-Task13/task_A/`

Date si mapping pentru Task A.

Fisiere:

- `task_a_trial.parquet`: date trial pentru clasificare binara.
- `id_to_label.json`: mapping id -> label.
- `label_to_id.json`: mapping label -> id.

Rol:

- Task A distinge intre cod uman si cod generat.

### `tools/SemEval-2026-Task13/task_B/`

Date si mapping pentru Task B.

Fisiere:

- `task_b_trial.parquet`
- `id_to_label.json`
- `label_to_id.json`

Rol:

- Task B distinge intre mai multe familii de generatori.

### `tools/SemEval-2026-Task13/task_C/`

Date si mapping pentru Task C.

Fisiere:

- `task_c_trial.parquet`
- `id_to_label.json`
- `label_to_id.json`

Rol:

- Task C distinge intre cod uman, machine, hybrid si adversarial.

## Fisiere Din Radacina Proiectului

### `README.md`

Acest document.

Rol:

- Explica structura proiectului.
- Explica fiecare componenta importanta.
- Ofera comenzi de rulare si verificare.

### `cerinte.md`

Fisier cu cerintele generale ale proiectului.

Rol:

- Stabileste asteptari despre structura, cod, raport si rezultate.
- A fost folosit ca ghid pentru implementare.

### `cerinte_proiect.md`

Fisier cu tema aleasa.

Rol:

- Descrie proiectul concret: emotion analysis.
- Mentioneaza resursele si articolul/pagina de referinta.

### `pagina.html`

Pagina HTML atasata initial.

Rol:

- Contine articolul si resursele mentionate in cerinta proiectului.
- A fost folosita pentru extragerea linkurilor si resurselor.

## Ce Fisiere Se Modifica In Mod Normal

Pentru lucrul obisnuit la proiect, cele mai importante fisiere sunt:

- `cod/data/final_eval_texts.csv`: daca se adauga sau se modifica exemple etichetate.
- `cod/data/sample_texts.csv`: daca se adauga exemple rapide pentru predictie.
- `cod/src/emotion_analysis/*.py`: daca se modifica implementarea.
- `cod/tests/test_core.py`: daca se adauga teste.
- `cod/outputs/final_experiment/*`: se regenereaza automat prin `run-experiments`.
- `cod/outputs/predictions.csv`: se regenereaza automat prin `predict-file`.

## Ce Fisiere Nu Trebuie Editate Manual In Mod Normal

- `cod/outputs/*.csv`, `cod/outputs/*.json`, `cod/outputs/*.svg`: sunt rezultate generate.
- `linkuri_extrase/raw/*`: sunt surse brute descarcate.
- `linkuri_extrase/text/*`: sunt texte extrase automat.
- `linkuri_extrase/archives/*`: sunt arhive dezarhivate.
- `tools/SemEval-2026-Task13/*`: este repository extern de referinta.

## Rezultatul Final Al Partii De Cod

Partea de cod este formata din:

- sistem CLI complet;
- model bazat pe lexicon;
- model Naive Bayes;
- model hybrid;
- dataset final cu peste 500 de exemple;
- evaluare automata pe 8 emotii;
- metrici globale si pe domenii;
- matrice de confuzie;
- distributii CSV si SVG;
- teste automate.

Aceasta structura este suficienta pentru a demonstra implementarea proiectului de emotion analysis fara a depinde de GPU, RunPod sau Kaggle.
