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

test_all:
	@poetry run task test_all

commit:
	@echo "Changes to be committed:"
	@echo "========================="
	@git status -s 
	@echo "========================="
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} == y ]
	@git add . && poetry run cz commit
	