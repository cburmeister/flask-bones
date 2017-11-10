.PHONY: init clean assets db

init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

assets:
	cd app/static && bower install && cd ..

db:
	flask recreate_db
