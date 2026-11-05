import unittest
from unittest.mock import patch

import tls_probe


class FakeRawSocket:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class FakeTlsSocket:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def version(self):
        return "TLSv1.3"

    def cipher(self):
        return ("TLS_AES_128_GCM_SHA256", "TLSv1.3", 128)

    def getpeercert(self, binary_form=False):
        if binary_form:
            return b"synthetic-certificate"
        return {
            "subject": ((("commonName", "example.invalid"),),),
            "issuer": ((("commonName", "Example Test CA"),),),
            "notBefore": "Jan  1 00:00:00 2026 GMT",
            "notAfter": "Jan  1 00:00:00 2027 GMT",
            "subjectAltName": (("DNS", "example.invalid"),),
        }


class FakeContext:
    def wrap_socket(self, raw, server_hostname):
        self.server_hostname = server_hostname
        return FakeTlsSocket()


class TlsProbeTests(unittest.TestCase):
    def test_validates_target_before_opening_socket(self):
        for host in ("", " example.com", "https://example.com", "user@example.com"):
            with self.subTest(host=host), self.assertRaises(ValueError):
                tls_probe.probe(host)
        with patch.object(tls_probe.socket, "create_connection") as connect:
            with self.assertRaises(ValueError):
                tls_probe.probe("example.com", port=65536)
            connect.assert_not_called()

    def test_rejects_nonfinite_and_boolean_timeouts(self):
        for timeout in (0, -1, float("inf"), float("nan"), True):
            with self.subTest(timeout=timeout), self.assertRaises(ValueError):
                tls_probe.probe("example.com", timeout=timeout)

    def test_verified_success_returns_protocol_cipher_and_fingerprint(self):
        with patch.object(tls_probe.ssl, "create_default_context", return_value=FakeContext()):
            with patch.object(tls_probe.socket, "create_connection", return_value=FakeRawSocket()) as connect:
                result = tls_probe.probe("example.invalid", 443, 1.5)
        self.assertTrue(result["ok"])
        self.assertEqual(result["tls_version"], "TLSv1.3")
        self.assertEqual(result["cipher_bits"], 128)
        self.assertEqual(result["verification"], "enabled")
        self.assertEqual(connect.call_args.kwargs["timeout"], 1.5)
        self.assertEqual(len(result["certificate"]["sha256_fingerprint"]), 64)

    def test_handshake_error_is_reported_as_data(self):
        import ssl
        with patch.object(tls_probe.ssl, "create_default_context", return_value=FakeContext()):
            with patch.object(tls_probe.socket, "create_connection", side_effect=ssl.SSLError("bad handshake")):
                result = tls_probe.probe("example.invalid")
        self.assertFalse(result["ok"])
        self.assertEqual(result["category"], "connection_or_handshake")


if __name__ == "__main__":
    unittest.main()
