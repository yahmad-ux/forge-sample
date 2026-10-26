# forge-sample

Small text helpers in Python. This repo is a test bed for an automated coding
loop that turns labelled issues into pull requests.

## Set up

    python3 -m venv .venv
    .venv/bin/pip install -r requirements-dev.txt

## Check

    .venv/bin/ruff format --check .
    .venv/bin/ruff check .
    .venv/bin/mypy
    .venv/bin/python -m unittest discover -s tests -v
