# Write-up: CyberEdu - Format String 101

**Category:** pwn (Binary Exploitation)
**Platform:** CyberEdu
**URL:** `https://app.cyber-edu.co/challenges/08ef6340-c1e4-11eb-9b9f-6bd8e9c6de87/`

---

## 1. Initial Analysis (Static Analysis)

The binary analysis started by running the `file` command to determine its properties:

![File command output](img/filedesc.png)

From the output, I extracted the following critical information:

* **`ELF 32-bit`**: This is a **32-bit** binary. All addresses and pointers will be 4 bytes long. The registers of interest will be `EBP`, `ESP`, `EIP`.
* **`LSB (Least Significant Byte)`**: The binary is **Little-Endian**. This is crucial information for building the payload, as addresses (e.g., `0x0804a030`) must be written into memory with their bytes reversed (`\x30\xa0\x04\x08`).
* **`not stripped`**: The binary is **not stripped**. This is a major bonus, as the symbol table is intact. This makes the analysis in Ghidra much easier, allowing us to see clear function names like `main` and `printFlag`.

---

## 2. Dynamic Analysis and Ghidra

On the first run, the program gives us a valuable clue: the exact address of the variable we need to modify.

![Initial program run](img/rulare.png)

The program informs us: `"Value to break is at 0x0804a030 and has a hex value 0x0000000a"`.

Next, I opened the binary in Ghidra to analyze the program's logic.

### The `main` Function

![Decompiled `main` function](img/main.png)

Analyzing the `main` function, we observe the following flow:
1.  User input is read into `local_e8` using `fgets`.
2.  A prefix (`"Break stuff.  "`) is copied into `local_1b0`.
3.  Our input (`local_e8`) is concatenated to `local_1b0` using `strlcat`.
4.  **🚨 Vulnerability:** `printf(local_1b0)` is called. Since we control the contents of `local_1b0`, this is a classic **Format String Vulnerability**.
5.  **🎯 Objective:** The program checks if `demo.3187` (the variable at `0x0804a030`) is equal to `0x20`. If so, it calls `printFlag()`.

### The `printFlag` Function

![Decompiled `printFlag` function](img/printflag.png)

The `printFlag` function is simple: it executes an `execve` syscall to run `/usr/bin/cat flag.txt`, thus displaying the flag's content.

---

## 3. Debugging and Payload Construction

The goal is clear: use the format string vulnerability to write the value `0x20` to the address `0x0804a030`.

### Finding the Offset (`N`)

I started the program in GDB and set a breakpoint just before the vulnerable `printf` call.

![Assembly code for printf](img/memorie.png)

Upon hitting the breakpoint, I inspected the stack (`x/20wx $esp`) to see where our buffer was located:

![Inspecting the stack in GDB](img/stiva.png)

We can see that our buffer (`local_1b0`) starts at address `0xffffcc70`, which corresponds to the **4th argument** (`Arg 4`) on the stack. This is our *base offset*.

> **How the attack works:**
> The `%n` specifier writes the number of bytes printed so far to an address specified by an argument on the stack. By using a positional specifier (e.g., `%8$n`), we can tell `printf` which argument to look at to find the address to write to.

### Aligning the Payload

Now we need to place our target address (`0x0804a030`) on the stack, at an aligned location (a multiple of 4 bytes) relative to our base (`Arg 4`).

1.  The prefix `"Break stuff.  "` is **14 bytes** long (including the two trailing spaces).
2.  To align our address on a 4-byte boundary (16), we need to add **2 bytes of padding** (e.g., `\x90\x90`).
3.  We place our target address (`\x30\xa0\x04\x08`) immediately after.

I checked the new stack structure in GDB:

![Address alignment on the stack](img/corect.png)

Perfect. Our address `0x0804a030` is now placed at `0xffffcc80`.

Let's calculate the final index `N`:
* **Base:** `Arg 4` (at address `0xffffcc70`)
* **Address Offset:** `0xffffcc80 - 0xffffcc70 = 0x10` (16 bytes)
* **Argument Offset:** $16 \text{ bytes} / 4 \text{ bytes/arg} = 4$
* **Final Index `N`:** $4 \text{ (Base)} + 4 \text{ (Offset)} = \textbf{8}$

We will use **`%8$n`** to tell `printf` to write to the address found at the 8th argument.

---

## 4. Final Payload and Local Testing

The last step is to make sure `printf` prints *exactly* `0x20` (32) characters before it encounters our `%8$n`.

Character count:
* **Prefix:** 14 characters (`"Break stuff.  "`)
* **Alignment Padding:** 2 characters (`\x90\x90`)
* **Address:** 4 characters (treated as text by `printf`)
* **Total so far:** $14 + 2 + 4 = 20$ characters.
* **Counting Padding:** $32 \text{ (target)} - 20 \text{ (current)} = \textbf{12}$ characters (e.g., `A` * 12).

The final payload becomes:

```python
payload = (
    b"\x90" * 2 +          # 2 bytes of alignment padding
    b"\x30\xa0\x04\x08" +  # Target address (little-endian)
    b"A" * 12 +           # 12 bytes of counting padding (32 total)
    b"%8$n"               # Write specifier for Arg 8
)
