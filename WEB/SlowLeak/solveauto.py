import requests

url = "http://web.secleaf.xyz:8080/"
s = requests.Session()

flag = {}

print("[*] Collecting flag characters...")

while len(flag) < 40:
    r = s.get(url)

    char = r.headers.get("X-Drip")
    serial = r.headers.get("X-Drip-Serial")

    if char and serial:
        pos = int(serial.split("/")[0])

        if pos not in flag:
            flag[pos] = char
            print(f"[+] {serial} : {char}")

print("\n[+] FLAG:")
print("".join(flag[i] for i in range(1, 41)))

s.close()