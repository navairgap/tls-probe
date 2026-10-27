# TLS probe JSON output (draft v1)

This is the proposed machine-readable output contract. The probe remains design-stage until implementation and fixture tests are added.

## Example

```json
{
  "schema_version": 1,
  "target": { "host": "example.test", "port": 443 },
  "connected": true,
  "tls": {
    "version": "TLSv1.3",
    "cipher": "TLS_AES_128_GCM_SHA256",
    "alpn": "h2"
  },
  "certificate": {
    "subject": "CN=example.test",
    "issuer": "CN=Example Test CA",
    "not_before": "2026-01-01T00:00:00Z",
    "not_after": "2027-01-01T00:00:00Z",
    "chain_valid": true
  },
  "error": null
}
```

## Verification result semantics

The JSON contract must separate certificate-chain trust from hostname verification. A valid chain for a different hostname is not a successful verification of the requested target. Report hostname matching independently (for example, `certificate.hostname_valid`) and define any aggregate `verified` value as true only when every verification check requested by the operator succeeds. Tests should include a trusted certificate with the wrong hostname, an expired certificate, and a self-signed certificate.

## Stability rules

- Keep `schema_version` as an integer and increment it only for incompatible changes.
- Represent unavailable values as JSON `null`; do not fabricate empty strings or success defaults.
- `connected` means a TLS handshake completed, not that the application is healthy.
- `chain_valid` reflects normal trust-store validation. Any diagnostic verification bypass must be opt-in and must be clearly represented in output.
- Errors should have a stable machine-readable `code` and a human-readable `message`; avoid embedding secrets or unbounded remote text.
- Timestamps are UTC RFC 3339. Hostnames should be preserved as requested while connection addresses, if reported, remain separate fields.

## Exit status proposal

- `0`: handshake completed and no requested check failed.
- `1`: connection or requested TLS check failed.
- `2`: invalid CLI arguments or configuration.

## Tests

Use local certificates and a loopback TLS server. Do not make public internet access a requirement for unit tests.
