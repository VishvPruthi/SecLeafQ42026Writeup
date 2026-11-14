# Fallen Leaf – Forensics Writeup

**Category:** Forensics  
**Flag:** `SecLeaf{d3l3t3d_k3ys_n3v3r_d13_th3_xattr_r3m3mb3rs}`

## 1. Introduction

The challenge provided a compressed disk image named `leafdisk.img.xz`. At first, it looked like a straightforward filesystem investigation because there was a `flag.txt` file in the user's Documents directory. However, the challenge was designed to mislead me with multiple fake flags and deleted evidence.

My goal was to investigate the filesystem, understand what happened before the evidence was deleted, and recover the actual flag.

## 2. Extracting and Examining the Disk Image

I first extracted the disk image:

```bash
xz -dk leafdisk.img.xz
```

Then I verified the file type:

```bash
file leafdisk.img
```
![FL](screenshots/01.png)
Since it was an ext4 filesystem image, I used `debugfs` to examine it without mounting it.

```bash
debugfs leafdisk.img
```

I listed the filesystem contents:

```bash
ls -la
```
![FL](screenshots/02.png)

I found the user's home directory:

```text
/home/leaf
```

Inside it, I noticed several interesting files and directories, including `Documents`, `.cache`, and shell history.

![FL](screenshots/03.png)

## 3. Investigating the First Flag

I checked the Documents directory and found `flag.txt`.

```bash
debugfs -R "cat /home/leaf/Documents/flag.txt" leafdisk.img
```
![FL](screenshots/05fakeflag.png)

The file contained:

```text
SecLeaf{fl4g_txt_1s_n0t_th3_fl4g}
```

This immediately looked suspicious because the flag itself suggested that it was not the real answer.

Instead of stopping there, I continued investigating.

## 4. Analyzing Bash History

The next important artifact was the user's Bash history.

```bash
debugfs -R "cat /home/leaf/.bash_history" leafdisk.img
```
![FL](screenshots/06.png)
The history revealed several interesting commands:

```bash
cat flag.txt
echo U2VjTGVhZntiNHNoX2gxc3QwcnlfbDEzc30= | base64 -d
cd ~/.cache
for f in k_*.txt; do gzip -N $f; done
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -salt \
-in harvest.txt -out Documents/harvest.enc \
-pass file:.cache/k_active
shred -u harvest.txt
rm -f .cache/k_*
history -c
```

The Base64 command caught my attention.

![FL](screenshots/07.png)

I decoded it:

Output:

```text
SecLeaf{b4sh_h1st0ry_l13s}
```

This was another decoy flag.

However, the remaining commands were much more interesting. They showed that the user had compressed encryption-key backups, encrypted a file named `harvest.txt`, securely deleted the original file, removed the key backups, and cleared the shell history.

This suggested that the actual evidence had been deliberately deleted.

## 5. Recovering the Deleted Encryption Keys

I examined the deleted inodes using:

```bash
debugfs -R "lsdel" leafdisk.img
```

Several deleted inodes appeared in the output.

![FL](screenshots/08.png)

I recovered the deleted key backups using their inode numbers:

```bash
debugfs -R "dump <24> k24.gz" leafdisk.img
debugfs -R "dump <25> k25.gz" leafdisk.img
debugfs -R "dump <26> k26.gz" leafdisk.img
debugfs -R "dump <27> k27.gz" leafdisk.img
```
![FL](screenshots/09.png)

I extracted the contents of the recovered files:

```bash
gzip -dc k24.gz
gzip -dc k25.gz
gzip -dc k26.gz
gzip -dc k27.gz
```

The recovered keys were:

```text
leafkey:Gr33n-Sapl1ng-77
leafkey:R00t-B4ll-Aut0mn-12
leafkey:Phl03m-X7lem-Fl0w-90
leafkey:C4mb1um-R1ng-2024
```
![FL](screenshots/10.png)

But I still needed to determine which key was actually used.


## 6. Decrypting harvest.enc

Next, I recovered the encrypted file:

```bash
debugfs -R "dump /home/leaf/Documents/harvest.enc harvest.enc" leafdisk.img
```

Using the recovered key, I decrypted it:

```bash
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 \
-in harvest.enc -out harvest.txt \
-pass pass:'Phl03m-X7lem-Fl0w-90'
```

After opening `harvest.txt`, I found another flag:

```text
SecLeaf{d3c0y_th3_tr33_h4s_n0_r00ts}
```
![FL](screenshots/12.png)

This was also a decoy.

However, the decrypted file contained a genuine flag fragment:

```text
d3l3t3d_k3ys_n3v3r_d13
```

## 8. Finding the Hidden Extended Attribute

I examined the extended attributes of `notes.txt`:

![FL](screenshots/13.png)

```bash
debugfs -R "ea_list /home/leaf/Documents/notes.txt" leafdisk.img
```

The output contained:

```text
user.leaf = L52GQM27PBQXI5DSL5ZDG3JTNVRDG4TT
```

The value looked like Base32-encoded data.

I decoded it:

```bash
echo 'L52GQM27PBQXI5DSL5ZDG3JTNVRDG4TT' | base32 -d
```

The output was:

```text
_th3_xattr_r3m3mb3rs
```

This was the missing part of the flag.

## 9. Reconstructing the Final Flag

At this point, I had recovered two genuine fragments:

From `harvest.txt`:

```text
d3l3t3d_k3ys_n3v3r_d13
```

From the extended attribute:

```text
_th3_xattr_r3m3mb3rs
```

Combining them with the flag prefix and suffix gave:

```text
SecLeaf{d3l3t3d_k3ys_n3v3r_d13_th3_xattr_r3m3mb3rs}
```

## 10. Final Flag

```text
SecLeaf{d3l3t3d_k3ys_n3v3r_d13_th3_xattr_r3m3mb3rs}
```