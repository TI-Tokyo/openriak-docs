import tempfile
import unittest
from pathlib import Path

from import_hugo_018 import ImportError018, import_tree


def page(title, menu_name, identifier, weight, parent=None):
    parent_line = f'    parent: "{parent}"\n' if parent else ""
    return (
        "---\n"
        f'title: "{title}"\n'
        "menu:\n"
        "  old-product-1.0.0:\n"
        f'    name: "{menu_name}"\n'
        f'    identifier: "{identifier}"\n'
        f"    weight: {weight}\n"
        f"{parent_line}"
        "---\n\nBody.\n"
    )


class ImportHugo018Tests(unittest.TestCase):
    def make_source(self, root):
        source = root / "legacy"
        (source / "guide").mkdir(parents=True)
        (source / "index.md").write_text(page("Home", "Legacy docs", "index", 10), encoding="utf-8")
        (source / "_index.md").write_text("---\ntitle: Search index\n---\n", encoding="utf-8")
        (source / "guide.md").write_text(page("Guide", "The guide", "guide", 20), encoding="utf-8")
        (source / "guide" / "topic.md").write_text(
            page("Topic", "First topic", "topic", 30, "guide"), encoding="utf-8"
        )
        (source / "diagram.png").write_bytes(b"png")
        (source / "_reference-links.md").write_text("[home]: /\n", encoding="utf-8")
        return source

    def test_copy_import_converts_sections_and_front_matter(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = self.make_source(root)
            destination = root / "modern"
            counts = import_tree(source, destination)
            self.assertEqual(counts["branch_bundles"], 2)
            self.assertEqual(counts["discarded_search_indexes"], 1)
            self.assertFalse((destination / "index.md").exists())
            self.assertFalse((destination / "guide.md").exists())
            self.assertTrue((destination / "diagram.png").exists())
            fragment = (destination / "_reference-links.md").read_text(encoding="utf-8")
            self.assertIn("list: never", fragment)
            self.assertIn("render: never", fragment)
            self.assertTrue(fragment.endswith("[home]: /\n"))
            home = (destination / "_index.md").read_text(encoding="utf-8")
            guide = (destination / "guide" / "_index.md").read_text(encoding="utf-8")
            self.assertIn('title: "Home"', home)
            self.assertNotIn("Search index", home)
            self.assertIn('linkTitle: "The guide"', guide)
            self.assertIn("weight: 20", guide)

    def test_in_place_import_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = self.make_source(Path(temporary))
            import_tree(source, source)
            first = (source / "guide" / "_index.md").read_text(encoding="utf-8")
            import_tree(source, source)
            second = (source / "guide" / "_index.md").read_text(encoding="utf-8")
            self.assertEqual(first, second)
            self.assertEqual(second.count("linkTitle:"), 1)
            self.assertEqual(second.count("weight: 20"), 2)  # menu and top-level weight

    def test_missing_menu_parent_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "legacy"
            source.mkdir()
            (source / "page.md").write_text(
                page("Page", "Page", "page", 10, "missing"), encoding="utf-8"
            )
            with self.assertRaises(ImportError018):
                import_tree(source, source, check=True)


if __name__ == "__main__":
    unittest.main()
