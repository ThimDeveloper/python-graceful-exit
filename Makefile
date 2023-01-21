.PHONY: all


clean: 
	find . -type d -name ".mypy_cache" | xargs rm -rf
	find . -type d -name ".pytest_cache" | xargs rm -rf
	find . -type d -name "__pycache__" | xargs rm -rf
	find `pwd`/src -type d -name "*.egg-info" | xargs rm -rf

remove-env:
	find . -type d -name .venv@ptg | xargs rm -rf

env:
	python3 -m venv .venv@ptg

install:
	python3 -m pip install -r requirements.txt

setup: clean remove-env env install

build:
	docker image build -t python_termination_guard:latest .

run: build
	docker-compose up
	
format:
	pautoflake `pwd`/src 
	black `pwd`/src

lint:
	pflake8 `pwd`/src

types:
	mypy `pwd`/src

test:
	pytest -s -vv

ci: format lint types test

package:
	find . -type d -name "dist" | xargs rm -rf
	python3 -m build

publish: package
	python3 -m  twine upload dist/*