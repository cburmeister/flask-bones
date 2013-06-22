init:
	pip install -r requirements.txt
	cp config.example.py app/config.py

clean:
	find . -name '*.pyc' -delete
