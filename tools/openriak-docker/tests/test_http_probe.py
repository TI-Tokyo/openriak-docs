import subprocess
import unittest
from unittest import mock
from test_openriak_docker import docker_tool as tool


class HttpProbeTests(unittest.TestCase):
    def test_status_and_body_are_both_reported_without_curl(self):
        for status, body in ((200, b'OK'), (503, b'OK'), (200, b'not ready')):
            response = f'HTTP/1.0 {status} Reply\r\nContent-Length: {len(body)}\r\n\r\n'.encode() + body
            with self.subTest(status=status, body=body), mock.patch.object(tool, 'docker_command', return_value='docker'), \
                    mock.patch.object(tool, 'run_before_deadline', return_value=subprocess.CompletedProcess([], 0, response, b'')) as run:
                self.assertEqual(tool.container_http_ping('node', 19), (0, body.decode(), status))
                command = run.call_args.args[0]
                self.assertNotIn('curl', command)
                self.assertEqual(command[-1], '19000')
                self.assertIn(tool.HTTP_PROBE_ERLANG, command)

    def test_connection_errors_and_invalid_responses_cannot_pass(self):
        cases = [(1, b'', b'connection refused'), (0, b'not HTTP\r\n\r\nOK', b''),
                 (0, b'HTTP/1.0 200 OK\r\nContent-Length: 3\r\n\r\nOK', b'')]
        for code, stdout, stderr in cases:
            with self.subTest(stdout=stdout), mock.patch.object(tool, 'docker_command', return_value='docker'), \
                    mock.patch.object(tool, 'run_before_deadline', return_value=subprocess.CompletedProcess([], code, stdout, stderr)):
                exit_code, body, status = tool.container_http_ping('node', 19)
                self.assertNotEqual(exit_code, 0)
                self.assertEqual(status, 0)

    def test_no_package_installation_adds_curl_and_alpine_keeps_coreutils(self):
        for target in tool.discover_targets():
            with self.subTest(image=target.image):
                script = tool.package_install_script(target)
                self.assertNotIn('curl', script)
                if target.family == 'alpine':
                    self.assertIn('coreutils', script)
        subprocess.run(['sh', '-n'], input=tool.HTTP_PROBE_COMMAND, text=True, check=True, capture_output=True)
