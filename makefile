fix:
	poetry run pre-commit run --all-files

test:
	poetry run python -m unittest

setup:
	poetry install
	poetry run pre-commit install

problem%:
	date
	poetry run python -m unittest tests/test_$@.py
	poetry run python -m advent_of_code_2020_py.$@
