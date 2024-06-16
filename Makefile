# Prod stuff

.PHONY: full
full: clean test content gen-tf deploy clear-caches

.PHONY: clean
clean:
	rm -rf public/*

.PHONY: test
test:
	pytest

.PHONY: content
content: clean
	python3 -m beneggerscom.ssg.main

.PHONY: gen-tf
gen-tf:
	python3 -m beneggerscom.gen_tf.main

.PHONY: deploy
deploy: gen-tf
	terraform -chdir=terraform init && terraform -chdir=terraform apply

.PHONY: clear-caches
clear-caches:
	./scripts/invalidate_caches.sh

# Dev stuff

.PHONY: continuous-test
continuous-test:
	while true; do find . | grep -v public | grep -v -e "^\./\." | entr pytest; done

.PHONY: dev-clean
dev-clean:
	rm -rf public_dev/*

.PHONY: dev-content
dev-content: dev-clean
	python3 -m beneggerscom.ssg.main --dev

.PHONY: server
server: dev-content
	python3 -m beneggerscom.dev_server.main

.PHONY: only-server
only-server:
	while true; do find . | grep -v public | grep -v -e "^\./\." | entr -rz python3 -m beneggerscom.dev_server.main; done

# Reloads everything on any file changes, including content.
.PHONY: dev
dev:
	while true; do find . | grep -v public | grep -v -e "^\./\." | entr -rz make server; done

# Scripts and local stuff

.PHONY: post
post:
	python3 -m beneggerscom.new_post.main

.PHONY: output
output:
	terraform -chdir=terraform output