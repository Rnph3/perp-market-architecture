# Tutorial — produce the comparative research package

1. Open a terminal in the repository root; check Python 3.10+ with `python3 --version`.
2. Run `python3 -m unittest discover -s tests -v`.
3. Run `python3 src/build_report.py`.
4. Inspect `artifacts/design_matrix.csv` and `artifacts/research_report.md`.
5. Open `artifacts/comparison.svg` in a browser.

**Expected outcome:** 4 documented venue designs and an evidence-source link per claim. No external data access is required.
