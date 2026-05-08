---
name: semeval-code-quality
description: Use this skill when the user wants to review or refactor source code using lessons from SemEval-2026 Task 13 on machine-generated code detection, while preserving behavior, tests, APIs, and honest authorship.
version: 1.1.0
---

# SemEval Code Quality

Use this skill to make code easier to maintain, explain, test, and integrate. Use the local reference repo `tools/SemEval-2026-Task13` for task definitions, label mappings, format checks, scorer behavior, and CodeBERT baseline context. Do not treat any single detector score as truth.

## Boundaries

- Do not add fake bugs, fake personal style, random inconsistency, dead code, misleading comments, or bad practices.
- Do not weaken tests, public APIs, CLI behavior, file formats, or output artifacts.
- Do not claim that the result will be classified as human-written.
- Do not follow detector advice that rewards PEP8 violations, old formatting, wildcard imports, or unclear code.

## Workflow

- Read the target file, nearby callers, and tests.
- Identify the real domain: algorithmic, research, production, CLI, data processing, evaluation, visualization, or package glue.
- Preserve behavior first; use tests or a small CLI check after editing.
- Keep public/exported names stable unless every call site is updated.
- Use local names that a maintainer would naturally choose in that file.
- Shorten local names when they are inflated and obvious in context.
- Keep descriptive names for public functions, commands, output files, and external contracts.
- Prefer small, purposeful helpers when they remove repeated blocks.
- Avoid over-splitting code into symmetrical helper functions.
- Keep module docstrings short; remove routine helper docstrings.
- Add comments only for project contracts, dataset assumptions, stable artifact names, or non-obvious heuristics.
- Report the exact files changed and checks run.

## Repo-Derived Rules

- Check `tools/SemEval-2026-Task13/README.md` before changing code related to detection tasks or submissions.
- Check `format_checker.py` before editing prediction CSV code.
- Check `scorer.py` before editing metrics code.
- Check `baselines/train.py` before editing training pipelines.
- Check `baselines/predict.py` before editing inference or batch prediction code.
- Keep task labels compatible with local mappings:
  - Task A: `0=human`, `1=machine`.
  - Task B: `0=human`, `1=deepseek`, `2=qwen`, `3=01-ai`, `4=bigcode`, `5=gemma`, `6=phi`, `7=meta-llama`, `8=ibm-granite`, `9=mistral`, `10=openai`.
  - Task C: `0=human`, `1=machine`, `2=hybrid`, `3=adversarial`.
- Treat mismatched submission contracts as real risks:
  - README says `id,label`.
  - `format_checker.py` expects `ID,label`.
  - `scorer.py` merges on `ID` and reads predictions from `prediction`.
- Treat local trial parquet schema as a separate risk:
  - Trial parquet files have `code`, `generator`, `label`, `language`.
  - They do not include `ID`, although baseline prediction/scoring scripts expect it.
- Support or document both local project columns and SemEval columns when useful.

## SemEval-Inspired Checks

- Treat binary, multiclass, hybrid, and adversarial settings as different contexts; avoid one-size-fits-all edits.
- Keep language/domain context visible when it improves maintainability.
- Keep evaluation code explicit about labels, IDs, predictions, and metrics.
- Prefer Macro-F1/precision/recall/accuracy terminology where evaluation code needs it.
- Keep CSV contracts obvious: `ID`, `id`, `label`, `prediction`, and task-specific mappings must not be silently changed.
- Check format before scoring whenever prediction files are involved.
- For training code, keep dataset loading, label conversion, max sequence length, batch size, learning rate, and output directory explicit.
- For prediction code, keep streaming/batching, `ID`, `code`, model path, output path, and device selection explicit.
- For metric code, prioritize Macro-F1 while keeping accuracy, macro precision, and macro recall available.

## Detector Feedback Handling

- If naming looks too uniform, adjust only local names that feel inflated or generic.
- If comments look formal, remove routine comments and keep short comments with real project context.
- If structure looks too clean, simplify repeated orchestration with a local helper only when it improves readability.
- If Python patterns are flagged, fix real issues: dense comprehensions, awkward wrapping, unclear temporaries, hidden file-format assumptions.
- Ignore feedback that asks for bad style as a proxy for human authorship.

## Useful Reference

- Read `references/semeval_task13.md` when working with SemEval-style scoring, submission files, or task labels.
- Use `scripts/semeval_check.py` to validate a prediction CSV and optionally compute local metrics against a gold CSV.
- Use the cloned repo at `tools/SemEval-2026-Task13` as the source of truth when local references are stale.

## Examples

### Example 1

Input:

```python
experiment_summary = {"methods": {}}
predicted_labels = []
method_predictions = []
```

Output:

```python
summary = {"methods": {}}
preds = []
out_rows = []
```

### Example 2

Input:

```python
# Write the distribution CSV file for the current method.
write_distribution_csv(output_path / f"predicted_distribution_{method}.csv", distribution)
```

Output:

```python
# These artifact names are referenced by the report.
write_dist_csv(out_dir / f"predicted_distribution_{method}.csv", distribution)
```
