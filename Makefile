.PHONY: all


remove-env:
	find . -type d -name .venv@ptg | xargs rm -rf

env:
	python3 -m venv .venv@ptg

install:
	python3 -m pip install -r requirements.txt

setup: remove-env env install

build:
	echo "build docker"