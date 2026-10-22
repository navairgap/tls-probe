# output compatibility

Treat machine-readable output as a compatibility contract. Keep field names stable, represent missing certificate data as null or an explicit status, and separate connection failure from certificate validation failure. Send diagnostics to stderr so stdout remains parseable JSON. Include negotiated protocol and cipher only when known. Add a schema version before making incompatible output changes.
