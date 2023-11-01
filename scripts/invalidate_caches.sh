#!/bin/bash
cd terraform/ && terraform output | grep cloudfront_distribution_id | cut -d" " -f3 | xargs -I{} -n 1 aws cloudfront create-invalidation --distribution-id={} --paths "/"