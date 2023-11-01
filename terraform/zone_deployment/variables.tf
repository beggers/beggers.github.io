variable "cert_arn" {
  default = "ERROR - NO CERT ARN SET"
  type    = string
}

variable "cloudfront_access_identity_arn" {
  default = "ERROR - NO CLOUDFRONT ACCESS IDENTITY ARN SET"
  type    = string
}

variable "cloudfront_access_identity_path" {
  default = "ERROR - NO CLOUDFRONT ACCESS IDENTITY PATH SET"
  type    = string
}

variable "content_type" {
  default = "ERROR - NO CONTENT TYPE SET"
  type    = string
}

variable "domain_aliases" {
  default = []
  type    = list(string)
}

variable "file" {
  default = "ERROR - NO FILE SET"
  type    = string
}

variable "file_directory" {
  default = "ERROR - NO FILE DIRECTORY SET"
  type    = string
}

variable "fqdn" {
  default = "ERROR - NO DOMAIN SET"
  type    = string
}

variable "zone_id" {
  default = "ERROR - NO ZONE ID SET"
  type    = string
}
