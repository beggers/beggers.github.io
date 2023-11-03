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
