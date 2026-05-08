# Simulare prezentare proiect - Emotion Analysis

Acest document este scriptul complet pentru prezentarea proiectului. Echipa are 3 membri, iar prezentarea este impartita astfel:

- **Student 1**: introducere, obiectiv, resurse, structura generala.
- **Student 2**: implementarea modelelor, preprocesare, lexicon, Naive Bayes, hybrid.
- **Student 3**: date, experimente, rezultate, teste, concluzii si demo.

Textul care trebuie spus profesorului este marcat cu verde.

Indicatiile de tip **Aratam in cod:** nu se citesc neaparat cu voce tare; sunt pentru momentul in care prezentam ecranul si aratam fisierul/functia relevanta.

---

## 1. Deschiderea prezentarii

**Vorbeste: Student 1**

<span style="color: green;">
Buna ziua! Proiectul nostru se numeste Emotion Analysis si are ca obiectiv detectarea emotiei dominante dintr-un text. Am construit o aplicatie Python care poate primi un text simplu sau un fisier CSV cu mai multe texte si returneaza emotia prezisa, impreuna cu scoruri pentru fiecare dintre cele 8 emotii folosite in proiect.
</span>

**Aratam in cod:**

- `cod/emotion_cli.py`
- `cod/src/emotion_analysis/cli.py`
- `cod/src/emotion_analysis/constants.py`

**Ce aratam concret:**

- In `constants.py`, aratam lista `EMOTIONS`.
- In `emotion_cli.py`, aratam ca proiectul poate fi pornit din terminal.
- In `cli.py`, aratam comenzile disponibile.

---

## 2. Tema proiectului

**Vorbeste: Student 1**

<span style="color: green;">
Tema aleasa de noi este detectarea emotiilor in text. Nu ne-am limitat la sentiment pozitiv sau negativ, ci am folosit 8 emotii: anger, anticipation, disgust, fear, joy, sadness, surprise si trust. Aceste emotii sunt folosite in mai multe resurse de NLP pentru analiza afectiva si sunt potrivite pentru o clasificare mai detaliata decat sentiment analysis clasic.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/constants.py`

**Ce aratam concret:**

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

---

## 3. Ce face aplicatia finala

**Vorbeste: Student 1**

<span style="color: green;">
Aplicatia finala poate fi folosita in trei moduri principale. In primul rand, putem analiza un singur text din linia de comanda. In al doilea rand, putem analiza un fisier CSV cu mai multe texte. In al treilea rand, putem rula un experiment complet pe un dataset etichetat, unde comparam metodele implementate si generam automat fisiere cu metrici, predictii, matrici de confuzie si grafice.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/cli.py`
- `cod/src/emotion_analysis/experiments.py`
- `cod/outputs/final_experiment/`

**Ce aratam concret:**

- In `cli.py`, aratam subcomenzile `predict`, `predict-file`, `evaluate`, `run-experiments`.
- In `experiments.py`, aratam functia `run_experiment_suite`.
- In `outputs/final_experiment/`, aratam fisierele generate.

---

## 4. Structura proiectului

**Vorbeste: Student 1**

<span style="color: green;">
Structura proiectului este impartita clar. Folderul cod contine implementarea, datele, output-urile si testele. Folderul linkuri_extrase contine resursele descarcate si extrase din pagina proiectului, inclusiv lexiconul NRC folosit de model. Folderul semeval-code-quality si folderul tools contin utilitare auxiliare pentru verificari de cod, dar nu sunt necesare pentru predictia emotiilor.
</span>

**Aratam in proiect:**

- `cod/`
- `cod/src/emotion_analysis/`
- `cod/data/`
- `cod/outputs/`
- `linkuri_extrase/`
- `semeval-code-quality/`
- `tools/SemEval-2026-Task13/`

**Ce aratam concret:**

- `cod/src/emotion_analysis/` ca pachetul principal.
- `cod/data/final_eval_texts.csv` ca dataset final.
- `cod/outputs/final_experiment/` ca rezultate generate.

---

## 5. Resursa principala: NRC Hashtag Emotion Lexicon

**Vorbeste: Student 1**

<span style="color: green;">
Pentru componenta bazata pe reguli am folosit NRC Hashtag Emotion Lexicon. Acest lexicon contine asocieri intre termeni si emotii, fiecare asociere avand un scor. Codul nostru incarca acest fisier local din resursele extrase si il transforma intr-o structura eficienta pentru cautare.
</span>

**Aratam in cod/resurse:**

- `linkuri_extrase/archives/061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2/NRC-Hashtag-Emotion-Lexicon-v0.2.txt`
- `cod/src/emotion_analysis/resources.py`

**Ce aratam concret:**

- In `resources.py`, aratam `DEFAULT_LEXICON_RELATIVE`.
- Aratam clasa `LexiconEntry`.
- Aratam functiile `load_hashtag_entries` si `load_hashtag_lexicon`.

---

## 6. Incarcarea lexiconului

**Vorbeste: Student 1**

<span style="color: green;">
Am facut incarcarea lexiconului intr-un modul separat, pentru ca modelele sa nu depinda direct de calea fisierului. Functia poate folosi fie calea implicita, fie o cale data de utilizator prin argumentul --lexicon sau prin variabila de mediu EMOTION_LEXICON_PATH.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/resources.py`

**Ce aratam concret:**

- `default_lexicon_path()`
- `resolve_lexicon_path(path)`
- `load_hashtag_lexicon(...)`
- `load_hashtag_entries(...)`

---

## 7. Preprocesarea textului

**Vorbeste: Student 2**

<span style="color: green;">
Inainte de predictie, textul este preprocesat. Am implementat normalizare, tokenizare, eliminarea URL-urilor, reducerea repetitiilor exagerate de caractere si tratarea unor cazuri precum hashtaguri, negatii si intensificatori. Acest pas este important pentru ca modelele sa primeasca texte intr-o forma consecventa.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/text.py`

**Ce aratam concret:**

- `URL_PATTERN`
- `TOKEN_PATTERN`
- `LONG_CHAR_RUN`
- `NEGATIONS`
- `INTENSIFIERS`
- `normalize_text(text)`
- `normalize_token(token)`
- `tokenize(text)`
- `token_variants(token)`

---

## 8. De ce avem negatii si intensificatori

**Vorbeste: Student 2**

<span style="color: green;">
Am adaugat si o logica simpla pentru context. De exemplu, expresia very happy ar trebui sa creasca scorul pentru joy, in timp ce not happy nu ar trebui tratata la fel ca happy. Pentru asta cautam negatii si intensificatori in apropierea tokenului analizat.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/text.py`
- `cod/src/emotion_analysis/lexicon_model.py`

**Ce aratam concret:**

- In `text.py`, aratam:
  - `has_recent_negation(tokens, index)`
  - `has_recent_intensifier(tokens, index)`
- In `lexicon_model.py`, aratam:
  - `recent_context_multiplier(tokens, token_index)`

---

## 9. Prima metoda: modelul lexical

**Vorbeste: Student 2**

<span style="color: green;">
Prima metoda implementata este metoda lexicala. Aceasta cauta fiecare token din text in lexiconul NRC. Daca un token este asociat cu o emotie, atunci emotia respectiva primeste un scor. La final, scorurile sunt normalizate, iar emotia cu scorul cel mai mare devine emotia dominanta.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/lexicon_model.py`

**Ce aratam concret:**

- Clasa `WeightedEmotionLexicon`
- Metoda `score(text)`
- Functia `normalize_emotion_totals(emotion_totals)`
- Functia `summarize_lexicon_hits(hits)`

---

## 10. Ce returneaza modelul lexical

**Vorbeste: Student 2**

