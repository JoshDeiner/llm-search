# Variables
IMAGE_NAME = my-python-app
CONTAINER_NAME = my-python-app-container
TAG = latest
NETWORK= search_network


build:
	docker build -t $(IMAGE_NAME):$(TAG) .

restart:
	docker restart searxng-instance

local:
	python src/lang_search.py
test:
	pytest tests/
run:
	docker run -d --network $(NETWORK) -v /home/josh/workspace/my-instance/logs:/app/logs --name $(CONTAINER_NAME) $(IMAGE_NAME):$(TAG)
# 	docker run -d --network $(NETWORK) -v $(pwd)/logs:/app/logs --name $(CONTAINER_NAME) $(IMAGE_NAME):$(TAG)


network:
	docker network ls | grep -q $(NETWORK) || docker network create $(NETWORK)


# Stop the container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Tag the image
tag:
	docker tag $(IMAGE_NAME):$(TAG) $(IMAGE_NAME):$(TAG)

# Clean up dangling images and stopped containers
clean:
	docker rm -f $(CONTAINER_NAME) || true
	docker rmi -f $(IMAGE_NAME):$(TAG) || true
	docker image prune -f
	docker container prune -f

# Push the image to a repository (e.g., Docker Hub or private registry)
# Set REGISTRY to your Docker repository (e.g., "username/repo")
push:
	docker tag $(IMAGE_NAME):$(TAG) $(REGISTRY)/$(IMAGE_NAME):$(TAG)
	docker push $(REGISTRY)/$(IMAGE_NAME):$(TAG)

# View logs of the container
logs:
	docker logs -f $(CONTAINER_NAME)

# Run an interactive shell in the container
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash


# Define Docker Compose specific targets

dc-run:
	docker compose up --build -d

dc-stop:
	docker compose down --volumes

dc-restart:
	docker compose down && docker compose up --build -d

dc-logs:
	docker compose logs -f 
