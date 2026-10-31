# TLS probe JSON output schema v1 (proposed)

The first machine-readable output should be a stable contract rather than a dump of library-specific objects. This schema is a design proposal; no CLI implementation is implied.

## Top-level fields

- **schema_version:** integer, initially 1.
- **target:** configured hostname or IP and requested port.
- **observed_at:** RFC 3339 timestamp with an explicit UTC offset.
- **status:** success or error.
- **connection:** phase and elapsed durations when known.
- **tls:** negotiated protocol and cipher suite when a handshake completes.
- **certificate:** subject, issuer, validity interval, SAN entries, and chain-validation status when available.
- **error:** stable category and optional diagnostic code when status is error.

Unavailable values should be represented as null or a documented status, not fabricated defaults. Do not represent an unknown protocol as an empty string if the field is semantically absent.

## Compatibility rules

Keep field names and types stable within a schema version. Add optional fields in a backward-compatible release. Introduce a new schema version for incompatible changes, and document how consumers can distinguish versions. Human-readable messages may change; scripts should branch on stable error categories and exit codes.

## Output hygiene

Write exactly one JSON document to stdout for a single probe. Send progress and diagnostic logging to stderr. Never include URL credentials, private key material, environment variables, or raw TLS application data. Limit certificate chain detail to the documented output size.

## Validation fixtures

Check successful TLS, expired and untrusted certificates, SAN mismatch, unavailable negotiated fields, DNS/connect/handshake failures, and malformed endpoint input. Parse every emitted fixture with a standard JSON parser and assert that errors still produce valid JSON.