<span style="color: green;">
Modelul lexical nu returneaza doar o eticheta. El returneaza textul, tokenii, scorurile brute, scorurile normalizate, emotia dominanta, increderea, acoperirea lexiconului si dovezile lexicale gasite. Acest lucru face metoda usor de explicat, pentru ca putem vedea ce cuvinte au contribuit la predictie.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/lexicon_model.py`

**Ce aratam concret in output-ul metodei `score`:**

- `"method"`
- `"tokens"`
- `"raw_scores"`
- `"scores"`
- `"dominant_emotion"`
- `"confidence"`
- `"coverage"`
- `"matches"`

---

## 11. A doua metoda: Naive Bayes

**Vorbeste: Student 2**

<span style="color: green;">
A doua metoda este un model Naive Bayes. In loc sa folosim doar potriviri exacte in lexicon, transformam intrarile din lexicon in exemple de antrenare. Fiecare termen devine un exemplu cu o eticheta emotionala si o greutate. Modelul invata apoi trasaturi de cuvinte si n-grame de caractere.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/nb_model.py`

**Ce aratam concret:**

- `TrainingExample`
- `EmotionNaiveBayes`
- `train_nb_from_lexicon(...)`
- `nrc_entry_to_training_example(entry)`
- `count_emotion_token_features(text)`

---

## 12. De ce folosim trasaturi de cuvant si caractere

**Vorbeste: Student 2**

<span style="color: green;">
Pentru Naive Bayes am folosit atat trasaturi de cuvant, cat si n-grame de caractere. Trasaturile de cuvant ajuta la identificarea termenilor cunoscuti, iar n-gramele de caractere ajuta modelul sa generalizeze la forme apropiate, hashtaguri sau mici variatii de scriere.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/nb_model.py`

**Ce aratam concret:**

- Functia `count_emotion_token_features(text)`
- Liniile unde se adauga:
  - `word=<token>`
  - forma fara `#`
  - `char3=...`
  - `char4=...`
  - `char5=...`

---

## 13. Antrenarea modelului Naive Bayes

**Vorbeste: Student 2**

<span style="color: green;">
Antrenarea se face automat din lexicon. Pentru fiecare intrare valida din NRC, construim un TrainingExample. Scorul din lexicon devine parte din greutatea exemplului, astfel incat termenii mai puternic asociati cu o emotie conteaza mai mult la antrenare.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/nb_model.py`

**Ce aratam concret:**

- `train_nb_from_lexicon(...)`
- `load_hashtag_entries(...)`
- `looks_like_training_phrase(term)`
- `nrc_entry_to_training_example(entry)`
- metoda `fit(...)` din `EmotionNaiveBayes`

---

## 14. Predictia cu Naive Bayes

**Vorbeste: Student 2**

<span style="color: green;">
La predictie, modelul calculeaza probabilitati pentru fiecare dintre cele 8 emotii. Pentru stabilitate numerica, scorurile sunt calculate in logaritmi, apoi sunt transformate in probabilitati normalizate. Emotia cu probabilitatea cea mai mare este aleasa ca rezultat.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/nb_model.py`

**Ce aratam concret:**

- `predict_proba(text)`
- `predict(text)`
- `normalize_log_emotion_scores(log_scores)`
- `NaiveBayesNotFittedError`

---

## 15. A treia metoda: hybrid

**Vorbeste: Student 2**

<span style="color: green;">
A treia metoda este metoda hybrid. Ea combina scorurile modelului lexical cu scorurile modelului Naive Bayes. Am facut aceasta combinatie pentru a pastra interpretabilitatea lexiconului, dar si pentru a beneficia de generalizarea modelului invatat.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/pipeline.py`

**Ce aratam concret:**

- Clasa `EmotionAnalyzer`
- Metoda `analyze(text, method="hybrid")`
- Parametrul `hybrid_lexicon_weight`
- Combinarea scorurilor:

```python
scores = {
    emotion: lexicon_share * lexicon_result["scores"][emotion]
    + nb_share * nb_result["scores"][emotion]
    for emotion in EMOTIONS
}
```

---

## 16. Rolul clasei EmotionAnalyzer

**Vorbeste: Student 2**

<span style="color: green;">
Clasa EmotionAnalyzer este interfata principala a proiectului. Ea ascunde detaliile modelelor si permite apelarea aceleiasi metode analyze indiferent daca vrem lexicon, Naive Bayes sau hybrid. De asemenea, modelul Naive Bayes este creat doar cand este nevoie, deci daca rulam doar metoda lexicala nu pierdem timp cu antrenarea NB.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/pipeline.py`

**Ce aratam concret:**

- `__init__(...)`
- `analyze(...)`
- `_nb_model(...)`

---

## 17. Datele de intrare

**Vorbeste: Student 3**

<span style="color: green;">
Pentru evaluarea finala am creat un dataset etichetat in fisierul final_eval_texts.csv. Acesta contine peste 500 de exemple, fiecare exemplu avand un id, un domeniu, o eticheta corecta si textul propriu-zis. Domeniile sunt social, news si blog, pentru a testa modelul pe stiluri diferite de text.
</span>

**Aratam in fisiere:**

- `cod/data/final_eval_texts.csv`
- `cod/data/sample_texts.csv`

**Ce aratam concret:**

- In `final_eval_texts.csv`, aratam coloanele:
  - `id`
  - `domain`
  - `label`
  - `text`
- In `sample_texts.csv`, aratam texte fara label pentru demo.

---

## 18. Citirea si scrierea fisierelor CSV

**Vorbeste: Student 3**

<span style="color: green;">
Pentru fisierele CSV am separat logica intr-un modul dedicat. Citirea verifica daca exista coloana de text, iar scrierea pastreaza un format stabil pentru predictii. In output avem id-ul, textul, metoda folosita, emotia dominanta, confidence, coverage si scoruri pentru fiecare emotie.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/io.py`

**Ce aratam concret:**

- `read_text_rows(path, text_column="text")`
- `write_prediction_rows(path, rows)`
- `flatten_prediction(source_row, prediction)`
- constantele:
  - `ID_COLUMN`
  - `SOURCE_ID_COLUMN`
  - `PREDICTION_COLUMN`

---

## 19. Comanda predict-file

**Vorbeste: Student 3**

<span style="color: green;">
Pentru predictii pe mai multe texte, folosim comanda predict-file. Aceasta citeste randurile dintr-un CSV, ruleaza modelul pentru fiecare text si scrie rezultatele intr-un fisier de output. Fisierul generat este predictions.csv.
</span>

**Aratam in cod si output:**

- `cod/src/emotion_analysis/cli.py`
- `cod/src/emotion_analysis/io.py`
- `cod/outputs/predictions.csv`

**Ce aratam concret:**

- In `cli.py`, blocul pentru `args.command == "predict-file"`.
- In `predictions.csv`, aratam coloanele cu scoruri.

**Comanda de demo:**

```powershell
python emotion_cli.py predict-file --input data/sample_texts.csv --output outputs/predictions.csv --method hybrid
```

---

## 20. Experimentul final

**Vorbeste: Student 3**

<span style="color: green;">
Experimentul final este rulat prin comanda run-experiments. Aceasta compara cele trei metode: lexicon, nb si hybrid. Pentru fiecare metoda se salveaza predictiile, matricea de confuzie, distributia predictiilor si metricile. La final se genereaza si un fisier de comparatie intre metode.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/experiments.py`

**Ce aratam concret:**

- `DEFAULT_METHODS = ("lexicon", "nb", "hybrid")`
- `run_experiment_suite(...)`
- bucla `for method in methods`
- apelul catre `classification_metrics(...)`
- apelurile de scriere CSV/SVG/JSON

**Comanda de demo:**

```powershell
python emotion_cli.py run-experiments
```

