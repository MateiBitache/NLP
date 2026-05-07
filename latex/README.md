# LaTeX Technical Report

Acest folder contine raportul tehnic complet pentru proiectul:

**Emotion Analysis in Text Using Lexicon-Based, Weakly Supervised, and Hybrid Methods**

## Structura

- `main.tex` - fisierul principal al documentului.
- `sections/` - sectiunile raportului: abstract, introducere, related work, metodologie, implementare, experimente, rezultate, limitari, etica, concluzie si appendix.
- `references.bib` - bibliografia BibTeX.

## Compilare in Overleaf

1. Creeaza un proiect nou in Overleaf.
2. Incarca toate fisierele din acest folder, pastrand structura `sections/`.
3. Seteaza `main.tex` ca fisier principal.
4. Compileaza cu pdfLaTeX.

## Compilare locala

Daca ai LaTeX instalat local:

```powershell
cd latex_document
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

In mediul curent nu am gasit `pdflatex` in PATH, deci documentul nu a fost compilat local aici.
