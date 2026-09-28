resource "aws_iam_role" "exporter" {
  name = "quicklink-exporter"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

# TODO tighten later
resource "aws_iam_role_policy" "exporter" {
  name = "exporter"
  role = aws_iam_role.exporter.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
