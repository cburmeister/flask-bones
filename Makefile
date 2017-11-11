.PHONY: init clean assets db

init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

assets:
	yarn install --modules-folder ./app/static/node_modules

db:
	flask recreate_db
