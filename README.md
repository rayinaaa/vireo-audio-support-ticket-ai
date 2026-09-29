# Vireo Audio — Support Ticket Audit

## What this is
A small local Streamlit tool for the Vireo Audio support-ticket task.

It:
- filters the stated reporting window (Jan 2025–Jun 2026);
- trains a local TF-IDF + logistic-regression classifier on historical category tags;
- shows existing vs AI-assisted category volume;
- shows monthly category and first-assigned-team volume;
- flags low-confidence classifications;
- flags tickets where the inferred category implies a different owning team;
- lets an operator classify a new ticket.

## Run from a clean machine
Requires Python 3.10+.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The CSV/PDF inputs are in `data/`.

## Validation
Run:

```bash
python evaluate.py
```

This performs a stratified 80/20 holdout. The reported metric is agreement with the historical category tag, not ground-truth accuracy. On the supplied data it is 83.9% (2,329 test tickets).

## Important decisions
- Reporting window follows the brief: Jan 2025–Jun 2026.
- Tier 2 is not compared with Tier 1 on volume because the support policy explicitly says Tier 2 is measured differently.
- Low-confidence predictions (<60%) are review candidates.
- Routing mismatch is a signal for human review, not an automatic reassignment.

## Data note
The export contains legacy rows before Jan 2025 despite the stated task window. They are excluded from headline metrics.

Legacy resolution timestamps also need UTC/IST reconciliation described in the support policy before using them for handle-time analysis.

## No paid calls
The tool uses local scikit-learn inference. There are no paid API calls or API keys required.
