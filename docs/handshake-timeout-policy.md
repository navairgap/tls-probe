# TLS connection and handshake deadlines (proposed)

TLS probing should use finite, independently documented deadlines so a slow or unresponsive endpoint cannot hold a CLI process indefinitely.

## Deadline phases

- **Name resolution:** apply a bounded resolution timeout where the platform API permits it. Document when the system resolver cannot be interrupted.
- **TCP connect:** bound the time spent establishing the socket connection.
- **TLS handshake:** start a separate deadline after the TCP connection succeeds. Do not reset it for every partial handshake record.
- **Overall operation:** optionally apply a total deadline that caps the sum of all phases and any retry delay.

Use a monotonic clock for elapsed-time calculations. Wall-clock changes must not extend a running operation.

## Failure categories

Report DNS failure, connect timeout, connection refusal, handshake timeout, protocol negotiation failure, and certificate validation failure as distinct categories. A timeout is not evidence that a certificate is invalid. A valid TCP connection followed by a failed TLS handshake should not be reported as a simple closed port.

## Cancellation and cleanup

On timeout, close the socket and release TLS resources before returning. Do not leave a background task or retry loop running after the CLI has reported failure. Any retry policy must be bounded and must not silently retry certificate-validation failures.

## Test matrix

Use a local controlled server or mocked transport. Cover slow DNS where testable, connect timeout, a server that accepts TCP but never completes TLS, a handshake that finishes just before the deadline, and cleanup after cancellation. Avoid public internet dependencies and long sleeps; inject clocks or use short local deadlines.