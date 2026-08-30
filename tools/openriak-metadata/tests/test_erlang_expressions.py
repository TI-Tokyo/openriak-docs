import unittest

from openriak_metadata.schema import parse_schema


class ErlangExpressionTests(unittest.TestCase):
    def test_dynamic_messages_and_adjacent_strings_are_preserved(self):
        text = '''
{validator, dynamic, ("minimum " ++ integer_to_list(system:value())), fun(X) -> X > 0 end}.
{validator, adjacent, "first " "second", fun(X) -> X end}.
{validator, block, begin X = system:value(), "message" end, fun(X) -> X end}.
'''
        parsed = parse_schema(text, "repo", "priv/example.schema")
        self.assertEqual(parsed.warnings, [])
        self.assertIn("integer_to_list", parsed.validators["dynamic"]["message"]["$erlang_expression"])
        self.assertEqual(parsed.validators["adjacent"]["message"], "first second")
        self.assertIn("begin", parsed.validators["block"]["message"]["$erlang_expression"])


if __name__ == "__main__":
    unittest.main()
