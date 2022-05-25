format-src:
	black src
	isort src
	flake8 src

format-tests:
	black test
	isort test
	flake8 test

format-all: format-src format-tests

# https://hub.docker.com/_/mongo

# https://www.bmc.com/blogs/mongodb-docker-container/
# docker compose for permanent volumes
run-db:
	docker run --name mongo-db-twitter --rm -it -p 27017:27017 -v twitter-clone-db:/db mongo