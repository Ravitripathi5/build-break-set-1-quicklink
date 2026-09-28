# Set 1 - QuickLink. Write your infrastructure here. You may split it into more .tf files.
# See BRIEF.md for the exact names that are verified.
#
# TODO ECR repository         ${local.prefix}-quicklink
# TODO DynamoDB table         ${local.prefix}-links
# TODO IAM role + policy      ${local.prefix}-quicklink-role (permissions_boundary!)
# TODO CloudWatch log group   /aws/lambda/${local.prefix}-quicklink
# TODO Lambda function        ${local.prefix}-quicklink (package_type = "Image")
# TODO Lambda function URL    authorization_type = "AWS_IAM"
