.PHONY: clean system-packages python-packages install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip install -r requirements.txt

install: system-packages python-packages

tests:
	python manage.py test

migrate:
	python manage.py db migrate --message 'Database migration'

upgrade:
	python manage.py db upgrade

run:
	python manage.py run

all: clean install tests run