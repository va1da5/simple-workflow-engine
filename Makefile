.PHONY: dev, restart

help:
	@cat Makefile | grep -v .PHONY

.venv:
	@python3 -m venv .venv

.env:
	cp sample.env .env

install: .venv .env
	@. .venv/bin/activate; \
	@pip install -r local.txt

restart:
	docker-compose rm -fs -s api worker
	docker-compose up -d api worker

restart-db:
	docker-compose rm -fs database
	docker-compose up -d database

restart-worker:
	docker-compose rm -fs worker
	docker-compose up -d worker

migrations:
	@. .venv/bin/activate; \
	python manage.py makemigrations

migrate: .venv
	@. .venv/bin/activate; \
	python manage.py migrate

admin: .venv
	@. .venv/bin/activate; \
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')" | python manage.py shell; \
	echo Done!

run: .venv
	@. .venv/bin/activate; \
	python manage.py runserver 127.0.0.1:8000

celery-monitor: .venv
	@. .venv/bin/activate; \
	watch -n 1 "celery -A config inspect active"

flower: .venv
	@. .venv/bin/activate; \
	celery -A config flower
