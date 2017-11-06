.PHONY: init clean celery assets server db

init:
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' -delete

celery:
	python runcelery.py -A app.tasks worker -l INFO

assets:
	cd app/static && bower install && cd ..

server:
	python manage.py runserver --host 0.0.0.0

db:
	python manage.py recreate_db
