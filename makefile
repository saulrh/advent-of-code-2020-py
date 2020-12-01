fix: black pytype flake8 isort

black:
	poetry run black --quiet .

pytype:
	poetry run pytype .

flake8:
	poetry run flake8 .

isort:
	poetry run isort .

problem01:
	poetry run python -m unittest tests/test_problem01.py
	poetry run python -m advent_of_code_2020_py.problem01