---

## 21. Metricile de evaluare

**Vorbeste: Student 3**

<span style="color: green;">
Pentru evaluare calculam accuracy, macro precision, macro recall si macro F1. Macro F1 este important deoarece avem clasificare multiclass si vrem ca fiecare emotie sa conteze egal, nu doar clasele care apar mai des.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/metrics.py`

**Ce aratam concret:**

- `classification_metrics(...)`
- `confusion_matrix(...)`
- calculul pentru:
  - `tp`
  - `fp`
  - `fn`
  - `precision`
  - `recall`
  - `f1`
  - `macro_f1`

---

## 22. Output-urile experimentului

**Vorbeste: Student 3**

<span style="color: green;">
Rezultatele experimentului sunt salvate in folderul outputs/final_experiment. Aici avem un fisier metrics.json cu rezumatul complet, un CSV de comparatie intre metode, predictii separate pentru fiecare metoda, matrici de confuzie si distributii in format CSV si SVG.
</span>

**Aratam in fisiere:**

- `cod/outputs/final_experiment/metrics.json`
- `cod/outputs/final_experiment/method_comparison.csv`
- `cod/outputs/final_experiment/domain_metrics.csv`
- `cod/outputs/final_experiment/predictions_lexicon.csv`
- `cod/outputs/final_experiment/predictions_nb.csv`
- `cod/outputs/final_experiment/predictions_hybrid.csv`
- `cod/outputs/final_experiment/confusion_lexicon.csv`
- `cod/outputs/final_experiment/confusion_nb.csv`
- `cod/outputs/final_experiment/confusion_hybrid.csv`

---

## 23. Graficele generate

**Vorbeste: Student 3**

<span style="color: green;">
Pentru vizualizare am generat si grafice SVG cu distributia etichetelor reale si distributia predictiilor. Am ales SVG pentru ca poate fi generat fara librarii externe si poate fi deschis usor in browser sau inclus in documente.
</span>

**Aratam in cod si fisiere:**

- `cod/src/emotion_analysis/visualization.py`
- `cod/outputs/final_experiment/gold_distribution.svg`
- `cod/outputs/final_experiment/predicted_distribution_lexicon.svg`
- `cod/outputs/final_experiment/predicted_distribution_nb.svg`
- `cod/outputs/final_experiment/predicted_distribution_hybrid.svg`

**Ce aratam concret in cod:**

- `COLORS`
- `write_distribution_svg(...)`
- `escape_xml(value)`

---

## 24. Rezultatele obtinute

**Vorbeste: Student 3**

<span style="color: green;">
In fisierul method_comparison.csv putem vedea comparatia intre metode. Acesta este tabelul principal pentru rezultate, deoarece contine accuracy, macro precision, macro recall si macro F1 pentru fiecare metoda. Pe baza acestor valori putem discuta care metoda se comporta cel mai bine si unde apar diferentele.
</span>

**Aratam in fisiere:**

- `cod/outputs/final_experiment/method_comparison.csv`
- `cod/outputs/final_experiment/metrics.json`

**Ce spunem daca profesorul intreaba de ce scorurile nu sunt perfecte:**

<span style="color: green;">
Scorurile nu sunt perfecte deoarece detectarea emotiilor este o problema subiectiva. Unele texte pot contine mai multe emotii in acelasi timp, iar modelul nostru alege o singura emotie dominanta. In plus, metoda lexicala depinde de acoperirea lexiconului, iar Naive Bayes este antrenat slab-supervizat din intrari de lexicon, nu dintr-un corpus foarte mare de propozitii reale.
</span>

---

## 25. Metrici pe domenii

**Vorbeste: Student 3**

<span style="color: green;">
Am adaugat si evaluare pe domenii. Asta inseamna ca putem vedea separat cum se comporta modelul pe texte de tip social, news si blog. Aceasta analiza este utila pentru ca stilul textelor poate influenta performanta modelului.
</span>

**Aratam in cod si output:**

- `cod/src/emotion_analysis/experiments.py`
- `cod/outputs/final_experiment/domain_metrics.csv`

**Ce aratam concret in cod:**

- `scores_by_domain(...)`
- `write_domain_csv(...)`

---

## 26. Testele automate

**Vorbeste: Student 3**

<span style="color: green;">
Am scris teste automate pentru componentele principale. Testele verifica modelul lexical, modelul Naive Bayes, metoda hybrid, metricile, validarea parametrilor si faptul ca experimentul scrie fisierele asteptate. Astfel putem modifica proiectul fara sa stricam functionalitatea principala.
</span>

**Aratam in cod:**

- `cod/tests/test_core.py`

**Ce aratam concret:**

- `test_lexicon_scores_known_words`
- `test_nb_learns_simple_examples`
- `test_pipeline_hybrid_with_injected_nb`
- `test_metrics_macro_f1`
- `test_invalid_hybrid_weight_is_rejected`
- `test_experiment_suite_writes_outputs`

**Comanda de demo:**

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
```

---

## 27. Demo live - predict pe un text

**Vorbeste: Student 1**

<span style="color: green;">
Acum putem demonstra rapid sistemul pe un text introdus direct in terminal. Alegem metoda hybrid, deoarece aceasta combina avantajele lexiconului si ale modelului Naive Bayes.
</span>

**Comanda:**

```powershell
python emotion_cli.py predict --text "I am happy but also a little afraid." --method hybrid
```

**Ce aratam dupa rulare:**

- `dominant_emotion`
- `confidence`
- `top_scores`
- eventual `evidence`, daca apar potriviri lexicale.

**Aratam in cod:**

- `cod/src/emotion_analysis/cli.py`
- `cod/src/emotion_analysis/pipeline.py`

---

## 28. Demo live - predictii pe CSV

**Vorbeste: Student 2**

<span style="color: green;">
Pentru mai multe texte, folosim fisierul sample_texts.csv. Comanda predict-file citeste toate randurile si scrie predictiile in outputs/predictions.csv.
</span>

**Comanda:**

```powershell
python emotion_cli.py predict-file --input data/sample_texts.csv --output outputs/predictions.csv --method hybrid
```

**Aratam in fisiere:**

- `cod/data/sample_texts.csv`
- `cod/outputs/predictions.csv`

---

## 29. Demo live - experiment complet

**Vorbeste: Student 3**

<span style="color: green;">
Pentru evaluarea finala rulam run-experiments. Aceasta comanda foloseste datasetul final_eval_texts.csv si regenereaza toate fisierele din outputs/final_experiment.
</span>

**Comanda:**

```powershell
python emotion_cli.py run-experiments
```

**Aratam in fisiere:**

- `cod/data/final_eval_texts.csv`
- `cod/outputs/final_experiment/method_comparison.csv`
- `cod/outputs/final_experiment/metrics.json`

---

## 30. De ce nu am folosit GPU / RunPod / Kaggle

**Vorbeste: Student 1**

<span style="color: green;">
Pentru acest proiect nu a fost necesar GPU, RunPod sau Kaggle, deoarece implementarea noastra foloseste metode usoare si explicabile: lexicon, Naive Bayes si o combinatie hybrid. Aceste metode ruleaza local, fara training deep learning costisitor. Pentru tema noastra, avantajul este ca putem explica fiecare pas si putem reproduce rezultatele rapid.
</span>

**Aratam in cod:**

- `cod/requirements.txt`
- `cod/src/emotion_analysis/lexicon_model.py`
- `cod/src/emotion_analysis/nb_model.py`

**Ce aratam concret:**

- In `requirements.txt`, aratam ca partea principala nu are dependinte externe.
- In modele, aratam ca nu folosim retele neuronale sau GPU.

---

## 31. Limitari

**Vorbeste: Student 2**

