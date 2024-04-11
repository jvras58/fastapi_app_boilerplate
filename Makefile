SHEll := /bin/zsh
.PHONY: venv

venv:
	poetry run poetry install

start:
	poetry run python src/main.py

show_docs:
	poetry run mkdocs serve

init_repo:
	@git flow init -d
	@git config --local git.flow.branch.master main
	@git config --local git.flow.branch.develop dev
	@git config --local git.flow.branch.feature feat/
	@git config --local git.flow.branch.release release/
	@git config --local git.flow.branch.hotfix hotfix/
	@git config --local git.flow.branch.support support/
	@git config --local git.flow.branch.versiontag v
	@git config --local git.flow.branch.bugfix bug/
