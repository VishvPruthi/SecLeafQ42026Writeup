# LeafSync — Forensics Writeup

**Category:** Forensics (DNS Exfiltration)  
**Points:** 150  
**Challenge:** LeafSync  
**Flag:** `SecLeaf{dns_labels_hide_the_truth}`

## Challenge Description

A developer workstation downloaded a synchronization helper from an internal documentation server and subsequently started sending repeated DNS queries to an unfamiliar domain.

The objective was to analyze the PCAP file and determine what information was exfiltrated through DNS.

**File:** `leafsync.pcap`

---

## Investigation

### Stage 1: HTTP — Identifying the Trigger

I started by opening `leafsync.pcap` in Wireshark.


I identified a request from the developer workstation:

```text
Source: 10.20.30.15
Destination: docs.internal.local
Request: GET /tools/leafsync-helper.sh
```

I followed the HTTP stream to inspect the downloaded script.

The script only printed a startup message and did not contain the exfiltrated information.

This suggested that the HTTP download was the trigger for the suspicious activity rather than the actual payload.

![LeafSync](screenshots/01.png)

### Stage 2: DNS — Discovering the Exfiltration

After the HTTP request, I examined DNS traffic.

I identified repeated DNS queries from:

```text
10.20.30.15
```

to the DNS server:

```text
10.20.30.53
```

The queries were directed to an unfamiliar domain:

```text
sync-cache.training.local
```

The query names followed a consistent structure:

![LeafSync](screenshots/02.png)

```text
01.<chunk>.sync-cache.training.local
02.<chunk>.sync-cache.training.local
03.<chunk>.sync-cache.training.local
...
06.<chunk>.sync-cache.training.local
```

Each query contained a sequence number and a Base64-encoded data chunk.

![LeafSync](screenshots/03.png)

### Stage 3: Extracting the Base64 Chunks

I extracted the encoded labels from the six DNS queries and arranged them in sequence order.

| Sequence | Base64 Chunk | Decoded Content |
|:---:|---|---|
| 01 | `U2VjTGVh` | `SecLea` |
| 02 | `ZntkbnNf` | `f{dns_` |
| 03 | `bGFiZWxz` | `labels` |
| 04 | `X2hpZGVf` | `_hide_` |
| 05 | `dGhlX3Ry` | `the_tr` |
| 06 | `dXRofQ==` | `uth}` |

The encoded chunks were concatenated in the original sequence order.

![LeafSync](screenshots/04.png)


## Noise and Decoys

During the investigation, I also observed unrelated DNS queries.

| Domain | Observation |
|---|---|
| github.com | Background activity |
| pypi.org | Background activity |
| ntp.pool.org | Time synchronization |
| *.internal.local | Internal lookups |
| sync-cache.training.local | Suspicious encoded queries |

The unfamiliar parent domain, sequential labels, and encoded content distinguished the exfiltration traffic from normal DNS activity.

---

## Final Flag

```text
SecLeaf{dns_labels_hide_the_truth}
```

## Conclusion

This challenge demonstrated how DNS can be used as a covert data exfiltration channel.

The downloaded helper acted as the trigger, while the subsequent DNS queries carried Base64-encoded information inside their question names.

By identifying the suspicious domain, extracting the sequential labels, and decoding the Base64 chunks, I successfully recovered the flag.
