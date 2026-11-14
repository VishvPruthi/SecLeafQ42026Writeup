# Blackroot Archive — Forensics Writeup

**Category:** Forensics  
**Points:** 200  
**Challenge:** Blackroot Archive  
**Flag:** `SecLeaf{exported_objects_reveal_the_archive_key}`

## Challenge Description

A finance workstation downloaded a ledger synchronization manifest, an internal archive notice was sent to operations, and unusual communication with an external archive service followed.

The objective was to analyze the provided PCAP file and recover the hidden flag by following the clues left in the network traffic.

**File:** `blackroot_archive.pcap`

---

## Investigation

### Stage 1: HTTP — Discovering the Manifest

I started by opening the PCAP file in Wireshark and examining the HTTP traffic.

I identified a request from workstation `10.88.12.15` for:

```http
GET /exports/ledger-sync.manifest
```

The response contained Base64-encoded data.

To reconstruct the complete response, I used:

```text
Right-click packet → Follow → TCP Stream
```
![Blackroot Archive Forensics Walkthrough](screenshots/01.png)

After extracting and decoding the Base64 content, I obtained:

```text
BLACKROOT_ARCHIVE_MANIFEST, artifact=ledger-sync-2026, encoding=base64, key_source=mail:archive-notice, next_service=tcp/4711
```

![Blackroot Archive Forensics Walkthrough](screenshots/03.png)

The manifest provided two important clues:

- `key_source=mail:archive-notice` indicated that the recovery key was available in an email.
- `next_service=tcp/4711` indicated that the archive data was transmitted over TCP port 4711.

This directed the investigation toward SMTP traffic and the unusual TCP service.

### Stage 2: SMTP — Recovering the XOR Key

Next, I examined the SMTP communication.

**Wireshark filter:**

```text
smtp
```
![Blackroot Archive Forensics Walkthrough](screenshots/04.png)

I identified the relevant SMTP session involving `10.88.12.22` and followed the TCP stream.

Inside the archive notice, I found:

![Blackroot Archive Forensics Walkthrough](screenshots/02.png)

```text
Recovery key: rootleaf
```

The recovered key was:

```text
rootleaf
```

The email provided the key required to decode the archive data.

### Stage 3: TCP/4711 — Extracting the Archive

Using the port identified in the manifest, I filtered the traffic:

```text
tcp.port == 4711
```

The connection involved:

```text
Source:      10.88.12.15
Destination:  198.51.100.144
Port:        4711
```

I followed the TCP stream and discovered ten records containing hexadecimal blobs:

![Blackroot Archive Forensics Walkthrough](screenshots/05.png)

```text
record=01;blob=<hex>
record=02;blob=<hex>
record=03;blob=<hex>
...
record=10;blob=<hex>
```

I extracted the hexadecimal data from all ten records and concatenated them in record order.

The reconstructed payload was **64 bytes**.

The complete hexadecimal payload was:

```text
275d391e3822370e28011b18092d231011013d18362358102b021f183556331c2a5c25180808370e102956440d2237002b37251e0d220d5428395606363d0d5f
```

### Stage 4: XOR and Base64 Decoding

The manifest and email provided everything needed for the final decoding stage:

- Archive payload: 64 bytes
- XOR key: `rootleaf`
- Encoding: Base64

I first converted the hexadecimal payload into bytes, then XORed it with the repeating key `rootleaf`.

The XOR operation produced the following Base64 string:

![Blackroot Archive Forensics Walkthrough](screenshots/06.png)

```text
U2VjTGVhZntleHBvcnRlZF9vYmplY3RzX3JldmVhbF90aGVfYXJjaGl2ZV9rZXl9
```

Finally, I decoded the Base64 string to recover the flag.

![Blackroot Archive Forensics Walkthrough](screenshots/07.png)

## Final Flag

```text
SecLeaf{exported_objects_reveal_the_archive_key}
```

## Conclusion

This challenge demonstrated how multiple network protocols can contain connected forensic clues.

The HTTP manifest identified the location of the recovery key and the archive service. The SMTP notice revealed the XOR key, and the TCP/4711 connection carried the encrypted archive payload.

By reconstructing the TCP stream, concatenating the hexadecimal records, applying repeating-key XOR, and decoding the resulting Base64, I successfully recovered the flag.

**Tools Used:**

- Wireshark
- cyberchef
