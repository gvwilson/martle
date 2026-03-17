.PHONY: docs
all: commands

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## build: build package
build:
	@python -m build

## check: check Python code issues
check:
	@ruff check .

## clean: clean up
clean:
	@rm -rf ./dist ./src/faw/public
	@find . -path './.venv' -prune -o -type d -name '__pycache__' -exec rm -rf {} +
	@find . -path './.venv' -prune -o -type f -name '*~' -exec rm {} +

## docs: rebuild GitHub docs
docs:
	mkdir -p docs
	uv run marimo export html-wasm --force --mode edit demo.py -o docs/index.html --sandbox

## fix: fix formatting and code issues
fix:
	@ruff format .
	@ruff check --fix .

## publish: publish using ~/.pypirc credentials
publish:
	twine upload --verbose dist/*

## serve: run local docs server
serve:
	python -m http.server --directory docs
