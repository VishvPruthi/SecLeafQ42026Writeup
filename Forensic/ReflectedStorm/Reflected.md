# 🌐 Reflected Storm – Network Forensics CTF Writeup

**Category:** Network Forensics  
**Tool Used:** Wireshark  
**Challenge:** Reflected Storm

## 1. Introduction

In this challenge, I was given a PCAP file named `reflected-storm.pcap`.

The objective was to analyze the captured network traffic, identify the IP address receiving amplified DNS responses, and determine the number of DNS servers involved in the attack.

## 2. Tools Used

- Wireshark

## 3. Investigation

### Step 1: Opening the PCAP File

I started by opening `reflected-storm.pcap` in Wireshark.

To focus on DNS communication, I applied the following display filter:

```text
dns
```

This allowed me to examine DNS queries and responses separately from other network traffic.

**Screenshot 1 – DNS Traffic in Wireshark**

![DNS Traffic](screenshots/01dns.png)

### Step 2: Identifying Suspicious DNS Queries

While examining the DNS packets, I looked for unusual query types.

I noticed DNS queries using the `ANY (255)` record type, which requests available DNS information for a domain.

I applied this filter:

```text
dns.flags.response == 0 && dns.qry.type == 255
```

After inspecting the packet details, I identified the queried domain:

```text
openresolver-test.example.com
```

**Screenshot 2 – DNS ANY Query Details**

![DNS ANY Query](screenshots/02any.png)

### Step 3: Identifying the Victim IP

Next, I examined the DNS responses to determine where the traffic was being sent.

I applied the following filter:

```text
dns.flags.response == 1 && udp.srcport == 53
```

I checked the Destination column and noticed that multiple DNS responses from different external servers were directed towards the same IP address.

The victim IP was:

```text
10.0.55.200
```

**Screenshot 3 – Identifying the Victim IP**

![Victim IP](screenshots/03-victim-ip.png)

### Step 4: Identifying the DNS Reflectors

After identifying the victim, I filtered the DNS responses directed towards that IP:

```text
ip.dst == 10.0.55.200 && udp.srcport == 53
```

I examined the Source column and identified the unique DNS server addresses.

The five reflectors were:

```text
198.51.100.22
203.0.113.5
192.0.2.17
198.51.100.10
203.0.113.88
```

I counted unique source IP addresses rather than the total number of response packets.

**Total DNS Reflectors: 5**


## 4. Final Findings

| Parameter | Result |
|---|---|
| Victim IP | `10.0.55.200` |
| Number of Reflectors | 5 |
| Queried Domain | `openresolver-test.example.com` |
| Query Type | ANY (255) |
| Attack Type | DNS Reflection / Amplification |

## 5. Understanding the Attack

The captured traffic indicated a DNS reflection and amplification attack.

The attacker sent DNS requests using the victim's IP address as the spoofed source address.

The DNS servers responded to the victim instead of the original sender.

Since the DNS responses were significantly larger than the original requests, this resulted in amplified traffic reaching the victim.

## 6. Flag

After identifying the victim IP and counting the unique DNS reflectors, I constructed the flag using the required format.

```text
FLOWTRIQ{10.0.55.200_5_reflectors}
```

## 7. What I Learned

- Analyzing PCAP files using Wireshark.
- Filtering DNS queries and responses.
- Understanding DNS ANY queries.
- Identifying IP spoofing.
- Recognizing DNS reflection and amplification attacks.
- Counting unique source IP addresses to identify reflectors.

## Conclusion

This challenge helped me understand how DNS reflection and amplification attacks can be identified through network traffic analysis.

By examining DNS queries, response destinations, and unique source IP addresses, I was able to identify the victim and determine the number of DNS reflectors involved.

**Challenge Solved! 🔐**