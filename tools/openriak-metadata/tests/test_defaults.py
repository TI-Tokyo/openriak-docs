import tempfile
import unittest
from pathlib import Path

from openriak_metadata.defaults import calculate_default, parse_rpm_vars, parse_vars


class DefaultsTests(unittest.TestCase):
    def setting(self, default="A"):
        return {"has_default": True, "default": default, "new_conf_value": None,
                "definitions": [{"repository": "riak", "path": "priv/riak.schema", "line": 1}]}

    def calculate(self, setting, release=None, package=None):
        release = release or {}; package = package or {}
        context = dict(release); context.update(package)
        return calculate_default("x", setting, context, release, package, [], [], {"x": setting})

    def test_precedence_and_commented_not_promoted(self):
        setting = self.setting("A")
        self.assertEqual(self.calculate(setting)["value"], "A")
        setting["new_conf_value"] = "B"
        self.assertEqual(self.calculate(setting)["value"], "B")
        absent = {"has_default": False, "default": None, "new_conf_value": None,
                  "commented": "not-active", "definitions": []}
        self.assertFalse(self.calculate(absent)["has_default"])

    def test_package_template_override(self):
        setting = self.setting({"$template": "{{logger_level}}"})
        base = self.calculate(setting, {"logger_level": "info"})
        package = self.calculate(setting, {"logger_level": "info"}, {"logger_level": "warning"})
        self.assertEqual(base["value"], "info")
        self.assertEqual(package["value"], "warning")
        self.assertEqual(package["source_layer"], "package")

    def test_vars_and_rpm_generated_vars(self):
        self.assertEqual(parse_vars('[{logger_level, info}, {platform_log_dir, "/tmp/log"}].'),
                         {"logger_level": "info", "platform_log_dir": "/tmp/log"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rpm = root / "rel" / "pkg" / "rpm"; rpm.mkdir(parents=True)
            (rpm / "vars.config.part").write_text('[{logger_level, info}].', encoding="utf-8")
            (rpm / "specfile").write_text('%define _riak_logdir /var/log/riak\necho "{platform_log_dir, \\"%{_riak_logdir}\\"}."\n', encoding="utf-8")
            values, sources = parse_rpm_vars(rpm, root)
            self.assertEqual(values["logger_level"], "info")
            self.assertEqual(values["platform_log_dir"], "/var/log/riak")
            self.assertTrue(all(s["source_type"] == "rpm-generated-vars" for s in sources))


if __name__ == "__main__":
    unittest.main()
