# TLS target input contract (proposed)

TLS-Probe accepts one explicitly selected endpoint. The input contract should be unambiguous before a CLI parser or network adapter is implemented.

## Host and port

- Accept a plain DNS hostname or an IP address literal as the host value.
- Reject URL schemes, paths, query strings, fragments, user-info, and embedded ports in the host field. The port is a separate integer argument.
- Accept ports from 1 through 65535. Port zero is not a remote service destination.
- Parse IPv4 and IPv6 literals as addresses, not as DNS names. Do not pass an IP literal as a guessed SNI hostname.
- Reject empty hosts, whitespace, control characters, and malformed address literals before any network operation.

## Identity and resolution

Keep the operator-supplied hostname, selected resolved address, SNI name, and certificate verification identity separate. Apply the rules in [DNS, SNI, and target identity](dns-sni-and-target-identity.md): resolving a hostname must not change the name used for certificate verification. Do not follow redirects or probe additional hosts discovered from remote responses.

## Validation and errors

Input validation errors should have a stable CLI exit category and must occur before DNS lookup or socket creation. Do not echo credentials or control characters into terminal diagnostics. JSON output should identify the requested host and port while preserving the distinction between invalid input, DNS failure, connect failure, handshake failure, and certificate validation failure.

## Local test cases

Use table-driven tests for empty input, whitespace, URL-shaped input, embedded ports, bracketed and unbracketed IPv6 literals, invalid numeric ports, port zero, and the valid boundary ports 1 and 65535. Tests must not need public DNS or an external TLS endpoint.
