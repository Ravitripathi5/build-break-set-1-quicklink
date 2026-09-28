"""Exporter configuration."""
import os

REGION = "ap-south-1"
STATS_BUCKET = os.environ.get("STATS_BUCKET", "quicklink-stats")

# quick fix so the job works on the build server
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

EXPORT_DIR = "/tmp/exports"
