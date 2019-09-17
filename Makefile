.PHONY: build version push namespace

version ?= latest
namespace ?= speedcheck
registry ?= k8s.azof.fr

build: db/Dockerfile tasks/Dockerfile
	docker-compose build

tag: build
ifneq ($(version), latest)
	git tag ${version}
endif
	docker tag azoff/speedcheck/db ${registry}/azoff/speedcheck/db:${version}
	docker tag azoff/speedcheck/tasks ${registry}/azoff/speedcheck/tasks:${version}
	docker tag azoff/speedcheck/server ${registry}/azoff/speedcheck/server:${version}

push: tag
	git push --tags
	docker push ${registry}/azoff/speedcheck/db:${version}
	docker push ${registry}/azoff/speedcheck/tasks:${version}
	docker push ${registry}/azoff/speedcheck/server:${version}

namespace:
	kubectl create namespace ${namespace}

secrets:
	kubectl --namespace=${namespace} apply -f secrets.yml

volumes:
	kubectl --namespace=${namespace} apply -f volumes.yml

dockerconfigjson:
	kubectl --namespace=${namespace} apply -f dockerconfigjson.yml

jobs:
	kubectl --namespace=${namespace} apply -f jobs.yml

cronjobs:
	kubectl --namespace=${namespace} apply -f cronjobs.yml

services:
	kubectl --namespace=${namespace} apply -f services.yml

deployments:
	kubectl --namespace=${namespace} apply -f deployments.yml