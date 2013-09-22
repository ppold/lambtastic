
test:
	py.test --doctest-modules --ignore=alembic

migrate:
	PYTHONPATH=. alembic upgrade head

clean:
	-rm lambtastic.db
