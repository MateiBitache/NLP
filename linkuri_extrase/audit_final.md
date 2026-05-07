# Final audit

Generated on 2026-05-07.

## Direct links from `pagina.html`

- `href` attributes found in `pagina.html`: 107
- Internal anchors: 1 (`#terms`)
- Unique external/direct URLs: 85
- Successful direct downloads: 79
- Successful GitHub clone + page download: 2
- Failed direct URLs: 4 old ACL Anthology links
- Recovered ACL fallback downloads: 5
- ACL BibTeX recovered from HTML: 1

Conclusion: all direct, non-anchor links from `pagina.html` were either downloaded/cloned or explicitly accounted for with modern fallback files.

## File processing

- Raw downloaded files: 86
- Empty raw files: 0
- Missing successful outputs: 0
- ZIP archives: 11
- ZIP archives successfully extracted: 11
- Files inside extracted archives: 96
- PDF/HTML/TXT/BibTeX text extraction/copy operations: 75
- ZIP files skipped by text extraction: 11, because they were handled through archive extraction
- Files inventoried inside cloned GitHub repositories: 1398

## Secondary links found inside downloaded HTML pages

This is the important caveat.

- Unique secondary links found inside downloaded HTML pages: 1350
- Likely downloadable secondary resources not present as direct links in `pagina.html`: 540
- They are indexed in `secondary_links.csv` and `secondary_resource_links_not_downloaded.csv`.

These secondary resources were not all downloaded, because that would be a second-level crawl of linked websites. It includes broad pages such as Saif Mohammad's homepage/publication lists and can quickly expand beyond the resources explicitly referenced by `pagina.html`.

## What remains manual or optional

- Review `secondary_resource_links_not_downloaded.csv` if you want a second-level crawl.
- The Yelp Academic Dataset page may require manual registration/license steps for the original Yelp dataset.
- Use original PDFs for slides/posters where extracted text loses visual layout.
