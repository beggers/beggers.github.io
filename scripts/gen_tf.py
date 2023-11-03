"""
This script generates the requisite terrafrom to deploy the site.
"""


import os


GENERATED_FILE_COMMENT = """# This file is generated by the gen_tf.py script.
# Do not edit this file directly.
"""

SUBDOMAIN_MODULE_BLOCK = """
module "{subdomain}" {{
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = {domain_aliases}
  file           = "{file_name}"
  file_directory = "../pages/"
  fqdn           = "{fqdn}"
  zone_id        = aws_route53_zone.main.zone_id
}}
"""

# TODO we could generate this directly from the output file in zone_deployment/
SUBDOMAIN_OUTPUT_BLOCK = """
output "{subdomain}_cloudfront_distribution_id" {{
  value = module.{subdomain}.cloudfront_distribution_id
}}

output "{subdomain}_hosted_zone_id" {{
  value = module.{subdomain}.hosted_zone_id
}}

output "{subdomain}_bucket_id" {{
  value = module.{subdomain}.bucket_id
}}

output "{subdomain}_bucket_regional_domain_name" {{
  value = module.{subdomain}.bucket_regional_domain_name
}}

output "{subdomain}_cert_arn" {{
  value = module.{subdomain}.cert_arn
}}

output "{subdomain}_cert_validation_record" {{
  value = module.{subdomain}.cert_validation_record
}}

"""

DOMAIN_FILE = "main.tf"
OUTPUT_FILE = "outputs_autogen.tf"

PAGES_DIRETORY = "pages"
TERRAFORM_DIRETORY = "terraform"


def main():
    filenames = get_filenames()
    if not filenames:
        print("No files found in the pages directory.")
        return
    generate_domain_file(filenames)
    generate_output_file(filenames)


def get_filenames():
    return [
        f
        for f in os.listdir(PAGES_DIRETORY)
        if not os.path.isdir(os.path.join(PAGES_DIRETORY, f))
    ]


def generate_domain_file(filenames):
    blocks = []
    for filename in filenames:
        subdomain = filename.split(".")[0]
        # Cool and normal best practices.
        domain_aliases = domain_aliases_as_string(
            ["www.${var.domainName}"] if subdomain == "index" else []
        )
        block = generate_subdomain_module_block(subdomain, domain_aliases, filename)
        blocks.append(block)

    write_blocks_to_file(blocks, os.path.join(TERRAFORM_DIRETORY, DOMAIN_FILE))


def generate_subdomain_module_block(subdomain, domain_aliases, file_name):
    return SUBDOMAIN_MODULE_BLOCK.format(
        subdomain=subdomain,
        domain_aliases=domain_aliases,
        file_name=file_name,
        fqdn=fqdn(subdomain),
    )


def domain_aliases_as_string(aliases):
    # f-strings insert lists of strings as single-quoted by default, but we
    # need them to be double-quoted. I googled for five minutes but decided it
    # would be more fun to write this function.
    #
    # This is pretty dumb so we're overwhelmingly likely to only ever use it
    # for index and www.
    return "[" + ", ".join([f'"{alias}"' for alias in aliases]) + "]"


def fqdn(subdomain):
    if subdomain == "index":
        return "${var.domainName}"
    return f"{subdomain}.${{var.domainName}}"


def generate_output_file(filenames):
    blocks = []
    for filename in filenames:
        subdomain = filename.split(".")[0]
        block = generate_subdomain_output_block(subdomain)
        blocks.append(block)

    write_blocks_to_file(blocks, os.path.join(TERRAFORM_DIRETORY, OUTPUT_FILE))


def generate_subdomain_output_block(subdomain):
    return SUBDOMAIN_OUTPUT_BLOCK.format(
        subdomain=subdomain,
    )


def write_blocks_to_file(blocks, filepath):
    with open(filepath, "w") as f:
        f.write(GENERATED_FILE_COMMENT)
        f.writelines(blocks)


if __name__ == "__main__":
    main()
