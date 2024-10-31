ifeq (,$(wildcard .env))
	@echo ".env file not found. Copying env.template to .env..."
	@cp env.template .env
	-@copy env.template .env
endif

include .env

install: # Only works on Debian based systems
	@echo "Building backend..."
	-@apt-get install -y python-is-python3
	-@cp .env src/backend/.env
	cd src/backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
	@echo "Building client..."
	-@cp .env src/client/.env
	cd src/client && npm i -g @quasar/cli@latest && npm i && quasar build -m pwa
	@echo "Success! Run 'make backend' to start the backend server and 'make client' to start the client server."
	@echo "Run 'make client-android' to start the client server with android studios."
	@echo Finished Reading? CTRL+C to exit.

backend: # Only works on Debian based systems
	@echo "Starting backend development server..."
	-@cp .env src/backend/.env
	-@cd src/backend && . .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port ${FVB_BACKEND_PORT} --reload
	
client: # Only works on Debian based systems
	@echo "Starting client development server..."
	-@cp .env src/client/.env
	cd src/client && npm i -g @quasar/cli@latest && npm i && quasar dev -m spa -p 8080


client-android: # Only works on Debian based systems
	@echo "Starting client development server with android studios..."
	-@cp .env src/client/.env
	cd src/client && npm i -g @quasar/cli@latest && npm i && quasar dev -m capacitor -T android --env.FVB_BACKEND_BASEURL ${FVB_BACKEND_BASEURL} --env.FVB_BACKEND_PORT ${FVB_BACKEND_PORT}

docker:
	@echo "Starting docker containers with build..."
	-@docker-compose down
	-@docker compose build
	docker compose up -d

docker-dev:
	@echo "Starting docker dev containers with build..."
	-@docker-compose down
	-@docker compose build --no-cache
	docker compose up -d

docker-dev-db:
	@echo "Starting docker dev containers with build..."
	-@docker-compose stop db phpmyadmin
	-@docker-compose rm db phpmyadmin -f
	docker compose up -d db phpmyadmin

docker-dev-client:
	@echo "Starting docker dev containers with build..."
	-@docker compose stop client
	-@docker compose rm client -f
	-@docker compose build client --no-cache
	docker compose up -d client

docker-dev-backend:
	@echo "Starting docker dev containers with build..."
	-@docker-compose stop backend
	-@docker-compose rm backend -f
	-@docker compose build backend --no-cache
	docker compose up -d backend