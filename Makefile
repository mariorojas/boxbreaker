install:
	python manage.py migrate
	python manage.py createsuperuser --user admin --email admin@example.com

migrate:
	python manage.py migrate

run:
	python manage.py runserver