<span style="color: green;">
Proiectul are si limitari. In primul rand, multe texte pot exprima mai multe emotii simultan, dar sistemul alege o singura emotie dominanta. In al doilea rand, metoda lexicala depinde de termenii existenti in lexicon. In al treilea rand, modelul Naive Bayes este antrenat din lexicon, deci nu are aceeasi putere ca un model mare antrenat pe milioane de exemple reale.
</span>

**Aratam in cod:**

- `cod/src/emotion_analysis/lexicon_model.py`
- `cod/src/emotion_analysis/nb_model.py`
- `cod/src/emotion_analysis/pipeline.py`

**Ce aratam concret:**

- In `lexicon_model.py`, faptul ca se cauta tokeni in lexicon.
- In `nb_model.py`, faptul ca trainingul vine din `train_nb_from_lexicon`.
- In `pipeline.py`, faptul ca se alege o singura `dominant_emotion`.

---

## 32. Posibile imbunatatiri

**Vorbeste: Student 2**

<span style="color: green;">
Ca imbunatatiri viitoare, am putea folosi un dataset real mai mare, etichetat manual la nivel de propozitie. De asemenea, am putea implementa multi-label classification, astfel incat un text sa poata avea mai multe emotii simultan. O alta directie ar fi compararea cu un model transformer, cum ar fi BERT, dar acesta ar necesita mai multe resurse si o discutie separata despre training.
</span>

**Aratam in proiect:**

- `cod/data/final_eval_texts.csv`
- `cod/src/emotion_analysis/pipeline.py`

**Ce explicam:**

- Datasetul curent este suficient pentru proiect, dar poate fi extins.
- Pipeline-ul este modular, deci ar putea primi o metoda noua.

---

## 33. Concluzie

**Vorbeste: Student 3**

<span style="color: green;">
In concluzie, am construit un sistem complet de emotion analysis. Sistemul citeste texte, le preproceseaza, aplica trei metode de predictie, salveaza rezultate, calculeaza metrici si genereaza grafice. Codul este organizat modular, are teste automate si poate fi rulat local prin comenzi simple.
</span>

**Aratam in proiect:**

- `README.md`
- `cod/src/emotion_analysis/`
- `cod/data/final_eval_texts.csv`
- `cod/outputs/final_experiment/`
- `cod/tests/test_core.py`

---

## 34. Incheiere

**Vorbeste: Student 1**

<span style="color: green;">
Acesta a fost proiectul nostru. Am incercat sa avem nu doar o predictie simpla, ci un pipeline complet si reproductibil: date, modele, evaluare, output-uri si teste. Va multumim!
</span>

---

# Impartirea Pe Membri

## Student 1

Parti recomandate:

- 1. Deschiderea prezentarii
- 2. Tema proiectului
- 3. Ce face aplicatia finala
- 4. Structura proiectului
- 5. Resursa principala
- 6. Incarcarea lexiconului
- 27. Demo predict text
- 30. De ce nu am folosit GPU
- 34. Incheiere

## Student 2

Parti recomandate:

- 7. Preprocesarea textului
- 8. Negatii si intensificatori
- 9. Modelul lexical
- 10. Output lexical
- 11. Naive Bayes
- 12. Trasaturi de cuvant si caractere
- 13. Antrenarea NB
- 14. Predictia NB
- 15. Hybrid
- 16. EmotionAnalyzer
- 28. Demo predictii CSV
- 31. Limitari
- 32. Posibile imbunatatiri

## Student 3

Parti recomandate:

- 17. Datele de intrare
- 18. CSV input/output
- 19. Comanda predict-file
- 20. Experimentul final
- 21. Metricile
- 22. Output-urile
- 23. Graficele
- 24. Rezultatele
- 25. Metrici pe domenii
- 26. Testele automate
- 29. Demo experiment complet
- 33. Concluzie

---

# Lista Rapida: Ce Aratam Pe Ecran

1. `cod/src/emotion_analysis/constants.py` - lista celor 8 emotii.
2. `cod/src/emotion_analysis/text.py` - preprocesare, tokenizare, negatii, intensificatori.
3. `cod/src/emotion_analysis/resources.py` - incarcarea lexiconului NRC.
4. `cod/src/emotion_analysis/lexicon_model.py` - metoda lexicala.
5. `cod/src/emotion_analysis/nb_model.py` - Naive Bayes.
6. `cod/src/emotion_analysis/pipeline.py` - metoda hybrid si `EmotionAnalyzer`.
7. `cod/src/emotion_analysis/io.py` - citire/scriere CSV.
8. `cod/src/emotion_analysis/metrics.py` - metrici.
9. `cod/src/emotion_analysis/experiments.py` - experimentul final.
10. `cod/src/emotion_analysis/visualization.py` - grafice SVG.
11. `cod/src/emotion_analysis/cli.py` - comenzile CLI.
12. `cod/data/final_eval_texts.csv` - datasetul final.
13. `cod/outputs/final_experiment/method_comparison.csv` - comparatia metodelor.
14. `cod/outputs/final_experiment/metrics.json` - rezumat complet.
15. `cod/tests/test_core.py` - teste automate.

---

# Ghid Foarte Precis: Ce Aratam In Cod, Pas Cu Pas

Aceasta sectiune este pentru prezentarea cu ecranul partajat. Cand spunem ca am implementat ceva, deschidem exact fisierul indicat si aratam exact zona mentionata.

## A. Pornirea aplicatiei din terminal

**Deschidem:** `cod/emotion_cli.py`

**Aratam exact:**

```python
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from emotion_analysis.cli import main
```

<span style="color: green;">
Aici se vede punctul de pornire al aplicatiei. Fisierul adauga folderul src in path, apoi importa functia main din CLI-ul proiectului. De aceea putem rula proiectul direct cu python emotion_cli.py.
</span>

**Apoi aratam:**

```python
if __name__ == "__main__":
    raise SystemExit(main())
```

<span style="color: green;">
Aceasta linie porneste efectiv aplicatia cand fisierul este rulat din terminal.
</span>

---

## B. Lista de emotii folosite in proiect

**Deschidem:** `cod/src/emotion_analysis/constants.py`

**Aratam exact:**

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

<span style="color: green;">
Aici sunt cele 8 clase pe care le prezice sistemul. Toate modelele, metricile, CSV-urile si graficele folosesc aceeasi lista, ca sa avem o ordine stabila si sa evitam diferente intre fisiere.
</span>

**Daca profesorul intreaba unde se foloseste lista:**

<span style="color: green;">
Lista este importata in modelele de predictie, in calculul metricilor, in generarea output-urilor CSV si in graficele SVG.
</span>

---

## C. Tokenizarea si normalizarea textului

**Deschidem:** `cod/src/emotion_analysis/text.py`

**Aratam exact expresiile regulate:**

```python
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
TOKEN_PATTERN = re.compile(r"#?[\w][\w'_-]*|[!?]+", re.UNICODE)
LONG_CHAR_RUN = re.compile(r"(.)\1{2,}")
```

<span style="color: green;">
Aici sunt regulile de baza pentru curatarea textului. Detectam URL-uri, extragem tokeni si reducem repetitiile exagerate de caractere, de exemplu forma soooo devine mai stabila pentru procesare.
</span>

**Apoi aratam functia:**

```python
def normalize_text(text: str) -> str:
    without_links = URL_PATTERN.sub(" URL ", text)
    return without_links.lower()
```

<span style="color: green;">
Aceasta functie elimina efectul linkurilor si transforma textul in lowercase, pentru ca Happy si happy sa fie tratate la fel.
</span>

**Apoi aratam functia:**

