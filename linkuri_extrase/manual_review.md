# Manual review

Generated on 2026-05-07 after automated download, archive extraction, GitHub cloning, and text extraction.

## Needs manual attention

- The old ACL Anthology URLs from `aclweb.org` failed because the old host/paths no longer serve them reliably:
  - `https://www.aclweb.org/anthology/W11-0611`
  - `http://aclweb.org/anthology-new/W/W11/W11-0611.bib`
  - `https://www.aclweb.org/anthology/P11-2064/`
  - `http://aclweb.org/anthology-new/P/P11/P11-2064.bib`
- These ACL items were recovered through modern `aclanthology.org` equivalents:
  - `raw/086_aclanthology.org_W11-0611.html`
  - `raw/088_aclanthology.org_W11-0611.pdf`
  - `text/086_aclanthology.org_W11-0611.extracted.bib`
  - `raw/089_aclanthology.org_P11-2064.html`
  - `raw/090_aclanthology.org_P11-2064.bib`
  - `raw/091_aclanthology.org_P11-2064.pdf`
- `https://www.yelp.ca/academic_dataset` was downloaded as the public web page, but the actual Yelp Academic Dataset may require manual registration/license steps if you need the original Yelp data, not just the NRC/Yelp lexicon ZIP linked in `pagina.html`.
- PDF text was extracted automatically, but posters/slides/table-heavy PDFs can lose layout in text form. Use the original PDFs in `raw/` for exact visual/manual review.
- GitHub repositories were cloned successfully. If Git later complains about `dubious ownership` from a sandbox user, mark the repo as safe or open it from the normal Windows user.

## No separate manual step needed

- Internal anchors such as `#terms` are already inside `pagina.html`.
- ZIP files that downloaded successfully were expanded into `archives/`.
- HTML pages were converted to text in `text/html/`.
- PDF files were converted to text in `text/pdf/`.
- BibTeX/TXT files were copied into `text/`.

## Important usage note

Some lexicons state redistribution restrictions. Keep the downloaded data for local/project use unless the source license explicitly allows redistribution.
