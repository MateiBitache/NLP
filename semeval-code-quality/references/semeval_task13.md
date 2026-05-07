# SemEval-2026 Task 13 Reference

Source: https://github.com/mbzuai-nlp/SemEval-2026-Task13

Local clone: `tools/SemEval-2026-Task13`

## Task Shape

- Task A: binary detection, human-written vs machine-generated code.
- Task B: multiclass authorship detection, human plus LLM families.
- Task C: hybrid detection, human-written, machine-generated, hybrid, adversarial.
- Main metric: Macro-F1 for all subtasks.
- Secondary metrics in `scorer.py`: accuracy, macro precision, macro recall.
- Dataset fields described by the README include code, label, language, generator, and task-specific mappings.
- Local trial parquet files currently have columns `code`, `generator`, `label`, `language`.
- Local trial parquet files do not expose `ID`; scripts that require `ID` need an added or preserved identifier column.

## Local Files Read

- `README.md`: task definitions, dataset format, restrictions, submission format, dates, citations.
- `format_checker.py`: CSV extension check, `ID` and `label` columns, task-specific `id_to_label.json`.
- `scorer.py`: merge gold/predictions on `ID`, compare gold `label` against prediction `prediction`, report Macro-F1, accuracy, macro precision, macro recall.
- `baselines/train.py`: CodeBERT training with `microsoft/codebert-base`, HuggingFace dataset subsets A/B/C, `code`/`label`, train/validation split, weighted F1 during training.
- `baselines/predict.py`: streaming parquet inference, required `ID` and `code`, output CSV `ID,prediction`.
- `task_A/id_to_label.json` and `label_to_id.json`.
- `task_B/id_to_label.json` and `label_to_id.json`.
- `task_C/id_to_label.json` and `label_to_id.json`.
- Trial parquet schemas:
  - Task A: 10,000 rows, `code`, `generator`, `label`, `language`.
  - Task B: 10,000 rows, `code`, `generator`, `label`, `language`.
  - Task C: 10,000 rows, `code`, `generator`, `label`, `language`.

## Format Notes

- README submission format says a CSV with `id` and `label`.
- `format_checker.py` checks for columns named `ID` and `label`.
- `scorer.py` merges gold and predictions on `ID`, reads gold from `label`, and reads predictions from `prediction`.
- Treat this mismatch as a project-contract risk. When building local tooling, support both common prediction-column conventions where possible and fail with a clear error.
- Treat missing `ID` in local trial parquet as another contract risk; generate IDs only for local experiments, never silently for official submission scoring.

## Label Mappings

Task A:

- `0`: human
- `1`: machine

Task B:

- `0`: human
- `1`: deepseek
- `2`: qwen
- `3`: 01-ai
- `4`: bigcode
- `5`: gemma
- `6`: phi
- `7`: meta-llama
- `8`: ibm-granite
- `9`: mistral
- `10`: openai

Task C:

- `0`: human
- `1`: machine
- `2`: hybrid
- `3`: adversarial

## Baseline Details

Training baseline:

- Uses `RobertaTokenizer` and `RobertaForSequenceClassification`.
- Defaults to `microsoft/codebert-base`.
- Loads `DaniilOr/SemEval-2026-Task13` by task subset.
- Requires `code` and `label`.
- Converts labels to integers.
- Uses max sequence length, batch size, learning rate, epoch count, and output directory as visible config.
- Reports accuracy, weighted precision, weighted recall, weighted F1.

Prediction baseline:

- Loads a trained model and tokenizer from `model_path`.
- Reads parquet input with streaming.
- Requires `ID` and `code`.
- Writes `ID,prediction`.
- Uses `cuda` when available unless device is provided.

## Code-Review Lessons

- Generalization matters: language, domain, and application scenario can change.
- Avoid edits that only target one detector surface.
- Evaluation files must keep IDs, labels, and prediction columns explicit.
- Refactors should not hide which labels, metrics, or artifacts are being produced.
- Detector-like feedback is useful only when it points to real maintainability problems.
- Prediction code should show batching, device, model path, input path, output path, and schema checks.
- Training code should show task subset, label count, data split, tokenizer/model setup, and metric choice.

## Safe Use

- Use SemEval scoring concepts to validate prediction files and metrics.
- Do not use SemEval as a recipe to disguise code origin.
- Do not introduce bad style to imitate human-written samples.
