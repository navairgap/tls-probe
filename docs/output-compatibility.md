# output compatibility

Treat machine-readable output as a compatibility contract. Keep field names stable, represent missing certificate data as null or an explicit status, and separate connection failure from certificate validation failure. Send diagnostics to stderr so stdout remains parseable JSON. Include negotiated protocol and cipher only when known. Add a schema version before making incompatible output changes.

## Error category contract

Use stable machine-readable error categories such as `dns_error`, `connect_timeout`, `handshake_error`, `certificate_untrusted`, and `hostname_mismatch`. Human-readable diagnostic messages may change, but scripts should branch on the category and documented exit code. Keep any low-level library message in a separate optional diagnostic field and never include credentials from an endpoint URL.
