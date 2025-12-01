




alembic_first_setup:
	alembic init alembic

alembic_create_migration:
	alembic revision --autogenerate -m "Update"


update_database_models:
	python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
