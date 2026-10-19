# tls-probe

A planned CLI for inspecting TLS configuration on explicitly selected services.

> **Status: design stage.** This repository currently contains documentation only; the probe and its tests are not implemented yet.

## Goal

Collect useful, scriptable facts about a TLS connection so an operator can spot outdated protocol support, certificate problems, and unexpected handshake behavior.

## Proposed output

The initial version should report:

- negotiated TLS version and cipher suite;
- certificate subject, issuer, validity dates, and chain validation result;
- connection and handshake errors with actionable context;
- stable JSON output for scripts and monitoring.

The tool should report observations rather than invent a single universal A–F grade.

## Safety and scope

- Connect only to hostnames and ports explicitly supplied by the operator.
- Use connection timeouts and bounded retries.
- Validate certificates by default; any diagnostic bypass must be explicit and clearly marked insecure.
- Never send credentials, modify the remote service, or scan unrelated hosts.
- Treat DNS, routing, server configuration, and the local trust store as separate possible causes of failure.

## Planned milestones

- [ ] Define CLI arguments and stable exit codes.
- [ ] Add unit tests for certificate parsing using local fixtures.
- [ ] Implement a standard-library TLS handshake path.
- [ ] Add JSON output and certificate-expiry reporting.
- [ ] Document limitations and platform compatibility.

## Development

The test suite should be hermetic: unit tests must not require public internet access or depend on a third-party TLS endpoint. Integration checks, if added, should be opt-in.

## License

MIT. See [LICENSE](LICENSE).
