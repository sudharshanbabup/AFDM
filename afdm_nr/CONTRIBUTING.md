# Contributing

Thanks for your interest in improving this reproducibility package!

## Reporting issues
- Use the GitHub issue templates (bug report / feature request).
- For numerical discrepancies, please state your OS, Python version, NumPy/SciPy
  versions, the exact command run, and the figure/table affected.

## Development setup
```bash
git clone https://github.com/<author-repository>.git
cd <author-repository>
python -m venv venv && source venv/bin/activate
pip install -e .
python run_all.py
```

## Guidelines
- Keep all simulation constants in `afdm_isac/params.py` (single source of truth).
- Follow [PEP 8](https://peps.python.org/pep-0008/); keep functions documented.
- Each figure script must remain runnable both standalone
  (`python experiments/figX.py`) and via `run_all.py`, and must write its output
  to `results/`.
- If you change a model or constant, note it in `CHANGELOG.md` and explain the
  rationale in the pull request.

## Pull requests
- Keep PRs focused and small where possible.
- Ensure `python run_all.py` completes without errors before submitting.
