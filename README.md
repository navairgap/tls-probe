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

## Sample output

```
$ python3 tls_probe.py example.com
protocol  : TLSv1.3
cipher    : TLS_AES_256_GCM_SHA384
cert      : CN=example.com (expires 2027-01-15)
flags     : HSTS · OCSP stapling
weakness  : accepts TLSv1.0 on port 443 — recommend disabling
```

## FAQ

**Why is TLS 1.3 early data not reported?**
Early data (0-RTT) is only observable when the client offers it; most browsers don't against new servers. The probe flags it when seen.

**Does it grade like SSL Labs?**
No — it reports raw facts. Grading is opinion; facts are not.


## CI

Runs the unittest suite on 3.9–3.12 on every push. The probe has no network-dependent tests — everything is mocked, so CI is hermetic.


## Exit codes

`0` all checks parsed cleanly. `1` host unreachable or handshake failed. `2` certificate unparseable. script against them freely.


## Requirements

python 3.9+, nothing else. no openssl binary needed — the probe speaks TLS itself.
