# Contributing to FairProp

Thank you for your interest in contributing to FairProp! We aim to build the open standard for Fair Housing compliance in software.

## Development Setup

1.  **Clone the repository**
2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # text/bash
    ```
3.  **Install dependencies**:
    ```bash
    pip install -e .
    ```

## Project Structure

*   `fairprop/`: The core Python package.
    *   `auditor.py`: Main business logic and auditing engine.
    *   `models.py`: AI model management (Neuro-Symbolic core).
    *   `cli.py`: Command-line interface implementation.
*   `fha_rules.json`: The source of truth for HUD-based keyword rules.

## Testing

We use `pytest`. Please ensure all tests pass before submitting a PR.
```bash
make test
```

## Code Style

*   We use strict type hinting.
*   Please format your code using `black`.

## Adding New Rules

To add a new compliance rule, simply edit `fha_rules.json`. No code changes required!
