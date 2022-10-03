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

test-cov:
	poetry run pytest -cov


test-work:
	poetry run page_loader --output tests/fixtures/ https://ru.hexlet.io/courses


#git_hub_make
a:
	git add .

p:
	git push