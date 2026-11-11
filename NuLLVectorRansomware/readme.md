# NullVector Ransomware – CTF Writeup

**Points:** 150  
**Challenge:** NullVector Ransomware – QS01 Incident Log #892

## 1. Introduction

In this challenge, we were given an encrypted file named `classified_report.locked` and a JSON file containing RSA factorization information.

The goal was to recover the original report and find the hidden flag.

At first, the encrypted file looked like a normal ransomware-encrypted document. However, after examining the challenge details, I found that it used multiple encryption and data transformation techniques.

## 2. Understanding the Challenge

The challenge involved three main stages:

1. RSA-2048 – Used to protect the AES encryption key.
2. AES-256-CBC – Used to encrypt the actual report.
3. Custom XOR and bit rotation – Used to transform the data further.

This meant that decrypting the AES ciphertext alone would not be enough to recover the original report.

## 3. Inspecting the Encrypted File

I started by examining `classified_report.locked` using a hex editor.

The file was 886 bytes in size.

After understanding its structure, I identified four sections:

| Offset | Size | Description |
|---|---:|---|
| 0 | 6 bytes | File header |
| 6 | 256 bytes | RSA-encrypted AES key |
| 262 | 16 bytes | AES initialization vector |
| 278 | 608 bytes | AES ciphertext |

This helped identify which parts of the file needed to be processed separately.

One important observation was that the RSA modulus was not embedded in the encrypted file. It was provided in the factorization JSON.

## 4. Recovering the RSA Private Key

The JSON file provided the following RSA values:

- `N` – RSA modulus
- `e` – Public exponent
- `p` – First prime factor
- `q` – Second prime factor

Since both prime factors were available, I could reconstruct the RSA private exponent.

First, calculate Euler's totient:

\[
\phi(N)=(p-1)(q-1)
\]

Then calculate the private exponent:

\[
d=e^{-1}\pmod{\phi(N)}
\]

With the private exponent and modulus available, the RSA-encrypted data could be decrypted.

## 5. Recovering the AES Key

The RSA ciphertext was extracted from bytes 6 to 261.

Using textbook RSA decryption:

\[
m=c^d\bmod N
\]

The resulting message was represented as a 256-byte value.

The actual AES key was stored in the last 32 bytes of this value.

Recovered AES key:

```text
078440dd9f8c28d0a8e90f37efd987f736e67023762a2bfbe32cbac9d7afa8d7
```

## 6. Decrypting the AES Data

Next, I extracted the AES initialization vector and ciphertext.

- AES key: Recovered from RSA decryption
- IV: Bytes 262–277
- Ciphertext: Bytes 278–885
- Mode: AES-256-CBC

After applying AES-CBC decryption and removing PKCS#7 padding, the output was still unreadable.

This indicated that another transformation had been applied to the data.

## 7. Reversing the Custom Transformation

The challenge used a custom operation involving XOR and bit rotation.

The encryption formula was:

\[
c[i]=ROR8(p[i]\oplus((i\times13+0x7A)\bmod256),3)
\]

To recover the original data, I reversed the operations:

\[
p[i]=ROL8(c[i],3)\oplus((i\times13+0x7A)\bmod256)
\]

The process involved:

1. Rotating each byte left by 3 bits.
2. Calculating the position-dependent XOR value.
3. Applying XOR to recover the original byte.
4. Repeating the process for every byte, starting from index zero.

After reversing this transformation, the original report became readable.

## 8. Flag

The recovered report contained the master asset key:

```text
SecLeaf{e4d90b218a754f1c93206e58b1f4a7c2}
```

## 9. What I Learned

This challenge helped me understand:

- How RSA encryption can protect an AES key.
- How prime factorization information can be used to reconstruct an RSA private key.
- How AES-CBC encryption works.
- Why an IV is required for AES-CBC decryption.
- How XOR and bit rotation transformations can be reversed.
- Why understanding the file structure is important when analyzing encrypted files.

## Conclusion

The main challenge was not just decrypting the AES data, but understanding the complete encryption process.

By analyzing the file structure, reconstructing the RSA private key, recovering the AES key, and reversing the custom transformation, the original report and flag could be recovered.

**Challenge solved!** 🔐