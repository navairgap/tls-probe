# TLS probe output contract

The command accepts exactly one operator-selected hostname or IP address and
one TCP port. It does not enumerate hosts, ports, or certificate names.

Certificate verification is enabled by default using the system trust store.
`--insecure` disables hostname and chain validation only for
diagnostics; its output explicitly records `verification: disabled`.
Never treat an insecure result as evidence that a certificate is trusted.

JSON output separates:
- connection or handshake failures;
- certificate-validation failures;
- successful negotiated protocol and cipher details;
- certificate subject, issuer, validity strings, SANs and SHA-256 fingerprint.

A failed connection is not automatically a certificate problem. DNS, routing,
firewalls, server availability, local trust stores and clock accuracy can all
affect the result. Keep stdout machine-readable and use the exit status:
0 for success, 1 for a probe failure, and 2 for invalid command-line input.
