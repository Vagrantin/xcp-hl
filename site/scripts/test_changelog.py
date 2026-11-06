#!/usr/bin/env python3
"""Contract checks for release publisher data consumed by the docs site."""
import copy
import unittest

from check_changelog import validate


ENTRY = {
    "repository": "xcp-ng-ce-iso", "tag": "v8.3-ce47", "date": "2026-10-20",
    "channel": "stable",
    "components": [{"repository": "xolite-ce", "version": "v0.21.0-ce30"}],
    "changes": [{"repository": "xolite-ce", "title": "Improve deploy flow",
                 "url": "https://github.com/Vagrantin/xolite-ce/pull/42"}],
}


class ChangelogContractTest(unittest.TestCase):
    def test_valid_release(self):
        validate([copy.deepcopy(ENTRY)])

    def test_duplicate_release_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate release"):
            validate([copy.deepcopy(ENTRY), copy.deepcopy(ENTRY)])

    def test_wrong_repository_pr_is_rejected(self):
        entry = copy.deepcopy(ENTRY)
        entry["changes"][0]["url"] = "https://github.com/Vagrantin/xoa-hl/pull/42"
        with self.assertRaisesRegex(ValueError, "change URL"):
            validate([entry])

    def test_unexpected_schema_is_rejected(self):
        entry = copy.deepcopy(ENTRY)
        entry["changes"][0]["body"] = "unreviewed markup"
        with self.assertRaisesRegex(ValueError, "invalid change"):
            validate([entry])


if __name__ == "__main__":
    unittest.main()
