include .env

build-source:
	@echo "Building backend..."
	python -m venv .venv
	-@source .venv/bin/activate && pip install -r requirements.txt
	-@.venv\Scripts\activate && pip install -r requirements.txt
	@echo "Building client..."
	-@cp .env src\client\.env
	-@copy .env src\client\.env
	npm i && cd src/client && quasar build -m pwa
	@echo "Success! Run 'make dev-backend' to start the backend server and 'make dev-client' to start the client server."
	@echo "Run 'make dev-client-android' to start the client server with android studios."
	@echo Finished Reading? CTRL+C to exit.

build-docker:
	@echo "Building backend..."
	cd src/backend && docker build -t src/backend .
	docker tag src/backend:latest src/backend:$(shell date +%s)
	@echo "Building client..."
	-@cp .env src\client\.env
	-@copy .env src\client\.env
	cd src/client && docker build -t src/client .
	docker tag src/client:latest src/client:$(shell date +%s)
	@echo "Success!"
	@echo "Run 'make build-docker-up' to start the docker containers."
	@echo Finished Reading? CTRL+C to exit.

build-docker-up:
	@echo "Starting docker containers with build..."
	docker-compose build --no-cache
	docker-compose up -d

dev-backend:
	@echo "Starting backend development server..."
	-@source .venv/bin/activate && cd src/backend && uvicorn main:app --host 0.0.0.0 --port ${VBANK_BACKEND_PORT} --reload
	-@.venv\Scripts\activate && cd src/backend && uvicorn main:app --host 0.0.0.0 --port ${VBANK_BACKEND_PORT} --reload
	
dev-client:
	@echo "Starting client development server..."
	-@cp .env src\client\.env
	-@copy .env src\client\.env
	npm i && cd src/client && quasar dev -m pwa -p 9000

dev-client-android:
	@echo "Starting client development server with android studios..."
	-@cp .env src\client\.env
	-@copy .env src\client\.env
	npm i && cd src/client && quasar dev -m capacitor -T android