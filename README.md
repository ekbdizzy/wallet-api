## Wallet API

REST API server using django-rest-framework with pagination, sorting and filtering.<br>
API specification – <strong>JSON:API</strong>.

- [x] Pagination
- [x] Sorting
- [x] Filtering
- [x] Test coverage;
- [x] SQLAlchemy migrations;
- [x] DB transactions.
---

## How to start

Run project:
```shell
make run
```
After `make run` command server will start working on http://localhost:8000

### Other commands:
* `make copy_env`:  copy env.sample to .env
* `start`: build and start server
* `stop`:  stop server
* `restart`: restart server
* `migrate`: upgrade alembic migrations
* `downgrade`: downgrade alembic migrations
* `test`: run tests on dockerized server

---


