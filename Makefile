create_env:
	cp env.sample .env

start:
	docker compose up --build -d

stop:
	docker compose down -v

restart: stop start

migrate:
	docker compose exec web alembic upgrade head

downgrade:
	docker compose exec web alembic downgrade -2

test:
	docker compose exec web python manage.py test

run: create_env restart migrate