resource "aws_s3_object" "favicon" {
  bucket       = module.index.bucket_id
  key          = "favicon.ico"
  source       = "../favicon.ico"
  etag         = filemd5("../favicon.ico")
  content_type = "image/x-icon"
}
