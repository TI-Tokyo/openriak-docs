import unittest

from openriak_metadata.defaults import resolve_config_references, resolve_templates
from openriak_metadata.schema import merge_mappings, parse_schema


SCHEMA = '''
%% @doc How Riak repairs out-of-sync keys.
%% More details.
%% @see another.setting
{mapping, "anti_entropy", "riak_kv.anti_entropy", [
  {default, active},
  {datatype, {enum, [active, passive, 'active-debug']}},
  {validators, [scheduler_absolute]},
  {hidden, false},
  {commented, passive},
  {new_conf_value, active},
  {include_default, true}
]}.
{translation, "riak_kv.anti_entropy", fun(Conf) -> case Conf of X -> X end end}.
{validator, scheduler_absolute, "must be 1 to 1024", fun(Value) -> Value > 0 end}.
'''


class SchemaTests(unittest.TestCase):
    def test_schema_metadata_and_opaque_functions(self):
        parsed = parse_schema(SCHEMA, "riak_kv", "priv/riak_kv.schema")
        self.assertEqual(parsed.warnings, [])
        mapping = parsed.mappings[0]
        self.assertEqual(mapping["default"], "active")
        self.assertEqual(mapping["datatype"]["values"], ["active", "passive", "active-debug"])
        self.assertEqual(mapping["validators"], ["scheduler_absolute"])
        self.assertEqual(mapping["documentation"], "How Riak repairs out-of-sync keys. More details.")
        self.assertEqual(mapping["see"], ["another.setting"])
        self.assertIn("case Conf", parsed.translations[0]["raw_erlang"])
        self.assertIn("Value > 0", parsed.validators["scheduler_absolute"]["raw_erlang"])

    def test_duplicate_and_merge_semantics(self):
        first = {"key": "a", "default": 1, "merge": False, "source": {"path": "a", "line": 1}}
        replacement = {"key": "a", "default": 2, "merge": False, "source": {"path": "b", "line": 2}}
        supplement = {"key": "a", "hidden": True, "merge": True, "source": {"path": "c", "line": 3}}
        settings, _ = merge_mappings([first, replacement, supplement])
        self.assertEqual(settings["a"]["default"], 2)
        self.assertTrue(settings["a"]["hidden"])
        self.assertEqual(len(settings["a"]["definitions"]), 3)

    def test_templates_and_references(self):
        value, names, complete = resolve_templates({"$template": "{{logger_level}}"}, {"logger_level": "warning"})
        self.assertEqual((value, names, complete), ("warning", ["logger_level"], True))
        settings = {"log.dir": {"has_default": True, "default": "/var/log/riak"}}
        self.assertEqual(resolve_config_references("$(log.dir)/console.log", settings, {}),
                         "/var/log/riak/console.log")
        circular = {"a": {"has_default": True, "default": "$(b)"},
                    "b": {"has_default": True, "default": "$(a)"}}
        self.assertIsNone(resolve_config_references("$(a)", circular, {}))


if __name__ == "__main__":
    unittest.main()
