# Hensel Garden – Cryptography Writeup

**Category:** Cryptography  
**Points:** 100  
**Flag:** `SecLeaf{r00ts_gr0w_through_pr1me_p0w3rs}`

## 1. Challenge Overview

Hensel Garden is a cryptography challenge in which a secret 128-bit seed is hidden behind two modular square equations.
The challenge provide one json file and one python file :

![Challenge Files](screenshots/01.png)

![Challenge Files](screenshots/02.png)

The challenge provides the following values:

```text
A = 2090995815874869393993
B = 246419994095244398264902
```

The secret seed `s` satisfies:

```text
(s + 87)^2 ≡ A (mod 2^72)

(s + 143)^2 ≡ B (mod 3^51)
```

The seed is a non-negative integer smaller than `2^128`.

An AES-GCM encrypted capsule is also provided. The encryption key is derived from the secret seed using SHA-256.

The objective is to recover the seed and decrypt the capsule to obtain the flag.

## 2. Understanding the Challenge

The main idea is that squaring a number modulo a prime power can produce multiple possible roots.

For example:

```text
7^2 = 49

49 mod 8 = 1
```

Similarly, other numbers such as 1, 3, and 5 also produce remainder 1 modulo 8.

This means that a modular square equation does not always have a single solution.

The challenge uses this property to hide the seed behind two different modular equations.

## 3. Recovering the Square Roots Using Hensel Lifting

Hensel lifting is a technique used to find solutions modulo increasingly large powers of a prime.

Instead of solving the entire equation at once, we begin with a small modulus and gradually increase it.

For the first equation:

```text
x^2 ≡ A (mod 2^72)
```

We start modulo 2, then continue modulo 4, 8, 16, and so on until reaching `2^72`.

At every stage, we extend the existing roots and retain only those satisfying the new equation.

Applying this process produces four roots modulo `2^72`:

```text
311693314961566273123
2049489926473256333725
2672876556396388879971
4410673167908078940573
```

The second equation is solved similarly:

```text
y^2 ≡ B (mod 3^51)
```

Starting modulo 3 and increasing the modulus up to `3^51` produces two roots:

```text
143629324417692064196608
2010064638657865702114139
```

Therefore, the challenge produces four roots for the first equation and two roots for the second.

## 4. Removing the Shifts

The recovered roots represent `s + 87` and `s + 143`, not the seed directly.

We subtract the respective shifts to obtain congruences for the seed.

For the correct first root:

```text
311693314961566273123 - 87

= 311693314961566273036
```

For the correct second root:

```text
143629324417692064196608 - 143

= 143629324417692064196465
```

The resulting congruences are:

```text
s ≡ 311693314961566273036
    (mod 2^72)

s ≡ 143629324417692064196465
    (mod 3^51)
```

## 5. Combining Both Clues Using CRT

The Chinese Remainder Theorem (CRT) allows us to combine two congruences with coprime moduli into a single solution.

The challenge uses moduli in json:

```text
m = 2^72
  = 4722366482869645213696

n = 3^51
  = 2153693963075557766310747
```

Since `m` and `n` are coprime, CRT can combine each pair of roots.

There are:

```text
4 × 2 = 8 possible combinations
```

The CRT formula is:

```text
s = a + m × ((b - a) × inverse(m, n) mod n)
```

The modular inverse is:

```text
inverse(m, n)
= 2005783915697921746635103
```

For the correct root pair, the CRT multiplier is:

```text
t = 59880982799651293
```

Therefore:

```text
s = 311693314961566273036
  + 4722366482869645213696
    × 59880982799651293
```

The recovered seed is:

```text
282779946134366997745983790016833981964
```

The remaining seven CRT candidates exceed the allowed 128-bit seed range.

This uniquely identifies the secret seed.

## 6. Verifying the Seed

The recovered seed satisfies both original equations:

```text
(seed + 87)^2 mod 2^72 = A

(seed + 143)^2 mod 3^51 = B
```

This confirms that the recovered seed is consistent with the challenge data.

## 7. Deriving the AES Key

The seed is converted into a 16-byte big-endian representation:

```text
d4bd6fc49311dd10e59d1a891c1b0e0c
```

The AES key is generated using SHA-256:

```text
SHA256(
    "SecLeaf/hensel/v2/" || seed_bytes
)
```

The resulting key is:

```text
c17e6cb58287b5d26bfc10183101fdfcd583ded77134de67fc4818d4659e0974
```

The prefix, byte order, and raw seed bytes are important. Any incorrect input would produce a different key.

## 8. AES-GCM Decryption

The challenge provides an AES-GCM capsule consisting of a nonce, ciphertext, and authentication tag.

The ciphertext is 40 bytes long, and the authentication tag is 16 bytes.

Using the derived AES key, the nonce, and the ciphertext concatenated with the tag, AES-GCM successfully decrypts and authenticates the capsule.

The successful authentication confirms that the recovered seed and key derivation are correct.

## 9. Final Flag

```text
SecLeaf{r00ts_gr0w_through_pr1me_p0w3rs}
```