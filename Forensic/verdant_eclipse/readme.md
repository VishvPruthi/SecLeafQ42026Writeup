# Verdant Eclipse — Forensics Writeup

## Challenge Information

| Field | Details |
|---|---|
| Challenge | Verdant Eclipse |
| Category | Forensics |
| Points | 300 |
| PCAP | `verdant_eclipse.pcap` |
| Flag Format | `SecLeaf{}` |

## Overview

Verdant Eclipse is a multi-stage network forensic challenge involving HTTP, DNS, and UDP traffic.

The objective is to investigate suspicious network activity, identify a hidden XOR key through DNS queries, reconstruct encrypted data from UDP packets, and decode the final flag.

The investigation follows three major stages:

1. Analyze HTTP traffic to identify the suspicious activity.
2. Extract the XOR key from DNS query labels.
3. Reconstruct and decrypt UDP payload chunks to recover the flag.

---

## Step 1:

First, open `verdant_eclipse.pcap` in Wireshark.

Look for suspicious DNS queries containing:

```text
alpha.verdant-lab.local
```

The following queries contain encoded information:

```text
01.Zm9s.alpha.verdant-lab.local
02.aWFn.alpha.verdant-lab.local
03.ZQ==.alpha.verdant-lab.local
```
![DNS Traffic](screenshots/001.png)

The numbered labels indicate the correct order of the encoded chunks.

### Extract the Base64 chunks

| Sequence | Base64 Chunk |
|---|---|
| 01 | `Zm9s` |
| 02 | `aWFn` |
| 03 | `ZQ==` |

Concatenate the chunks:

```text
Zm9saWFnZQ==
```
### Decode using CyberChef

Open CyberChef and use the following operation:

```text
From Base64
```

Input:

```text
Zm9saWFnZQ==
```

Output:

```text
foliage
```
![Base64 Decode](screenshots/01.png)

The extracted XOR key is:

```text
foliage
```

---

## Step 2: Identify the UDP Exfiltration Traffic

The next stage contains encrypted data transmitted through UDP.

The suspicious destination is:

```text
198.51.100.77:6060
```
Inspect the UDP payloads and look for messages containing:

```text
channel=leafsync
```
The packets contain numbered hexadecimal chunks.

Other traffic, such as `metrics` on port 6060 and `backup` on port 9000, should not be confused with the relevant `leafsync` data.

### Extract the hexadecimal chunks

| Sequence | Hexadecimal Chunk |
|---|---|
| 01 | `335d3a033520` |
| 02 | `330e35021d15` |
| 03 | `03321e5f0d31` |
| 04 | `2f573c310b00` |
| 05 | `315352090227` |
| 06 | `081f020a1100` |
| 07 | `350150183d32` |
| 08 | `53150d3e2f1d` |
| 09 | `3d545e040a52` |
| 10 | `350905010050` |

Each chunk contains six bytes.

The sequence numbers must be used to reconstruct the original payload in the correct order.

---

## Step 4: Reconstruct and Decrypt the Payload

Join all ten hexadecimal chunks in sequence order.

The combined hexadecimal data is:

```text
335d3a033520330e35021d1503321e5f0d312f573c310b00315352090227081f020a1100350150183d3253150d3e2f1d3d545e040a52350905010050
```

### CyberChef Operations

![Base64 Decode](screenshots/02.png)

Open CyberChef and configure the following operations in order:

1. **From Hex**
2. **XOR**
   - Key: `foliage`
   - Key format: UTF-8
   - Repeat key: Enabled
3. **From Base64**

The XOR operation removes the encryption layer, and Base64 decoding reveals the final flag.

### Intermediate Base64 Output

After XOR decryption, the result is:

```text
U2VjTGVhZnttdWx0aXN0YWdlX25ldHdvcmtfZm9yZW5zaWNzX21hc3Rlcnl9
```

Now decode this string using Base64.

![Base64 Decode](screenshots/03.png)

## Final Flag

```text
SecLeaf{multistage_network_forensics_mastery}
```