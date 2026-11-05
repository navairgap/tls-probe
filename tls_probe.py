#!/usr/bin/env python3
"""Inspect TLS on one explicitly supplied host and port; standard library only."""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
import socket
import ssl
import sys


def _validate(host: str, port: int, timeout: float) -> None:
    if not isinstance(host, str) or not host or host != host.strip():
        raise ValueError("host must be a non-empty hostname or IP address")
    if any(ch.isspace() or ch in "/?#@" for ch in host):
        raise ValueError("host must not contain URL paths, credentials or whitespace")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("port must be an integer from 1 to 65535")
    if (isinstance(timeout, bool) or not isinstance(timeout, (int, float))
            or not math.isfinite(timeout) or timeout <= 0 or timeout > 30):
        raise ValueError("timeout must be finite and between 0 and 30 seconds")


def _name_parts(value: object) -> list[list[str]]:
    parts: list[list[str]] = []
    if isinstance(value, tuple):
        for group in value:
            if isinstance(group, tuple):
                for pair in group:
                    if isinstance(pair, tuple) and len(pair) == 2:
                        parts.append([str(pair[0]), str(pair[1])])
    return parts


def probe(host: str, port: int = 443, timeout: float = 3.0,
          insecure: bool = False) -> dict[str, object]:
    """Perform one TLS handshake. Certificate verification is on by default."""
    _validate(host, port, timeout)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) if insecure else ssl.create_default_context()
    if insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection((host, port), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=host) as tls:
                cert = tls.getpeercert()
                der = tls.getpeercert(binary_form=True)
                cipher = tls.cipher() or (None, None, None)
                return {
                    "ok": True,
                    "target": host,
                    "port": port,
                    "verification": "disabled" if insecure else "enabled",
                    "tls_version": tls.version(),
                    "cipher": cipher[0],
                    "cipher_bits": cipher[2],
                    "certificate": {
                        "subject": _name_parts(cert.get("subject")),
                        "issuer": _name_parts(cert.get("issuer")),
                        "not_before": cert.get("notBefore"),
                        "not_after": cert.get("notAfter"),
                        "subject_alt_names": [
                            [str(kind), str(name)] for kind, name in cert.get("subjectAltName", ())
                        ],
                        "sha256_fingerprint": hashlib.sha256(der).hexdigest() if der else None,
                    },
                }
    except ssl.SSLCertVerificationError as exc:
        return {"ok": False, "target": host, "port": port,
                "category": "certificate_validation", "error": str(exc),
                "verification": "enabled"}
    except (OSError, ssl.SSLError) as exc:
        return {"ok": False, "target": host, "port": port,
                "category": "connection_or_handshake", "error": str(exc),
                "verification": "disabled" if insecure else "enabled"}


def positive_timeout(value: str) -> float:
    try:
        result = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("timeout must be a positive number") from exc
    if not math.isfinite(result) or not 0 < result <= 30:
        raise argparse.ArgumentTypeError("timeout must be finite and between 0 and 30 seconds")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", help="one explicitly selected host or IP address")
    parser.add_argument("-p", "--port", type=int, default=443)
    parser.add_argument("-t", "--timeout", type=positive_timeout, default=3.0)
    parser.add_argument("--insecure", action="store_true",
                        help="disable certificate verification for diagnostics only")
    args = parser.parse_args(argv)
    try:
        result = probe(args.host, args.port, args.timeout, args.insecure)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
