init:
	pip install -r requirements.txt
	cp app/config.example.py app/config.py

clean:
	find . -name '*.pyc' -delete
