clean:
	rm -rf dist/
	rm -rf build/

publish: clean
	python setup.py sdist bdist_wheel
	python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

tag: publish
	python scripts/wheel_version.py | xargs git tag
	python scripts/wheel_version.py | xargs -I '{}' git push '{}' origin

test:
	pytest tests/
