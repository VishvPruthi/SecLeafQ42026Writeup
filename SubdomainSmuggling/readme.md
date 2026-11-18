# Subdomain Smuggling – Full Writeup

**Category:** Network  
**Points:** 100  
**Flag:** `SecLeaf{D474_3xf1l_DN5}`

## 1. Challenge

First, I opened the PCAP file in Wireshark.

The capture contained normal TCP traffic along with DNS communication. Since the challenge mentioned that the attacker used a core network protocol to leak data, I decided to investigate DNS traffic.

This revealed four suspicious DNS queries originating from the workstation `192.168.1.20`.

| Frame | DNS Query |
|---:|---|
| 167 | `U2VjTGVhZn.evil.com` |
| 293 | `tENDc0XzN4.evil.com` |
| 395 | `ZjFsX0RONX.evil.com` |
| 502 | `0=.evil.com` |

The leftmost labels appeared to contain encoded information. Since all four queries shared the same domain suffix, I suspected that the attacker had divided the data into multiple DNS subdomain fragments.

![Suspicious DNS Queries](screenshots/01.png)

![Suspicious DNS Queries](screenshots/02.png)

![Suspicious DNS Queries](screenshots/03.png)

![Suspicious DNS Queries](screenshots/04.png)

I copied the leftmost labels from the suspicious DNS queries and arranged them according to their packet frame numbers.

The extracted fragments were:

```text
U2VjTGVhZn
tENDc0XzN4
ZjFsX0RONX
0=
```

Since the fragments were transmitted in different DNS requests, I concatenated them in their original order.

```text
U2VjTGVhZntENDc0XzN4ZjFsX0RONX0=
```

The resulting string appeared to be Base64 encoded.

![Suspicious DNS Queries](screenshots/05.png)

```text
SecLeaf{D474_3xf1l_DN5}
```

This confirmed that the suspicious DNS queries contained the hidden challenge flag.

## Final Flag

```text
SecLeaf{D474_3xf1l_DN5}
```
## 8. Conclusion

This challenge demonstrated how DNS can be abused as a covert communication channel to exfiltrate information.

The attacker encoded data into DNS subdomain labels and transmitted the fragments through ordinary DNS requests. By filtering suspicious queries, preserving their original order and capitalization, and decoding the reconstructed Base64 payload, I successfully recovered the flag.

The challenge highlighted the importance of monitoring DNS traffic and identifying unusual domain patterns, especially when conventional data transfer methods are absent.

### Key Learnings

- DNS queries can carry hidden data inside subdomain labels.
- Filtering DNS requests avoids duplicate fragments from responses.
- Packet order and capitalization are important during payload reconstruction.
- Base64 fragments must be combined before decoding.
- Wireshark and Linux terminal utilities are useful tools for DNS traffic analysis.

**Challenge Solved:** `SecLeaf{D474_3xf1l_DN5}`