```python
def normalize_token(token: str) -> str:
    token = token.strip().lower()
    token = token.strip("\"'.,;:()[]{}")
    return LONG_CHAR_RUN.sub(r"\1\1", token)
```

<span style="color: green;">
Aici curatam fiecare token individual. Eliminam punctuatia de la margini si reducem secventele foarte lungi de caractere repetate.
</span>

**Apoi aratam functia:**

```python
def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    tokens: list[str] = []
    for match in TOKEN_PATTERN.finditer(normalized):
        token = normalize_token(match.group(0))
        if not token or token == "url":
            continue
        tokens.append(token)
    return tokens
```

<span style="color: green;">
Aceasta este functia care transforma textul brut intr-o lista de tokeni folosita mai departe de ambele modele.
</span>

---

## D. Negatii si intensificatori

**Ramanem in:** `cod/src/emotion_analysis/text.py`

**Aratam exact:**

```python
NEGATIONS = {
    "no",
    "not",
    "never",
    ...
    "nu",
    "niciodata",
    "nimic",
    "nimeni",
}
```

<span style="color: green;">
Aici avem lista de negatii. Ea conteaza pentru cazuri precum not happy, unde termenul happy exista, dar contextul ii reduce intensitatea emotionala.
</span>

**Aratam exact:**

```python
INTENSIFIERS = {
    "very",
    "really",
    "extremely",
    ...
    "foarte",
    "super",
    "extrem",
}
```

<span style="color: green;">
Aici avem intensificatori. Ei cresc contributia unui termen emotional, de exemplu very happy ar trebui sa conteze mai mult decat happy simplu.
</span>

**Apoi deschidem:** `cod/src/emotion_analysis/lexicon_model.py`

**Aratam exact:**

```python
def recent_context_multiplier(tokens: list[str], token_index: int) -> float:
    multiplier = 1.0
    if has_recent_negation(tokens, token_index):
        multiplier *= 0.35
    if has_recent_intensifier(tokens, token_index):
        multiplier *= 1.35
    return multiplier
```

<span style="color: green;">
Aici se vede cum folosim efectiv negatiile si intensificatorii. Negatia scade scorul, iar intensificatorul il creste.
</span>

---

## E. Calea catre lexiconul NRC

**Deschidem:** `cod/src/emotion_analysis/resources.py`

**Aratam exact:**

```python
DEFAULT_LEXICON_RELATIVE = Path(
    "linkuri_extrase"
    "/archives"
    "/061_saifmohammad.com_NRC-Hashtag-Emotion-Lexicon-v0.2"
    "/NRC-Hashtag-Emotion-Lexicon-v0.2"
    "/NRC-Hashtag-Emotion-Lexicon-v0.2.txt"
)
```

<span style="color: green;">
Aceasta este calea catre lexiconul NRC folosit de proiect. Lexiconul este in resursele extrase, iar codul stie sa il gaseasca automat.
</span>

**Apoi aratam:**

```python
@dataclass(frozen=True)
class LexiconEntry:
    emotion: str
    term: str
    score: float
```

<span style="color: green;">
Fiecare rand valid din lexicon este reprezentat printr-un LexiconEntry: emotia, termenul si scorul asociat.
</span>

**Apoi aratam in `load_hashtag_entries`:**

```python
parts = line.rstrip("\n").split("\t")
if len(parts) != 3:
    continue
emotion, raw_term, raw_score = parts
```

<span style="color: green;">
Aici citim lexiconul linie cu linie. Fiecare linie trebuie sa aiba trei campuri: emotie, termen si scor.
</span>

**Apoi aratam:**

```python
score = float(raw_score)
...
term = normalize_token(raw_term)
...
entries.append(LexiconEntry(emotion=emotion, term=term, score=score))
```

<span style="color: green;">
Aici convertim scorul in numar, normalizam termenul si salvam intrarea in lista de intrari folosite de modele.
</span>

---

## F. Modelul lexical: cum se calculeaza scorurile

**Deschidem:** `cod/src/emotion_analysis/lexicon_model.py`

**Aratam exact constructorul:**

```python
class WeightedEmotionLexicon:
    def __init__(
        self,
        lexicon: dict[str, dict[str, float]] | None = None,
        *,
        lexicon_path: str | None = None,
        max_entries_per_emotion: int | None = None,
    ) -> None:
        self.lexicon = lexicon or load_hashtag_lexicon(
            lexicon_path,
            max_entries_per_emotion=max_entries_per_emotion,
            min_score=0.0,
        )
```

<span style="color: green;">
Aici se construieste modelul lexical. Daca nu ii dam noi un lexicon manual, el incarca automat NRC Hashtag Emotion Lexicon.
</span>

**Apoi aratam inceputul metodei `score`:**

```python
tokens = tokenize(text)
emotion_totals = {emotion: 0.0 for emotion in EMOTIONS}
lexicon_hits: list[LexiconHit] = []
```

<span style="color: green;">
Pentru fiecare text, il tokenizam, apoi initializam scorul fiecarei emotii cu zero.
</span>

**Apoi aratam partea centrala:**

```python
for index, token in enumerate(tokens):
    context_multiplier = recent_context_multiplier(tokens, index)

    checked_terms: set[str] = set()
    for term in token_variants(token):
        if term in checked_terms:
            continue
        checked_terms.add(term)

        for emotion in EMOTIONS:
            weight = self.lexicon[emotion].get(term)
            if weight is None or weight <= 0:
                continue
            contribution = weight * context_multiplier
            emotion_totals[emotion] += contribution
```

<span style="color: green;">
Aceasta este logica principala a metodei lexicale. Pentru fiecare token, verificam variantele lui, cautam termenul in lexicon pentru fiecare emotie si adaugam contributia la scorul emotiei.
</span>

**Apoi aratam finalul metodei:**

```python
normalized = normalize_emotion_totals(emotion_totals)
dominant = max(normalized, key=normalized.get) if normalized else None
```

<span style="color: green;">
La final normalizam scorurile si alegem emotia cu scorul cel mai mare.
</span>

---

## G. Dovezile lexicale din output

**Ramanem in:** `cod/src/emotion_analysis/lexicon_model.py`

**Aratam exact `LexiconHit`:**

```python
@dataclass
class LexiconHit:
    emotion: str
    term: str
    token_index: int
    contribution: float
```

<span style="color: green;">
Aceasta structura retine dovezile gasite in text: ce termen a fost gasit, pentru ce emotie si cu ce contributie.
</span>

**Apoi aratam in `score`:**

```python
lexicon_hits.append(
    LexiconHit(
        emotion=emotion,
        term=term,
        token_index=index,
        contribution=contribution,
    )
)
```

<span style="color: green;">
De fiecare data cand gasim un termen relevant in lexicon, salvam si dovada, nu doar scorul.
</span>

**Apoi aratam `summarize_lexicon_hits`:**

```python
ranked_hits = sorted(grouped.items(), key=lambda group: group[1], reverse=True)
return [
    {"emotion": emotion, "term": term, "contribution": round(contribution, 4)}
    for (emotion, term), contribution in ranked_hits[:limit]
]
```

<span style="color: green;">
Aici grupam dovezile si pastram cele mai importante contributii. Asa putem explica de ce modelul a ales o anumita emotie.
</span>

---

## H. Naive Bayes: structura modelului

**Deschidem:** `cod/src/emotion_analysis/nb_model.py`

**Aratam exact:**

```python
@dataclass
class TrainingExample:
    text: str
    label: str
    weight: float = 1.0
```

<span style="color: green;">
Acesta este formatul unui exemplu de antrenare pentru Naive Bayes: text, eticheta emotionala si greutate.
</span>

**Apoi aratam constructorul `EmotionNaiveBayes`:**

