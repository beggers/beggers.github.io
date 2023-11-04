When we remove a zone, we want to delete all the objects in it:
- S3 object
- S3 bucket
- Cloudfront distro
- DNS records
- SSL cert
- Etc

The SSL cert gives a difficulty: Terraform needs the provider config for the
SSL cert in order to destroy it, but if we remove the zone_deployment module
altogether we also remove the provider!

This module is the workaround: it provides Terraform with the provider and
nothing else so Terraform knows how to destroy the SSL cert.