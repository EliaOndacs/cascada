
WEB_CONCURRENCY=5

install-deps:
	pip install -r requirements.txt

run-dev: install-deps
	uvicorn main:server --reload

run-prod: install-deps
	uvicorn main:server --host 0.0.0.0 --port 80 --workers $(WEB_CONCURRENCY)
