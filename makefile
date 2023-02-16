install:
	pip install --upgrade pip
lint:
	pylint --disable=R,C design_toolkit.py
