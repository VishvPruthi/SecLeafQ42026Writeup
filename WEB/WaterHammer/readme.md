# 🔐 SecLeaf CTF Writeup – Water Hammer

| Details | Information |
|---|---|
| Platform | SecLeaf |
| Category | Web Exploitation |
| Challenge | Water Hammer |
| Points | 100 |
| Vulnerability | Race Condition |
| Tool | Burp Suite Repeater |

![Challenge Overview](screenshots/challenge.png)

## 📌 Challenge Overview

The challenge was based on a water customer portal called Hollow Creek.

Every account starts with **100 litres** of quota. Customers can claim a one-time goodwill voucher worth 50 litres, while opening the Reserve Valve costs 1,000 litres.

The objective was to collect enough quota to open the valve and retrieve the flag.


## 🔍 1. Initial Reconnaissance

I explored the customer portal and noticed the following:

- Starting quota: 100 litres
- Goodwill voucher: 50 litres (one-time use)
- Reserve Valve: 1,000 litres

I first tried redeeming the voucher normally. After it was claimed, another redemption attempt returned:

```json
{
  "error": "Voucher already claimed.",
  "ok": false
}
```

So, a normal request wasn't going to be enough.

![Challenge Overview](screenshots/01-challenge.png)

## ⚡ 2. Finding the Race Condition

I intercepted the voucher redemption request using Burp Suite.

The endpoint was:

```http
POST /voucher/redeem HTTP/1.1
```

I sent the request to Burp Repeater and created a group of multiple requests.

Instead of sending them one by one, I used **Send group (parallel)** to execute them simultaneously.

![Burp Suite Parallel Requests](screenshots/02-burp-parallel.png)

## 🚀 3. Exploitation

I sent 20 requests in parallel.

The idea was to exploit a possible race condition where multiple requests could pass the voucher validation before the server updated the claimed status.

Some requests returned successful responses, while others returned:

```json
{
  "error": "Voucher already claimed.",
  "ok": false
}
```

The successful requests credited additional litres to my account.

After the parallel execution, my quota increased to **1,100 litres**!

![Quota Increased](screenshots/03-quota-1100.png)

## 🚩 4. Opening the Reserve Valve

With 1,100 litres available, I clicked the **Open valve** button.

The portal deducted 1,000 litres and successfully opened the Reserve Valve.

The flag was displayed on the screen.

![Reserve Valve Opened](screenshots/04-flag.png)

## 🏁 Flag

```text
SecLeaf{ch3ck_f1r5t_wr1t3_14t3r_b00m}
```

## 💡 What I Learned

This challenge helped me understand how race conditions can affect applications that handle one-time operations.

Sending multiple requests simultaneously can expose problems when validation and state updates are not handled atomically.

**Key takeaway:** Always consider race conditions when testing operations involving payments, vouchers, rewards, or limited-use actions.

---

*Happy Hacking! 🔐*