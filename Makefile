.PHONY: build run test clean test-cov test-unit test-integration

# Build the Docker image
build:
	docker build -t python-docker-app .

# Run the Docker container
run:
	docker run -p 5000:5000 python-docker-app

# Run all tests
test:
	pytest

# Run tests with coverage
test-cov:
	pytest --cov=app --cov-report=html

# Run unit tests only
test-unit:
	pytest -m unit

# Run integration tests only
test-integration:
	pytest -m integration

# Clean up Docker containers and images
clean:
	docker stop $$(docker ps -a -q) 2>/dev/null || true
	docker rm $$(docker ps -a -q) 2>/dev/null || true
	docker rmi python-docker-app 2>/dev/null || true 