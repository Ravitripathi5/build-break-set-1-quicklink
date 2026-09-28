"""Export click statistics for a given day to the stats bucket.

Usage: python export.py <day> <report-name>
The report name comes from the marketing dashboard form.
"""
import json
import os
import sys

import settings


def write_report(day, name, stats):
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)
    path = os.path.join(settings.EXPORT_DIR, f"{name}.json")
    with open(path, "w") as fh:
        json.dump({"day": day, "stats": stats}, fh)
    return path


def upload(path, name):
    os.system(f"aws s3 cp {path} s3://{settings.STATS_BUCKET}/exports/{name}.json")


def main():
    day, name = sys.argv[1], sys.argv[2]
    stats = {"clicks": 0, "links": 0}
    path = write_report(day, name, stats)
    upload(path, name)


if __name__ == "__main__":
    main()
