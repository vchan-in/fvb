include .env

install:
	@echo "Building backend..."
	-@cp .env src/backend/.env
	-@copy .env src\backend\.env
	python -m venv .venv
	-@source .venv/bin/activate && pip install -r src/backend/requirements.txt
	-@.venv\Scripts\activate && pip install -r src/backend/requirements.txt
	@echo "Building client..."
	-@cp .env src/client/.env
	-@copy .env src\client\.env
	npm i && cd src/client && quasar build -m pwa
	@echo "Success! Run 'make backend' to start the backend server and 'make client' to start the client server."
	@echo "Run 'make client-android' to start the client server with android studios."
	@echo Finished Reading? CTRL+C to exit.

backend:
	@echo "Starting backend development server..."
	-@cp .env src/backend/.env
	-@copy .env src\backend\.env
	-@source .venv/bin/activate && cd src/backend && uvicorn main:app --host 0.0.0.0 --port ${VBANK_BACKEND_PORT} --reload
	-@.venv\Scripts\activate && cd src/backend && uvicorn main:app --host 0.0.0.0 --port ${VBANK_BACKEND_PORT} --reload
	
client:
	@echo "Starting client development server..."
	-@cp .env src/client/.env
	-@copy .env src\client\.env
	cd src/client && npm i -g @quasar/cli@latest && npm i && quasar dev -m spa -p 8080 VBANK_BACKEND_BASEURL=${VBANK_BACKEND_BASEURL} VBANK_BACKEND_PORT=${VBANK_BACKEND_PORT}

client-android:
	@echo "Starting client development server with android studios..."
	-@cp .env src/client/.env
	-@copy .env src\client\.env
	cd src/client && npm i -g @quasar/cli@latest && npm i && quasar dev -m capacitor -T android VBANK_BACKEND_BASEURL=${VBANK_BACKEND_BASEURL} VBANK_BACKEND_PORT=${VBANK_BACKEND_PORT}

docker:
	@echo "Starting docker containers with build..."
	docker-compose down
	docker compose build
	docker compose up -d

docker-dev:
	@echo "Starting docker dev containers with build..."
	docker-compose down
	docker compose build --no-cache
	docker compose up -d