dev-backend:
	@echo "Starting backend development server..."
	cd src/backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload

dev-client:
	@echo "Starting client development server..."
	cd src/client && npm i && quasar dev -m pwa -p 9000

dev-client-android:
	@echo "Starting client development server with android studios..."
	cd src/client && npm i && quasar dev -m capacitor -T android

build:
	@echo "Building client..."
	cd src/client && docker build -t src/client .
	docker tag src/client:latest src/client:$(shell date +%s)

	@echo "Building backend..."
	cd src/backend && docker build -t src/backend .
	docker tag src/backend:latest src/backend:$(shell date +%s)

docker-up-build:
	@echo "Starting docker containers with build..."
	docker-compose build --no-cache
	docker-compose up -d

docker-up:
	@echo "Starting docker containers..."
	docker-compose up -d
