
test:
	py.test --doctest-modules --ignore=alembic

migrate:
	PYTHONPATH=. alembic upgrade head

clean:
	-rm -f lambtastic.db
