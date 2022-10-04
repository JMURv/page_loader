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
	poetry run pytest -cov

test-cov:
	poetry run pytest --cov=page_loader --cov-report xml

test-work:
	poetry run page-loader --output page_loader\tests\fixtures https://ru.hexlet.io/courses

test-work1:
	poetry run page-loader https://ru.hexlet.io/courses

#git_hub_make
a:
	git add .

p:
	git push