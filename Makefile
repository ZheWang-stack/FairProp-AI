.PHONY: install test lint format clean

install:
	pip install -e .

test:
	pytest tests/

lint:
	pylint fairprop/

format:
	black fairprop/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -name "*.pyc" -delete
