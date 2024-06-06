.PHONY: full
full: clean test content gen-tf deploy clear-caches

.PHONY: gen-tf
gen-tf:
	python3 scripts/gen_tf.py

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
	python3 scripts/ssg.py

.PHONY: test
test:
	pytest

.PHONY: dev-content
dev-content: clean
	python3 scripts/ssg.py --dev

.PHONY: dev
dev: dev-content
	python3 scripts/dev_server.py

.PHONY: post
post:
	python3 scripts/new_post.py

.PHONY: output
output:
	terraform -chdir=terraform output