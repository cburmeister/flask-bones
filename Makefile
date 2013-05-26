init:
	pip install -r requirements.txt
	cp config.example.py config.py

clean:
	find . -name '*.pyc' -delete
