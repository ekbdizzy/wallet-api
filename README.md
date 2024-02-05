## Wallet API

REST API server using django-rest-framework with pagination, sorting and filtering.<br>
API specification – <strong>JSON:API</strong>.

- [x] Pagination
- [x] Sorting
- [x] Filtering
- [x] Test coverage
- [x] SQLAlchemy migrations
- [x] DB transactions
---

## How to start

Run project:
```shell
make run
```
After `make run` command server will start working on http://localhost:8000

### Other make commands:
* `make copy_env`:  copy env.sample to .env
* `make start`: build and start server
* `make stop`:  stop server
* `make restart`: restart server
* `make migrate`: upgrade alembic migrations
* `make downgrade`: downgrade alembic migrations
* `make test`: run tests on dockerized server

---


