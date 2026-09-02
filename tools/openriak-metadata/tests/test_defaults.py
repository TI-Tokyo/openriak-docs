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

    def test_nested_package_templates_are_resolved(self):
        setting = self.setting({"$template": "{{repl_data_root}}"})
        package = self.calculate(setting, package={
            "platform_data_dir": "/var/lib/riak",
            "repl_data_root": "{{platform_data_dir}}/riak_repl",
        })
        self.assertEqual(package["value"], "/var/lib/riak/riak_repl")
        self.assertEqual(package["resolved_value"], "/var/lib/riak/riak_repl")
        structured = self.calculate(self.setting({"$erlang_tuple": [
            "{{web_ip}}", {"$template": "{{web_port}}"}, ["{{platform_data_dir}}/listener"]
        ]}), package={"web_ip": "127.0.0.1", "web_port": 8098, "platform_data_dir": "/var/lib/riak"})
        self.assertEqual(structured["resolved_value"], {
            "$erlang_tuple": ["127.0.0.1", 8098, ["/var/lib/riak/listener"]]
        })

    def test_vars_and_rpm_generated_vars(self):
        self.assertEqual(parse_vars('[{logger_level, info}, {platform_log_dir, "/tmp/log"}].'),
                         {"logger_level": "info", "platform_log_dir": "/tmp/log"})
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rpm = root / "rel" / "pkg" / "rpm"; rpm.mkdir(parents=True)
            (rpm / "vars.config.part").write_text('[{logger_level, info}].', encoding="utf-8")
            (rpm / "specfile").write_text(
                '%define _riak_logdir %{_localstatedir}/log/riak\n'
                '%define platform_data_dir %{_localstatedir}/lib/riak\n'
                'echo "{platform_log_dir, \\"%{_riak_logdir}\\"}."\n'
                'echo "{platform_data_dir, \\"%{platform_data_dir}\\"}."\n'
                'echo "{platform_lib_dir, \\"%{_libdir}/riak/lib\\"}."\n'
                'echo "{platform_etc_dir, \\"%{_sysconfdir}/riak\\"}."\n',
                encoding="utf-8",
            )
            values, sources = parse_rpm_vars(rpm, root)
            self.assertEqual(values["logger_level"], "info")
            self.assertEqual(values["platform_log_dir"], "/var/log/riak")
            self.assertEqual(values["platform_data_dir"], "/var/lib/riak")
            self.assertEqual(values["platform_lib_dir"], "/usr/lib64/riak/lib")
            self.assertEqual(values["platform_etc_dir"], "/etc/riak")
            self.assertTrue(all(s["source_type"] == "rpm-generated-vars" for s in sources))


if __name__ == "__main__":
    unittest.main()
