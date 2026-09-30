# tls-probe

Grade the TLS configuration of your own services

> 🚧 **Status: planning** — architecture and README first, code next.

## Why

TLS is easy to get wrong: old protocols, weak ciphers, expiring certs. tls-probe connects to your own services and grades them like SSL Labs does — but entirely local and scriptable.

## Planned features

- Scan your services for protocol/cipher weaknesses
- Certificate expiry tracking with advance warnings
- A–F grading with concrete fix commands
- JSON output for cron + dashboards

## Stack

`python` `ssl` `cryptography`

## Notes

Only ever connects to hosts you explicitly list — it's an auditor, not a scanner.

## License

MIT, see [LICENSE](LICENSE).

---
maintained · verified 2026-09-30
