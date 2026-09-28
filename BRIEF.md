# Set 1 - QuickLink (URL shortener API)

**Scenario.** Marketing wants short links for campaigns. The developers finished the code in `app/`, and the unit tests pass. Nobody has shipped it yet. Your job is to package it as a container image, provision the infrastructure with Terraform, and deploy it to the AWS sandbox as a Lambda function behind an IAM-protected Function URL. A teammate also opened a pull request, `crack-files/`, that adds an analytics exporter. Review it before it merges.

Read `RULES.md` first. `<id>` below is your participant ID, for example `p07`.

---

## Part A - Build and deploy (50 points, verified live)

Everything below is checked automatically by name. Use the exact names.

| What | Exact name or setting |
|---|---|
| ECR repository | `hk-<id>-quicklink`, scan on push **on**, tag mutability **IMMUTABLE** |
| Image | `hk-<id>-quicklink:v1`, built from `app/`, with env `APP_VERSION=v1` baked in |
| DynamoDB table | `hk-<id>-links`, partition key `code` (String), on-demand billing |
| IAM role for Lambda | `hk-<id>-quicklink-role` with `permissions_boundary = var.permissions_boundary_arn`. Allow only what the function needs |
| Log group | `/aws/lambda/hk-<id>-quicklink` |
| Lambda function | `hk-<id>-quicklink`, `package_type = "Image"`, env `TABLE_NAME` = the table name |
| Function URL | on `hk-<id>-quicklink`, `authorization_type = "AWS_IAM"` |

**Tasks**
1. **A1 Package (8).** Write `Dockerfile` in the work folder root. Use the AWS Lambda Python 3.12 base image, copy `app/handler.py`, and set the handler command to `handler.lambda_handler`. Make `APP_VERSION=v1` part of the image. Unit tests must pass: `python3 -m unittest discover -s app`.
2. **A2 Registry (6).** Create the ECR repository with Terraform and push the image as tag `v1`.
3. **A3 Infrastructure as Code (8).** Write all resources in `infra/*.tf`. `providers.tf` and `variables.tf` are already provided. The code must pass `terraform fmt -check` and `terraform validate`. Do not hardcode the account ID or any credentials.
4. **A4 Working deployment (18).** These must work:
   - `GET /health` returns `{"status":"ok","service":"quicklink","version":"v1"}`
   - `POST /shorten` with body `{"url":"https://..."}` returns 201 and `{"code":"..."}`
   - `GET /<code>` returns 301 to the stored URL
   - An **unsigned** request to the Function URL is rejected with 403
5. **A5 Hardening (5).** Enable point-in-time recovery on the table. Set log retention to 14 days.
6. **A6 CI pipeline (5).** Write `.github/workflows/deploy.yml`, which is checked statically and not run. On push to `main` it should: run the unit tests, authenticate to AWS with **OIDC** (`role-to-assume`, `id-token: write`, no stored access keys), build the image and push it to ECR, and run `terraform fmt -check`, `validate`, and `plan`.

**Test it yourself**
```bash
aws lambda invoke --function-name hk-<id>-quicklink --cli-binary-format raw-in-base64-out \
  --payload '{"rawPath":"/health","requestContext":{"http":{"method":"GET"}}}' out.json && cat out.json
python3 tools/check_build.py --id <id>
```

**Known gotchas (not a trick)**
- Lambda needs the image to exist before the function can be created. Apply in two steps (`-target` the repository first), or push before the full apply.
- Build for the architecture you configure on the function, for example `--platform linux/arm64` with `architectures = ["arm64"]`. With BuildKit, add `--provenance=false`. Lambda rejects image indexes that carry attestations.
- IMMUTABLE tags mean you cannot push `v1` twice. If you need to rebuild, use `v1b` and set `image_tag`, but the verifier expects the image to report version `v1`.

---

## Part B - Break: review `crack-files/` (40 points)

`crack-files/` is a teammate's pull request, "analytics exporter". It has **at least 6** real security problems across secrets, public exposure, IAM, container hardening, the CI pipeline, and application code. For each one:
- fix it **in place**, keeping the file working and meaningful (deleting the file does not count), and
- record it in `FINDINGS.md`: where it is, the risk, and the fix.

You do not deploy these files.

## Part C - Operate (10 points)
Submit on time. Keep keys and state files out of the zip. Make sure every resource carries the default tags. Answer the three questions in `FINDINGS.md`.

## Submit
```bash
python3 tools/submit.py --id <id>      # creates set-1-<id>-submission.zip. Upload it where the organizer said.
```
Do **not** run `terraform destroy`.
