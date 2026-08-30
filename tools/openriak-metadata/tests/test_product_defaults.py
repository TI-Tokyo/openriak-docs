import unittest
from types import SimpleNamespace

from openriak_metadata.cli import generate_defaults
from openriak_metadata.registry import PRODUCTS


class ProductDefaultsTests(unittest.TestCase):
    def test_cs_and_ts_are_cleanly_not_implemented(self):
        for product_name in ("cs", "ts"):
            args = SimpleNamespace(product=product_name, version="3.2.6")
            document = generate_defaults(args, PRODUCTS[product_name], [])
            self.assertEqual(document["status"], "not_implemented")
            self.assertEqual(document["settings"], {})
            self.assertEqual(document["effective_defaults"], {})
            self.assertIn(PRODUCTS[product_name]["display_name"], document["warnings"][0])


if __name__ == "__main__":
    unittest.main()