```python
self.vocabulary: set[str] = set()
self.class_feature_counts: dict[str, Counter[str]] = {
    label: Counter() for label in self.labels
}
self.class_totals = {label: 0.0 for label in self.labels}
self.class_priors = {label: 0.0 for label in self.labels}
self._fitted = False
```

<span style="color: green;">
Aici se vad structurile interne ale modelului: vocabularul, frecventele trasaturilor pe clasa, totalurile pe clasa si priorurile claselor.
</span>

---

## I. Naive Bayes: antrenarea din lexicon

**Ramanem in:** `cod/src/emotion_analysis/nb_model.py`

**Aratam exact `train_nb_from_lexicon`:**

```python
entries = load_hashtag_entries(
    lexicon_path,
    max_entries_per_emotion=max_per_emotion,
    min_score=min_score,
)
examples = [
    nrc_entry_to_training_example(entry)
    for entry in entries
    if looks_like_training_phrase(entry.term)
]
return EmotionNaiveBayes().fit(examples)
```

<span style="color: green;">
Aici se vede cum antrenam modelul din lexicon. Incarcam intrarile NRC, filtram termenii nepotriviti, le transformam in exemple de antrenare si apelam fit.
</span>

**Apoi aratam `nrc_entry_to_training_example`:**

```python
usable_score = min(max(entry.score, 0.0), 3.0)
phrase = entry.term.replace("_", " ")
return TrainingExample(text=phrase, label=entry.emotion, weight=1.0 + usable_score)
```

<span style="color: green;">
Scorul din lexicon este folosit ca greutate. Termenii mai puternic asociati cu o emotie au influenta mai mare la antrenare.
</span>

**Apoi aratam in `fit`:**

```python
feature_counts = count_emotion_token_features(example.text)
...
weighted_hits = count * weight
self.class_feature_counts[example.label][feature] += weighted_hits
self.class_totals[example.label] += weighted_hits
self.vocabulary.add(feature)
```

<span style="color: green;">
In fit, transformam fiecare exemplu in trasaturi si actualizam frecventele pentru clasa corespunzatoare.
</span>

---

## J. Naive Bayes: feature extraction

**Ramanem in:** `cod/src/emotion_analysis/nb_model.py`

**Aratam exact:**

```python
def count_emotion_token_features(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    tokens = tokenize(text)
```

<span style="color: green;">
Aceasta functie transforma un text in trasaturi numerice pentru modelul Naive Bayes.
</span>

**Apoi aratam:**

```python
if token.startswith("#") and len(token) > 1:
    counts[f"word={token[1:]}"] += 1
counts[f"word={token}"] += 2
```

<span style="color: green;">
Aici adaugam trasaturi de cuvant. Pentru hashtaguri folosim si forma fara diez.
</span>

**Apoi aratam:**

```python
padded_token = f"^{token}$"

for width in (3, 4, 5):
    last_start = len(padded_token) - width
    if last_start < 0:
        continue

    for start in range(last_start + 1):
        ngram = padded_token[start:start + width]
        counts[f"char{width}={ngram}"] += 1
```

<span style="color: green;">
Aici extragem n-grame de caractere de lungime 3, 4 si 5. Acestea ajuta modelul sa generalizeze la forme asemanatoare ale cuvintelor.
</span>

---

## K. Naive Bayes: predictia

**Ramanem in:** `cod/src/emotion_analysis/nb_model.py`

**Aratam exact `predict_proba`:**

```python
features = count_emotion_token_features(text)
vocab_size = max(len(self.vocabulary), 1)
log_scores: dict[str, float] = {}
for label in self.labels:
    log_score = math.log(self.class_priors[label])
    denominator = self.class_totals[label] + self.alpha * vocab_size
```

<span style="color: green;">
La predictie, extragem trasaturile textului si calculam un scor logaritmic pentru fiecare emotie.
</span>

**Apoi aratam:**

```python
probability = (observed + self.alpha) / denominator
log_score += count * math.log(probability)
```

<span style="color: green;">
Aceasta este formula cu smoothing. Alpha evita probabilitati zero pentru trasaturi nevazute.
</span>

**Apoi aratam `predict`:**

```python
scores = self.predict_proba(text)
dominant = max(scores, key=scores.get)
```

<span style="color: green;">
Dupa ce avem probabilitatile, alegem emotia cu scorul cel mai mare.
</span>

---

## L. Metoda hybrid

**Deschidem:** `cod/src/emotion_analysis/pipeline.py`

**Aratam exact constructorul:**

```python
if not 0.0 <= hybrid_lexicon_weight <= 1.0:
    raise ValueError("hybrid_lexicon_weight must be between 0 and 1.")
```

<span style="color: green;">
Aici validam greutatea metodei hybrid. Ea trebuie sa fie intre 0 si 1.
</span>

**Apoi aratam in `analyze`:**

```python
if method == "lexicon":
    return self.lexicon_model.score(text)
if method == "nb":
    return self._nb_model().predict(text)
if method != "hybrid":
    raise ValueError("method must be one of: lexicon, nb, hybrid")
```

<span style="color: green;">
Aici se vede ca pipeline-ul poate rula una dintre cele trei metode.
</span>

**Apoi aratam combinarea hybrid:**

```python
lexicon_result = self.lexicon_model.score(text)
nb_result = self._nb_model().predict(text)
lexicon_share = self.hybrid_lexicon_weight
nb_share = 1.0 - lexicon_share
scores = {
    emotion: lexicon_share * lexicon_result["scores"][emotion]
    + nb_share * nb_result["scores"][emotion]
    for emotion in EMOTIONS
}
dominant = max(scores, key=scores.get)
```

<span style="color: green;">
Aceasta este metoda hybrid. Rulam ambele modele, combinam scorurile pentru fiecare emotie si alegem emotia dominanta.
</span>

**Apoi aratam `_nb_model`:**

```python
if self.nb_model is None:
    self.nb_model = train_nb_from_lexicon(
        self.lexicon_path,
        max_per_emotion=self.nb_max_per_emotion,
    )
return self.nb_model
```

<span style="color: green;">
Modelul Naive Bayes este creat doar cand este necesar. Acest lucru face metoda lexicala mai rapida cand este rulata separat.
</span>

---

## M. Citirea CSV-urilor

**Deschidem:** `cod/src/emotion_analysis/io.py`

**Aratam exact:**

```python
def read_text_rows(path: str | Path, *, text_column: str = "text") -> list[dict[str, str]]:
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = csv.DictReader(handle)
        if rows.fieldnames is None or text_column not in rows.fieldnames:
            raise ValueError(f"CSV must contain a '{text_column}' column.")
        return list(rows)
```

<span style="color: green;">
Aici citim datele din CSV si verificam explicit ca exista coloana de text. Daca nu exista, programul opreste rularea cu o eroare clara.
</span>

---

## N. Scrierea predictiilor CSV

**Ramanem in:** `cod/src/emotion_analysis/io.py`

**Aratam exact lista de coloane:**

```python
columns = [
    ID_COLUMN,
    SOURCE_ID_COLUMN,
    "text",
    "method",
    "dominant_emotion",
    PREDICTION_COLUMN,
    "confidence",
    "coverage",
]
columns.extend(f"score_{emotion}" for emotion in EMOTIONS)
```

<span style="color: green;">
Aici se vede formatul output-ului pentru predictii. Pentru fiecare text salvam metoda, emotia dominanta, confidence, coverage si scorul fiecarei emotii.
</span>

**Apoi aratam `flatten_prediction`:**

```python
csv_row: dict[str, Any] = {
    ID_COLUMN: row_id,
    SOURCE_ID_COLUMN: row_id,
    "text": prediction["text"],
    "method": prediction["method"],
    "dominant_emotion": prediction["dominant_emotion"],
    PREDICTION_COLUMN: prediction["dominant_emotion"],
    "confidence": round(float(prediction["confidence"]), 4),
    "coverage": round(float(prediction.get("coverage", 0.0)), 4),
}
```

