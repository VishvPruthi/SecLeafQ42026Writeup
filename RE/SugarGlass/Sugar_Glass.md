# Sugar Glass — Reverse Engineering Writeup

**Category:** Reverse Engineering  
**Flag:** `SecLeaf{gl455_h0ld5_4_53cr3t}`

---

## 1. Challenge Overview

The challenge provided a stripped 64-bit ELF executable named `sugar_glass`. The program accepted user input and printed either `Filed.` or `Rejected.` depending on whether the input passed its validation routine.

The objective was to understand the validation logic, reverse the byte transformations, recover the expected 29-character input, and verify it against the original executable.

## 2. Binary Reconnaissance

I first identified the executable format:

```bash
file sugar_glass
```

The output confirmed that it was a 64-bit x86-64 ELF, PIE executable, dynamically linked, and stripped.

![Challenge files](screenshots/01.png)

I made it executable and checked its readable strings:

```bash
chmod +x sugar_glass
strings -n 4 sugar_glass
```

Some useful strings were:

```text
fgets
strlen
strcspn
strncpy
Filed.
Rejected.
SGR2
```
![Challenge files](screenshots/02.png)

These strings suggested that the program reads input, processes a string, and then checks it against some validation logic. The `Filed.` and `Rejected.` messages provided clear success and failure indicators.

## 3. Static Analysis

I used `objdump` to inspect the assembly:

```bash
objdump -d -M intel sugar_glass | less
```

The relevant code was identified around:

- `main()` at `0x1090`
- The validation routine at `0x1230`

I examined the validation routine more closely:

```bash
objdump -d -M intel \
  --start-address=0x1230 \
  --stop-address=0x1400 \
  sugar_glass
```
![Challenge files](screenshots/03.png)

The validator checks the input length and then processes the input byte by byte. It uses arithmetic, XOR, and circular rotations before comparing the results against an embedded validation table.

## 4. Extracting the Embedded Data

I inspected the read-only data section:

```bash
objdump -s -j .rodata sugar_glass
```

The `SGR2` marker was followed by challenge parameters and byte arrays used by the validation routine.

![Challenge files](screenshots/04.png)

The important values identified were:

| Parameter | Value |
|---|---:|
| Required input length | 29 bytes |
| Position increment | 11 |
| Initial position seed | `0x05` |
| Initial byte state | `0x42` |
| Initial secondary state | `0x39` |
| Initial accumulator | `0x5D` |

The ciphertext and validation table were also located in the data section.

## 5. Understanding the Validation Logic

The validation routine processes the input in a scrambled order rather than from the first character to the last.

The input position is calculated using a changing index and modulo 29. The position increment of 11 causes the validator to visit different input positions during each iteration.

For each byte, the program performs operations involving:

1. XOR with a ciphertext byte.
2. Addition of the current state.
3. An 8-bit circular left rotation by 3.
4. XOR with a secondary state.
5. An 8-bit circular left rotation by 1.
6. Accumulator update.
7. Comparison with the validation table.

If a comparison fails, the program rejects the input.

## 6. Reversing the Transformation

Instead of guessing the entire input, I used the validation table to determine the required transformed value for each iteration.

The important operations can be reversed:

| Forward operation | Reverse operation |
|---|---|
| `ROL8(value, 1)` | `ROR8(value, 1)` |
| XOR with a known value | XOR with the same value |
| Addition | Subtraction |
| `ROL8(value, 3)` | `ROR8(value, 3)` |

The accumulator was used to calculate the required byte contribution. I then reversed the rotations, XOR, and addition to recover the original input character.

Because the positions were scrambled, each recovered character was placed into its original position rather than appended directly to the flag.

## 7. Developing the Solver

I used Python to automate the repeated calculations.

The rotate-left function was:

```python
def rol8(x, n):
    x &= 0xff
    return ((x << n) | (x >> (8 - n))) & 0xff
```

The corresponding rotate-right function was:

```python
def ror8(x, n):
    x &= 0xff
    return ((x >> n) | (x << (8 - n))) & 0xff
```

These functions reproduce the 8-bit circular rotations used by the binary.

The solver follows the validation routine, reverses the transformations, and stores each recovered character at its correct scrambled position.

![Challenge files](screenshots/05.png)

## 8. Recovering the Flag

After reversing the validation logic and recovering the characters, the expected input was:

```text
SecLeaf{gl455_h0ld5_4_53cr3t}
```

## 9. Flag Verification

I tested the recovered input against the original executable:

```bash
echo "SecLeaf{gl455_h0ld5_4_53cr3t}" | ./sugar_glass
```

The program returned:

```text
Filed.
```
![Challenge files](screenshots/06.png)

This confirmed that the recovered flag was accepted by the original binary.

## 10. Final Flag

```text
SecLeaf{gl455_h0ld5_4_53cr3t}
```

## 11. Key Takeaways

- Identifying ELF executables using `file`.
- Finding useful strings using `strings`.
- Inspecting stripped binaries with `objdump`.
- Understanding registers and assembly instructions.
- Recognizing XOR, addition, and circular rotations.
- Reversing byte transformations.
- Understanding scrambled input positions.
- Automating repetitive calculations using Python.
- Verifying the recovered flag against the original executable.

---