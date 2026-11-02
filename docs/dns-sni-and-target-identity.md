# DNS resolution, SNI, and target identity (proposed)

TLS-Probe is still a documentation-only design. This contract separates the
operator's requested identity from the network address used for a connection.

## Keep the identities separate

For every probe, retain these as distinct values:

1. **Configured target** — the hostname or IP address supplied by the operator.
2. **Resolved address** — the A or AAAA address selected for this connection.
3. **SNI name** — the DNS hostname sent in the TLS ClientHello, when applicable.
4. **Verification name** — the configured DNS hostname or IP identity checked
   against the peer certificate.

Do not replace the configured hostname with its resolved IP for certificate
verification. DNS resolution selects a route to the service; it does not change
the identity the operator asked to inspect.

## DNS behavior

- Resolve only the explicitly configured target.
- Apply a finite resolution deadline and report DNS failure separately from
  TCP connection and TLS handshake failure.
- Record the selected address and address family in the result.
- Do not silently retry an unbounded list of addresses. If multi-address
  probing is added, make the policy explicit and give each attempt its own
  bounded deadline and result.
- Do not follow HTTP redirects or discover additional hosts. TLS-Probe inspects
  the selected endpoint; it is not a crawler or subnet scanner.

## SNI and certificate verification

- For a DNS hostname, send that hostname as SNI and verify the certificate
  against the same configured hostname.
- For an IP-literal target, do not invent a DNS SNI name. Verify the peer
  certificate against an IP-address subject alternative name.
- Keep certificate-chain validation enabled by default.
- A diagnostic option that disables verification, if ever added, must be
  explicit in the command line and unmistakable in human and JSON output.
- A SAN mismatch must not be hidden by a legacy common-name fallback when SAN
  entries are present.

## Result fields

The versioned JSON result should expose the requested target and selected
resolved address separately. Include the SNI and verification identities when
known, and use null or a documented status when a value does not apply. Never
report an IP address as the requested hostname merely because DNS resolved it.

## Test matrix

Use local controlled TLS fixtures to verify:

- a hostname resolves to an IP but is verified using the hostname;
- multiple A/AAAA answers follow the documented selection policy;
- an IP-literal target is verified as an IP SAN and sends no guessed SNI;
- DNS timeout and no-record outcomes are distinct from connect timeout;
- SAN mismatch fails even when a legacy common name matches;
- redirects and names discovered from remote responses are never followed.

Keep fixture keys local. Tests must not require public services or disable
certificate verification to pass.
