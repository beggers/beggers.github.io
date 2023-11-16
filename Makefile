full: clean content gen-tf deploy clear-caches

gen-tf:
	python3 scripts/gen_tf.py

clear-caches:
	./scripts/invalidate_caches.sh

deploy: gen-tf
	terraform -chdir=terraform init && terraform -chdir=terraform apply

.PHONY: clean
clean:
	rm -rf public/*

.PHONY: content
content: clean
	python3 scripts/ssg.py

dev-content: clean
	python3 scripts/ssg.py --dev

dev: dev-content
	python3 scripts/dev_server.py

post:
	python3 scripts/new_post.py

.PHONY: output
output:
	terraform -chdir=terraform output