.PHONY: full
full: clean test content gen-tf deploy clear-caches

.PHONY: gen-tf
gen-tf:
	python3 -m beneggerscom.gen_tf.main

.PHONY: clear-caches
clear-caches:
	./scripts/invalidate_caches.sh

.PHONY: deploy
deploy: gen-tf
	terraform -chdir=terraform init && terraform -chdir=terraform apply

.PHONY: clean
clean:
	rm -rf public/*

.PHONY: content
content: clean
	python3 -m beneggerscom.ssg.main

.PHONY: continuous-test
continuous-test:
	find . | grep -v public | grep -v -e "^\./\." | entr pytest

.PHONY: test
test:
	pytest

.PHONY: dev-content
dev-content: clean
	python3 -m beneggerscom.ssg.main --dev

.PHONY: server
server: dev-content
	python3 -m beneggerscom.dev_server.main

.PHONY: only-server
only-server:
	find . | grep -v public | grep -v -e "^\./\." | entr -rz python3 -m beneggerscom.dev_server.main

# Reloads everything on any file changes, including content.
.PHONY: dev
dev:
	find . | grep -v public | grep -v -e "^\./\." | entr -rz make server

.PHONY: post
post:
	python3 -m beneggerscom.new_post.main

.PHONY: output
output:
	terraform -chdir=terraform output