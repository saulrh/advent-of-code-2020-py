test:
	poetry run python -m unittest

problem%:
	date
	poetry run python -m unittest tests/test_$@.py
	poetry run python -m advent_of_code_2020_py.$@