<span style="color: green;">
Aceasta functie transforma predictia interna intr-un rand plat, potrivit pentru CSV.
</span>

---

## O. Metricile

**Deschidem:** `cod/src/emotion_analysis/metrics.py`

**Aratam exact validarea:**

```python
if len(gold_labels) != len(predicted_labels):
    raise ValueError("gold_labels and predicted_labels must have the same length.")
```

<span style="color: green;">
Inainte de evaluare verificam ca avem acelasi numar de etichete reale si predictii.
</span>

**Apoi aratam calculul TP/FP/FN:**

```python
tp = confusion[label][label]
fp = sum(confusion[other][label] for other in labels if other != label)
fn = sum(confusion[label][other] for other in labels if other != label)
```

<span style="color: green;">
Aici calculam true positives, false positives si false negatives pentru fiecare emotie.
</span>

**Apoi aratam formulele:**

```python
precision = tp / (tp + fp) if tp + fp else 0.0
recall = tp / (tp + fn) if tp + fn else 0.0
f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
```

<span style="color: green;">
Pe baza acestor valori calculam precision, recall si F1 pentru fiecare emotie.
</span>

**Apoi aratam macro:**

```python
macro_precision = sum(float(values["precision"]) for values in per_label.values()) / len(labels)
macro_recall = sum(float(values["recall"]) for values in per_label.values()) / len(labels)
macro_f1 = sum(float(values["f1"]) for values in per_label.values()) / len(labels)
```

<span style="color: green;">
Macro inseamna media pe toate emotiile, astfel incat fiecare clasa conteaza egal.
</span>

---

## P. Experimentul final: citire, validare, output

**Deschidem:** `cod/src/emotion_analysis/experiments.py`

**Aratam exact semnatura:**

```python
def run_experiment_suite(
    *,
    input_path: str | Path = "data/final_eval_texts.csv",
    output_dir: str | Path = "outputs/final_experiment",
    text_column: str = "text",
    label_column: str = "label",
    domain_column: str = "domain",
    methods: tuple[str, ...] = DEFAULT_METHODS,
    ...
) -> dict[str, Any]:
```

<span style="color: green;">
Aceasta este functia principala a experimentului. Implicit citeste datasetul final si scrie rezultatele in outputs/final_experiment.
</span>

**Apoi aratam:**

```python
rows = read_text_rows(input_path, text_column=text_column)
check_labels(rows, label_column=label_column)
check_methods(methods)

out_dir = Path(output_dir)
out_dir.mkdir(parents=True, exist_ok=True)
```

<span style="color: green;">
La inceput citim datele, verificam etichetele, verificam metodele si pregatim folderul de output.
</span>

**Apoi aratam distributia gold:**

```python
gold = [row[label_column] for row in rows]
summary["gold_distribution"] = label_distribution(gold)

write_dist_csv(out_dir / "gold_distribution.csv", summary["gold_distribution"])
write_distribution_svg(
    out_dir / "gold_distribution.svg",
    summary["gold_distribution"],
    title="Gold emotion distribution",
)
```

<span style="color: green;">
Inainte de predictii salvam distributia etichetelor reale, atat CSV cat si SVG.
</span>

---

## Q. Experimentul final: bucla pe metode

**Ramanem in:** `cod/src/emotion_analysis/experiments.py`

**Aratam exact:**

```python
for method in methods:
    out_rows: list[dict[str, Any]] = []
    preds: list[str] = []

    for row in rows:
        prediction = analyzer.analyze(row[text_column], method=method)
        preds.append(prediction["dominant_emotion"])
        out_row = flatten_prediction(row, prediction)
```

<span style="color: green;">
Aici se vede ca rulam fiecare metoda pe fiecare rand din dataset. Pentru fiecare text salvam predictia si pregatim randul de output.
</span>

**Apoi aratam metricile:**

```python
metrics = classification_metrics(gold, preds)
distribution = label_distribution(preds)
```

<span style="color: green;">
Dupa ce avem predictiile unei metode, calculam metricile si distributia predictiilor.
</span>

**Apoi aratam fisierele scrise:**

```python
write_preds_csv(out_dir / f"predictions_{method}.csv", out_rows)
write_conf_csv(out_dir / f"confusion_{method}.csv", metrics["confusion"])
write_dist_csv(out_dir / f"predicted_distribution_{method}.csv", distribution)
write_distribution_svg(
    out_dir / f"predicted_distribution_{method}.svg",
    distribution,
    title=f"Predicted emotion distribution - {method}",
)
```

<span style="color: green;">
Aici se vede exact unde generam fisierele de predictii, matricea de confuzie si distributiile pentru fiecare metoda.
</span>

---

## R. Comparatia intre metode

**Ramanem in:** `cod/src/emotion_analysis/experiments.py`

**Aratam exact:**

```python
comparison.append(
    {
        "method": method,
        "accuracy": metrics["accuracy"],
        "macro_precision": metrics["macro_precision"],
        "macro_recall": metrics["macro_recall"],
        "macro_f1": metrics["macro_f1"],
        "total": metrics["total"],
    }
)
```

<span style="color: green;">
Aici construim randul de comparatie pentru fiecare metoda.
</span>

**Apoi aratam:**

```python
write_compare_csv(out_dir / "method_comparison.csv", comparison)
write_domain_csv(out_dir / "domain_metrics.csv", summary)
(out_dir / "metrics.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False),
    encoding="utf-8",
)
```

<span style="color: green;">
La final scriem comparatia intre metode, metricile pe domenii si rezumatul complet in metrics.json.
</span>

---

## S. Metrici pe domenii

**Ramanem in:** `cod/src/emotion_analysis/experiments.py`

**Aratam exact:**

```python
def scores_by_domain(
    rows: list[dict[str, str]],
    preds: list[str],
    label_column: str,
    domain_column: str,
) -> dict[str, dict[str, Any]]:
```

<span style="color: green;">
Aceasta functie calculeaza performanta separat pe domenii, de exemplu social, news si blog.
</span>

**Apoi aratam:**

```python
gold_by_domain: dict[str, list[str]] = defaultdict(list)
pred_by_domain: dict[str, list[str]] = defaultdict(list)
for row, pred in zip(rows, preds):
    domain = row.get(domain_column, "unknown") or "unknown"
    gold_by_domain[domain].append(row[label_column])
    pred_by_domain[domain].append(pred)
```

<span style="color: green;">
Aici grupam etichetele reale si predictiile dupa domeniul fiecarui text.
</span>

**Apoi aratam:**

```python
metrics = classification_metrics(gold_by_domain[domain], pred_by_domain[domain])
```

<span style="color: green;">
Pentru fiecare domeniu aplicam aceeasi functie de metrici ca la evaluarea globala.
</span>

---

## T. Grafice SVG

**Deschidem:** `cod/src/emotion_analysis/visualization.py`

**Aratam exact culorile:**

```python
COLORS = {
    "anger": "#d73027",
    "anticipation": "#fdae61",
    ...
    "trust": "#66bd63",
}
```

<span style="color: green;">
Aici fiecare emotie are o culoare stabila pentru grafice.
</span>

**Apoi aratam:**

```python
def write_distribution_svg(
    path: str | Path,
    distribution: dict[str, int],
    *,
    title: str = "Predicted emotion distribution",
) -> None:
```

<span style="color: green;">
Aceasta functie scrie graficul SVG pentru o distributie de emotii.
</span>

**Apoi aratam zona cu barele:**

