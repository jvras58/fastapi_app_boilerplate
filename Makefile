SHEll := /bin/zsh
.PHONY: venv

venv:
	poetry run poetry install

start:
	poetry run python src/main.py

show_docs:
	poetry run mkdocs serve

init_repo:
	@git flow init -df
