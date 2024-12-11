dev:
	python src/main.py


migrations_init:
	alembic init src/migrations

migrations_make:
	alembic revision --autogenerate -m "$(message)"

migrations_migrate:
	alembic upgrade head

migrations_downgrade:
	alembic downgrade $(rev)

start_celery:
	celery --app=src.tasks.celery_app:celery_instance worker -l INFO
