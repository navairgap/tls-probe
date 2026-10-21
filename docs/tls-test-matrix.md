# tls test matrix

Use local fixtures or a controlled test server. Cover valid certificates, expired certificates, hostname mismatch, untrusted chains, unsupported protocols, refused connections, slow handshakes, and invalid host/port input. Enforce finite timeouts and keep JSON output valid on failures. Certificate validation must remain enabled by default; any insecure diagnostic mode must be explicit and clearly marked.
