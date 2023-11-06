deploy: clean content gen-tf tf clear-caches

gen-tf:
	python3 scripts/gen_tf.py

clear-caches:
	./scripts/invalidate_caches.sh

tf: gen-tf
	terraform -chdir=terraform init && terraform -chdir=terraform apply

.PHONY: clean
clean:
	rm -rf public/*

.PHONY: content
content:
	python3 scripts/ssg.py

dev: content
	python3 scripts/server.py
