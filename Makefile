.PHONY: test

test:
	pipenv run pytest --flake8 --cov pygetty --cov-report term-missing --cov-report xml
