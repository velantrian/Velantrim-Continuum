"""Timeout / connection loss after send is UNKNOWN_OUTCOME, distinct from error; never retried."""
from __future__ import annotations

import http.client
import importlib.util
import io
import socket
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "scripts" / "e0" / "adapters" / "openrouter_capture_adapter.py"
spec = importlib.util.spec_from_file_location("openrouter_capture_adapter_uo", ADAPTER)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class _Opener:
    def __init__(self, exc):
        self.exc, self.calls = exc, 0

    def open(self, req, timeout):
        self.calls += 1
        raise self.exc


class UnknownOutcomeTests(unittest.TestCase):
    def transport_with(self, exc):
        op = _Opener(exc)
        with mock.patch.object(adapter.urllib.request, "build_opener", return_value=op):
            try:
                adapter.default_transport(adapter.ENDPOINT, b"{}", {}, 1.0)
            finally:
                self.assertEqual(op.calls, 1, "single attempt, no retry")

    def test_socket_timeout_is_unknown(self):
        with self.assertRaises(adapter.CaptureUnknownOutcome):
            self.transport_with(socket.timeout("timed out"))

    def test_urlerror_timeout_is_unknown(self):
        with self.assertRaises(adapter.CaptureUnknownOutcome):
            self.transport_with(urllib.error.URLError(TimeoutError("t")))

    def test_reset_after_send_is_unknown(self):
        for exc in (ConnectionResetError(), http.client.RemoteDisconnected("x"), http.client.IncompleteRead(b"")):
            with self.subTest(exc=type(exc).__name__), self.assertRaises(adapter.CaptureUnknownOutcome):
                self.transport_with(exc)

    def test_pre_send_failures_are_plain_error(self):
        for exc in (urllib.error.URLError(socket.gaierror("dns")), ConnectionRefusedError()):
            with self.subTest(exc=type(exc).__name__):
                with self.assertRaises(adapter.CaptureAdapterError) as cm:
                    self.transport_with(exc)
                self.assertNotIsInstance(cm.exception, adapter.CaptureUnknownOutcome)

    def test_main_exit_code_4_distinct(self):
        def boom(*a, **k):
            raise adapter.CaptureUnknownOutcome("transport timeout: TimeoutError")
        err = io.StringIO()
        with mock.patch.object(adapter, "run", boom), mock.patch("sys.stdin", io.StringIO("{}")), mock.patch("sys.stderr", err):
            self.assertEqual(adapter.main([]), 4)
        self.assertIn("CAPTURE_ADAPTER_UNKNOWN_OUTCOME", err.getvalue())


if __name__ == "__main__":
    unittest.main()
