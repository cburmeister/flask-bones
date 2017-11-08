.PHONY: init clean celery assets server db

init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

celery:
	python runcelery.py -A app.tasks worker -l INFO

assets:
	cd app/static && bower install && cd ..

db:
	flask recreate_db