```python
bar_width = int(chart_width * count / max_value)
color = COLORS[emotion]
svg_lines.extend(
    [
        ...
        f'<rect x="{margin_left}" y="{bar_y}" width="{bar_width}" height="24" rx="3" fill="{color}"/>',
        ...
    ]
)
```

<span style="color: green;">
Aici se calculeaza latimea fiecarei bare si se scrie dreptunghiul colorat in SVG.
</span>

---

## U. CLI-ul: comenzile disponibile

**Deschidem:** `cod/src/emotion_analysis/cli.py`

**Aratam exact:**

```python
subparsers = parser.add_subparsers(dest="command", required=True)
```

<span style="color: green;">
CLI-ul foloseste subcomenzi. Fiecare subcomanda corespunde unei functionalitati a proiectului.
</span>

**Aratam comanda `predict`:**

```python
predict_cmd = subparsers.add_parser("predict", help="Analyze one text.")
predict_cmd.add_argument("--text", required=True)
predict_cmd.add_argument("--method", choices=("lexicon", "nb", "hybrid"), default="hybrid")
```

<span style="color: green;">
Aceasta comanda analizeaza un singur text.
</span>

**Aratam comanda `predict-file`:**

```python
file_cmd = subparsers.add_parser("predict-file", help="Analyze a CSV file.")
file_cmd.add_argument("--input", required=True)
file_cmd.add_argument("--output", required=True)
```

<span style="color: green;">
Aceasta comanda analizeaza un fisier CSV si scrie predictiile intr-un alt CSV.
</span>

**Aratam comanda `run-experiments`:**

```python
experiment_cmd = subparsers.add_parser(
    "run-experiments",
    help="Compare lexicon, NB and hybrid on a labeled CSV dataset.",
)
```

<span style="color: green;">
Aceasta este comanda pentru experimentul final, unde comparam metodele pe datasetul etichetat.
</span>

---

## V. CLI-ul: unde se executa predict-file

**Ramanem in:** `cod/src/emotion_analysis/cli.py`

**Aratam exact:**

```python
if args.command == "predict-file":
    rows = read_text_rows(args.input, text_column=args.text_column)
    predictions = []
    for row in rows:
        prediction = analyzer.analyze(row[args.text_column], method=args.method)
        predictions.append(flatten_prediction(row, prediction))
    write_prediction_rows(args.output, predictions)
    print(f"Wrote {len(predictions)} predictions to {args.output}")
    return 0
```

<span style="color: green;">
Aici se vede tot fluxul pentru predictii pe CSV: citim randurile, analizam fiecare text, transformam predictia in rand CSV si scriem fisierul de output.
</span>

---

## W. CLI-ul: unde se executa run-experiments

**Ramanem in:** `cod/src/emotion_analysis/cli.py`

**Aratam exact:**

```python
if args.command == "run-experiments":
    summary = run_experiment_suite(
        input_path=args.input,
        output_dir=args.output_dir,
        text_column=args.text_column,
        label_column=args.label_column,
        domain_column=args.domain_column,
        methods=tuple(args.methods),
        lexicon_path=args.lexicon,
        hybrid_lexicon_weight=args.hybrid_weight,
    )
```

<span style="color: green;">
Aceasta bucata apeleaza functia principala de experiment si ii trimite toate setarile din terminal.
</span>

**Apoi aratam:**

```python
print_experiment_summary(summary, output_dir=args.output_dir)
```

<span style="color: green;">
Dupa rulare, CLI-ul afiseaza un sumar cu rezultatele metodelor.
</span>

---

## X. Datasetul final

**Deschidem:** `cod/data/final_eval_texts.csv`

**Aratam exact headerul:**

```csv
id,domain,label,text
```

<span style="color: green;">
Acesta este formatul datasetului final. Avem un id, un domeniu, eticheta corecta si textul analizat.
</span>

**Aratam cateva randuri din emotii diferite.**

<span style="color: green;">
Datasetul contine exemple pentru toate cele 8 emotii si pentru domenii diferite, ca social, news si blog.
</span>

**Apoi aratam in cod unde este citit:**

- `cod/src/emotion_analysis/experiments.py`
- linia cu `input_path: str | Path = "data/final_eval_texts.csv"`

---

## Y. Output-ul principal de comparatie

**Deschidem:** `cod/outputs/final_experiment/method_comparison.csv`

**Aratam headerul:**

```csv
method,accuracy,macro_precision,macro_recall,macro_f1,total
```

<span style="color: green;">
Acesta este fisierul principal pentru compararea metodelor. Fiecare rand este o metoda, iar coloanele sunt metricile de evaluare.
</span>

**Apoi deschidem:** `cod/src/emotion_analysis/experiments.py`

**Aratam exact:**

```python
write_compare_csv(out_dir / "method_comparison.csv", comparison)
```

<span style="color: green;">
Aici se vede unde este generat acest fisier.
</span>

---

## Z. Testele automate

**Deschidem:** `cod/tests/test_core.py`

**Aratam testul lexical:**

```python
def test_lexicon_scores_known_words(self):
    ...
    result = model.score("I am very happy, not furious.")
    self.assertEqual(result["dominant_emotion"], "joy")
```

<span style="color: green;">
Acest test verifica faptul ca modelul lexical tine cont de cuvinte emotionale, intensificatori si negatii.
</span>

**Aratam testul NB:**

```python
def test_nb_learns_simple_examples(self):
    ...
    result = model.predict("angry and furious")
    self.assertEqual(result["dominant_emotion"], "anger")
```

<span style="color: green;">
Acest test verifica faptul ca modelul Naive Bayes poate invata din exemple simple.
</span>

**Aratam testul experimentului:**

```python
def test_experiment_suite_writes_outputs(self):
    ...
    self.assertTrue((work_dir / "out" / "metrics.json").exists())
    self.assertTrue((work_dir / "out" / "predicted_distribution_hybrid.svg").exists())
```

<span style="color: green;">
Acest test verifica faptul ca experimentul complet scrie fisierele de output asteptate.
</span>

**Comanda de rulat:**

```powershell
$env:PYTHONPATH='src'
python -m unittest discover -s tests
```

<span style="color: green;">
Aceasta comanda ruleaza toate testele proiectului.
</span>

---

# Variante Scurte Pentru Intrebari Probabile

## De ce ati ales lexicon + Naive Bayes?

<span style="color: green;">
Am ales aceasta combinatie pentru ca lexiconul este interpretabil, iar Naive Bayes adauga o componenta de invatare si generalizare. Metoda hybrid combina cele doua avantaje.
</span>

## De ce nu deep learning?

<span style="color: green;">
Pentru cerinta proiectului am preferat o solutie reproductibila local, explicabila si fara dependente grele. Un model deep learning ar fi o extensie posibila, dar ar necesita mai multe date si resurse.
</span>

## Cum stim ca proiectul merge?

<span style="color: green;">
Avem teste automate in test_core.py, putem rula predictii pe texte simple si putem rula experimentul complet pe datasetul final. Output-urile sunt generate automat in outputs/final_experiment.
</span>

## Care este metoda finala recomandata?

<span style="color: green;">
Metoda finala recomandata este hybrid, deoarece foloseste atat scorurile lexiconului, cat si probabilitatile modelului Naive Bayes.
</span>

## Ce inseamna confidence?

<span style="color: green;">
Confidence este scorul normalizat al emotiei dominante. Nu trebuie interpretat ca probabilitate perfecta, ci ca nivel relativ de incredere al modelului pentru predictia aleasa.
</span>

## Ce inseamna coverage?

<span style="color: green;">
Coverage arata ce proportie din tokenii textului au fost acoperiti de lexicon. O acoperire mai mare inseamna ca metoda lexicala a gasit mai multe dovezi directe in text.
</span>
