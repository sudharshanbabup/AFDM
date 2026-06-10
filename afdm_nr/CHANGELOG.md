# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-08
### Added
- Initial public release accompanying the IEEE Access paper.
- Core library `afdm_isac/` (waveforms, channel, sensing, links, resource).
- Per-figure scripts in `experiments/` reproducing Figs. 3–10 and Table 2.
- `run_all.py` to regenerate every result; fixed random seed for reproducibility.
- Packaging (`pyproject.toml`), CI workflow, and community-health files.
