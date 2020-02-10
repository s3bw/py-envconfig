clean:
	rm -rf dist/
	rm -rf build/

publish: clean
	python setup.py sdist bdist_wheel
	python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

test:
	pytest tests/
