# Blackout Protocol – SecLeaf CTF 2026

**Category:** Reverse Engineering  
**Event:** SecLeaf Q4 CTF 2026  
**Points:** 500  

## 1. Challenge Overview

Blackout Protocol was an interesting challenge that combined network forensics, memory analysis, and reverse engineering.

We were provided with four files:

| File | Description |
|---|---|
| `blackout_protocol` | Verification executable |
| `transmission.pcap` | Network traffic capture |
| `incident.journal` | Binary incident records |
| `retained.mem` | Memory dump containing key material |

The main objective was to investigate the evidence, recover the required transformation parameters, and understand how the executable validates the final input.

## 2. Initial File Analysis

I started by extracting the challenge archive and identifying the provided files.

The executable was a Linux ELF 64-bit binary, while the other three files contained network, journal, and memory evidence.

![Challenge files](screenshots/01-challenge-files.png)

## 3. Network Traffic Analysis

**Tool: Wireshark**

I opened `transmission.pcap` in Wireshark to investigate the captured network traffic.

The capture contained 290 packets, primarily UDP traffic.

The application used a custom protocol identified by the magic bytes `BKP5`.

Instead of treating every packet as useful, I focused on identifying packets belonging to the custom protocol and filtering out unrelated traffic.

The investigation involved checking:

- UDP destination ports.
- Protocol identifiers.
- Protocol tag values.
- Source IP addresses.
- Record indexes and packet checksums.

According to the challenge analysis, 32 genuine packets were identified from the original 290 packets.

These packets contributed 12 bytes each, giving a total of 384 bytes used to reconstruct a lookup table.

![BKP5 packet inspection](screenshots/bkp5.png)

## 4. Memory Dump Analysis

**Tool: HxD Hex Editor**

Next, I inspected `retained.mem` using HxD.

The memory dump contained a recognizable header:

```text
M16B
```

This helped identify the relevant structure inside the binary file.

Two important 64-bit values were recovered:

```text
A = 0x72f23b4a1c67cd00
B = 0xabfedf0984f04e18
```

These values were combined using XOR:

```text
A XOR B = 0xd90ce44398978318
```

The resulting value was used as memory key material during reconstruction.

The memory dump also contained a 512-byte region at offsets `0x600–0x7FF`, which was relevant to the verifier's lookup-table construction.

![Memory header](screenshots/05-memory-header.png)

![Memory seed values](screenshots/06-memory-seeds.png)

## 5. Incident Journal Analysis

The next file was `incident.journal`.

It contained:

- Magic identifier: `JRN4`
- Total records: 224
- Record size: 24 bytes

Not all records were genuine. The records needed to be checked using their FNV-1a checksums and unique indexes.

The checksum algorithm used was FNV-1a 32-bit:

```python
def fnv1a_32(data):
    h = 0x811c9dc5

    for byte in data:
        h ^= byte
        h = (h * 0x01000193) & 0xffffffff

    return h
```

After checksum validation and duplicate-index filtering, 48 authentic and uniquely indexed records remained.

These records provided additional information required for reconstructing the transformation parameters.

![Journal structure](screenshots/07-journal-structure.png)

## 6. Reverse Engineering the Executable

**Tool: Ghidra**

After examining the supporting evidence, the next step was understanding the verification executable.

The binary was stripped, so its original function names were unavailable.

The validation logic used a custom 52-round transformation.

The transformation consisted of several stages:

1. S-box substitution.
2. Byte permutation.
3. Forward diffusion.
4. Reverse diffusion.
5. Additional periodic operations.

The S-box was 256 bytes long and was used for byte substitution.

The transformation was reversible once its parameters were reconstructed. The recovery process required reversing the operations in the opposite order.


## 7. Combining the Evidence

The important part of this challenge was understanding how the four files were connected.

| Evidence | Information recovered |
|---|---|
| `retained.mem` | Header and seed material |
| `incident.journal` | 48 validated records |
| `transmission.pcap` | 32 genuine packets |
| `blackout_protocol` | Verification and transformation logic |

The journal and network data were used to reconstruct the parameters required by the executable.

The recovered candidate was then checked against the original verifier.

## 8. Flag Verification

The challenge used the original executable as the final authority.

The recovered candidate was:

```text
SecLeaf{n01s3_1n_th3_w1r35_4nd_4ft3r1m4g3s!!!!!}
```

The verification command on Linux was:

```bash
./blackout_protocol 'SecLeaf{n01s3_1n_th3_w1r35_4nd_4ft3r1m4g3s!!!!!}'
```

The expected successful response was:

```text
Authenticated.
```

## 9. Final Flag

```text
SecLeaf{n01s3_1n_th3_w1r35_4nd_4ft3r1m4g3s!!!!!}
```

## 10. Key Learnings

This challenge helped me understand several important concepts:

- Investigating custom UDP protocols in Wireshark.
- Identifying useful network packets among unrelated traffic.
- Inspecting binary memory dumps using a hex editor.
- Understanding FNV-1a checksums.
- Reconstructing data from multiple evidence sources.
- Understanding S-boxes, permutations, and diffusion.
- Reverse engineering stripped ELF binaries.
- Validating a recovered input using the original executable.

**Conclusion:** Blackout Protocol was a good example of how network traffic, memory artifacts, and reverse engineering can work together in a single forensic investigation.