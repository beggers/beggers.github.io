deploy: tf clear-caches

gen-tf:
	python3 scripts/gen_tf.py

clear-caches:
	./scripts/invalidate_caches.sh

tf: gen-tf
	terraform -chdir=terraform apply
