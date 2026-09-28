resource "aws_s3_bucket" "stats" {
  bucket = "quicklink-stats"
}

# Dashboard reads the files directly from the browser, so make them readable.
resource "aws_s3_bucket_public_access_block" "stats" {
  bucket                  = aws_s3_bucket.stats.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "stats" {
  bucket = aws_s3_bucket.stats.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid       = "DashboardRead"
      Effect    = "Allow"
      Principal = "*"
      Action    = "s3:GetObject"
      Resource  = "${aws_s3_bucket.stats.arn}/*"
    }]
  })
}
