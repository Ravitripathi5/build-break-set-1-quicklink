# PR #142 - Analytics exporter for QuickLink

Author: j.doe - "Ready to merge, tested on my laptop!"

Adds a nightly job that exports click stats to a shared bucket so the marketing dashboard can read them.

Files:
- `exporter/settings.py` - configuration
- `exporter/export.py` - export job
- `exporter/Dockerfile` - container for the job
- `exporter/bucket.tf` - shared stats bucket
- `exporter/iam.tf` - permissions for the job
- `.github/workflows/export.yml` - CI for the exporter
