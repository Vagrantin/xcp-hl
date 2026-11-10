"""Guard against omitted or ambiguous screenshot-review inventory items."""
import pathlib
import tempfile
import unittest

from export_xoa_steps import inventory, numbered_items, digest


class NumberedItems(unittest.TestCase):
    def test_examples_comments_and_fences_do_not_become_steps(self):
        text = '''---
title: example
---
## Setup
1. Real item.
```sh
2. Not an item.
````
~~~text
3. Still an example.
~~~
<!--
4. Hidden example.
-->
2. Next real item.
'''
        items = numbered_items(text)
        self.assertEqual([item['cue'] for item in items], ['Real item.', 'Next real item.'])
        self.assertEqual([item['sourceLine'] for item in items], [5, 15])

    def test_html_comment_example_inside_code_does_not_hide_real_steps(self):
        items = numbered_items('```html\n<!-- an example\n```\n1. Real step.\n')
        self.assertEqual([item['cue'] for item in items], ['Real step.'])

    def test_restarted_lists_duplicate_headings_and_nested_items_are_unique(self):
        items = numbered_items('## Repeat\n1. First.\n\n## Repeat\n1. Again.\n   1) Nested.\n')
        self.assertEqual([item['ordinal'] for item in items], [1, 2, 3])
        self.assertEqual([item['indent'] for item in items], [0, 0, 3])
        self.assertEqual(items[0]['headingPath'], ['Repeat'])

    def test_unclosed_blocks_fail_instead_of_omitting_the_rest_of_a_page(self):
        for text in ('```sh\n1. example', '<!--\n1. hidden'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                numbered_items(text)

    def test_page_hash_covers_continuations_and_unnumbered_instructions(self):
        self.assertNotEqual(digest('1. Item.\n   Continuation.'),
                            digest('1. Item.\n   Changed prerequisite.'))
        self.assertEqual(digest('1. Item.  \n'), digest('1. Item.'))

    def test_inventory_includes_pages_without_steps_and_keeps_review_pending(self):
        with tempfile.TemporaryDirectory() as temp:
            site = pathlib.Path(temp) / 'site'
            root = site / 'content/en/docs/xoa-hl'
            root.mkdir(parents=True)
            for name, body in [('task', '1. Read it.\n1. Read again.'), ('concept', 'An explanation.')]:
                (root / f'{name}.md').write_text(
                    f'---\ntitle: {name}\ntranslationKey: xoa-{name}\n---\n{body}\n')
            report = inventory(site, 'a' * 40)
            self.assertEqual((report['pageCount'], report['pagesWithNumberedItems'], report['itemCount']),
                             (2, 1, 2))
            items = report['pages'][1]['items']
            self.assertEqual(len({item['id'] for item in items}), 2)
            self.assertTrue(all(item['disposition'] == 'pending-editorial-review' for item in items))


if __name__ == '__main__':
    unittest.main()
