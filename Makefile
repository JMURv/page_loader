install:
	poetry install

build:
	poetry build

package-install:
	pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest

test-vv:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov-report term-missing --cov=page_loader

test-cov:
	poetry run pytest --cov=page_loader --cov-report xml

add:
	git add .

p:
	git push