# tls test matrix

Use local fixtures or a controlled test server. Cover valid certificates, expired certificates, hostname mismatch, untrusted chains, unsupported protocols, refused connections, slow handshakes, and invalid host/port input. Enforce finite timeouts and keep JSON output valid on failures. Certificate validation must remain enabled by default; any insecure diagnostic mode must be explicit and clearly marked.

## Certificate identity fixtures

Include certificates with multiple DNS subject alternative names, an IP-address SAN, a wildcard SAN, and a legacy common-name value without a SAN. Verify that hostname matching follows the platform's current certificate rules and that a common name is not silently used to override a mismatching SAN. Include a chain where the leaf is valid but an intermediate is expired, and report the chain error separately from hostname mismatch. Keep all private test keys local to the fixture generator.
