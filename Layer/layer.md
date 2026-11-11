# LAYERS CTF Writeup

## Introduction

The challenge provided a ZIP file named `Binary_Data.zip`. At first, the contents looked like random binary data. Instead of trying to decode everything at once, I inspected the file and followed each layer step by step.

The challenge involved binary conversion, ROT13, hexadecimal decoding, an encrypted RAR archive, and ROT47.

## Step 1: Extracting the ZIP File

I started by extracting `Binary_Data.zip` using 7-Zip.

After extraction, I found a file named `Binary_Data`. I opened it in a text editor and noticed that it contained binary data 0 and 1.

## Step 2: Converting Binary to ASCII

The file contained binary digits. I used CyberChef and selected the **From Binary** operation.

I configured it to use 8-bit groups because one byte contains 8 bits.

After decoding, the output became readable ASCII text.

**Screenshot 2 – Binary to ASCII conversion**

![Binary to ASCII](screenshots/01.png)

## Step 3: Applying ROT13

The decoded output contained characters from `0-9` and `n-s`.

This looked unusual, so I tried the ROT13 cipher.

After applying ROT13, the letters changed into hexadecimal characters (`a-f`), while the digits remained unchanged.

This revealed a long hexadecimal string.

**Screenshot 3 – ROT13 decoding**

![ROT13 output](screenshots/02.png)

## Step 4: Converting Hexadecimal to a RAR File

The next step was to decode the hexadecimal string into raw bytes.

I used CyberChef's **From Hex** operation.

The output started with the bytes:

`52 61 72 21 1A 07 01 00`

These bytes matched the RAR file signature. This indicated that the decoded data was actually a RAR archive.

I saved the binary output as `archive.rar`.

**Screenshot 4 – Hex to RAR conversion**

![Hexadecimal to RAR](screenshots/02.png)

## Step 5: Extracting the Encrypted RAR Archive

I opened `archive.rar` using 7-Zip.

The archive was password-protected. 
So, I bruteforce the RAR file and found the password in rockyou file
Using the recovered password:

`stormstorm`

I extracted the archive successfully and found a file named `Text`.

**Screenshot 6 – Extracted Text file**

![Extracted Text file](screenshots/03.png)

## Step 6: Applying ROT47

I opened the extracted `Text` file and found another encoded string.

I suspected that another substitution cipher was being used, so I tried ROT47 in CyberChef.

The output revealed the final flag:

`F1n4lLy_YOu_G0t_1T_!^!`

**Screenshot 7 – ROT47 decoding and final flag**

![Final flag](screenshots/04.png)

## Final Flag

```text
F1n4lLy_YOu_G0t_1T_!^!
```

## Conclusion

This challenge was interesting because the data was hidden behind multiple encoding layers. The important part was identifying the format at each stage instead of randomly trying different methods.

The main techniques used were:

- Binary to ASCII conversion
- ROT13 decoding
- Hexadecimal decoding
- RAR5 archive identification
- Password-protected archive extraction
- ROT47 decoding

Overall, this challenge helped me understand how multiple encoding and encryption layers can be combined to hide data.