RUN = poetry run

.PHONY: fix test setup problem% ipython

fix:
	$(RUN) pre-commit run --all-files

test:
	$(RUN) python -m unittest

setup:
	pip3 install --user poetry
	poetry install
	$(RUN) pre-commit install
	$(RUN) ipython profile create --ProfileDir.location=./.ipython_profile

problem%:
	date
	$(RUN) python -m unittest tests/test_$@.py
	$(RUN) python -m advent_of_code_2020_py.$@

ipython:
	$(RUN) ipython --ProfileDir.location=./.ipython_profile
