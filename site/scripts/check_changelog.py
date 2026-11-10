#!/usr/bin/env python3
"""Validate generated release notes before Hugo renders them."""
import json
import pathlib
import re
import sys
from urllib.parse import urlparse


REPOSITORIES = {
    "xcp-hl", "xoa-hl", "xolite-ce", "xoa-proxy", "xcp-ng-ce-iso",
    "build-xoa-hl",
}


def validate(entries):
    if not isinstance(entries, list):
        raise ValueError("changelog must be a list")
    seen = set()
    for index, entry in enumerate(entries):
        at = f"entry {index + 1}"
        if not isinstance(entry, dict) or set(entry) != {
            "repository", "tag", "date", "channel", "components", "changes"
        }:
            raise ValueError(f"{at}: unexpected or missing fields")
        if entry["repository"] not in {"xcp-ng-ce-iso", "build-xoa-hl"}:
            raise ValueError(f"{at}: unknown release repository")
        if not isinstance(entry["tag"], str) or not re.fullmatch(r"[A-Za-z0-9._-]+", entry["tag"]):
            raise ValueError(f"{at}: invalid tag")
        identity = (entry["repository"], entry["tag"])
        if identity in seen:
            raise ValueError(f"{at}: duplicate release")
        seen.add(identity)
        if not isinstance(entry["date"], str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entry["date"]):
            raise ValueError(f"{at}: invalid date")
        if entry["channel"] not in {"stable", "candidate"}:
            raise ValueError(f"{at}: invalid channel")
        if not isinstance(entry["components"], list) or not entry["components"]:
            raise ValueError(f"{at}: components required")
        for component in entry["components"]:
            if not isinstance(component, dict) or set(component) != {"repository", "version"}:
                raise ValueError(f"{at}: invalid component")
            if component["repository"] not in REPOSITORIES or not isinstance(component["version"], str) or not component["version"]:
                raise ValueError(f"{at}: invalid component identity")
        if not isinstance(entry["changes"], list):
            raise ValueError(f"{at}: changes must be a list")
        for change in entry["changes"]:
            if not isinstance(change, dict) or set(change) != {"repository", "title", "url"}:
                raise ValueError(f"{at}: invalid change")
            if change["repository"] not in REPOSITORIES or not isinstance(change["title"], str) or not change["title"].strip():
                raise ValueError(f"{at}: invalid change title or repository")
            url = urlparse(change["url"] if isinstance(change["url"], str) else "")
            if url.scheme != "https" or url.netloc != "github.com" or not re.fullmatch(
                rf"/Vagrantin/{re.escape(change['repository'])}/pull/[1-9][0-9]*", url.path
            ) or url.query or url.fragment:
                raise ValueError(f"{at}: change URL must match its repository PR")


def main():
    path = pathlib.Path(sys.argv[1])
    try:
        validate(json.loads(path.read_text(encoding="utf-8")))
    except (ValueError, OSError) as error:
        sys.exit(f"{path}: {error}")
    print(f"Validated changelog data: {path}")


if __name__ == "__main__":
    main()
