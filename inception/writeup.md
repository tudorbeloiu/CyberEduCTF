# Write-up

**Category:** Misc
**Platform:** CyberEdu
**URL:** `https://app.cyber-edu.co/challenges/55bee840-7f21-11ea-9848-99f815545ba1`
---

This was an easy challenge that tested my knowledge about multiple layers (a file that hides another file in their data).

We were given a `.zip` archive. First we find out details about it:

![zipdetail.png](/img/zipdetail.png)

We extract the archive and we now have another file to work with, `chall.jpeg`, and we run again the `file` command, this time on the new file:

![challdetail.png](/img/challdetail.png)

Given the challenge name "Inception" and its category being "Misc", we try to find hidden files inside `chall.jpeg`. For this task, we use the `binwalk` command. This tool scans the file for other files:

![binwalk.png](/img/binwalk.png)

Ok, we got a lot of information from this. At starting offset (`0x0`), we have normal JPEG data, but buried at the end of the file, at offset `0x1B16B`, a `.png` file is present.
> `110955        0x1B16B         PNG image, 400 x 400, 1-bit colormap, non-interlaced`

Now, let's analyze this PNG. We use again the `binwalk` command but with `-e` flag that stands for `--extract`:

![binwalke.png](/img/binwalke.png)

In the new extracted directory, we find 2 files:

![lsl_chall.png](/img/lsl_chall.png)

We again use the `file` command:

![file1b1a6.png](/img/file1b1a6.png)

But we find out that `binwalk -e` failed to extract the `.png` file (that's why the WARNING message appeared before).

## Let's try another approach

We get back in the directory that contains `chall.jpeg` and we manually extract the `.png` file using the `dd` command:

```bash
dd if=chall.jpeg of=next_chall.png bs=1 skip=110955
```
>

```bash
    if = chall.jpeg -> input file
    of = next_chall.png -> output file
    bs = 1 -> set the block syze to 1 byte
    skip = 110955 -> skips the first 110955 bytes(the offset we found)
```

![dd.png](/img/dd.png)
   
We don't need to use `zsteg`, `steghide`, `stegseek` or any other commands common in steganography challenges, beceause when we take a look in the directory after the extraction we can clearly see that our .png file contains a qr code!

![qrcode.png](/img/qrcode.png)
  

Now, we only have to read the qr code and for this particular task we use the `zbarimg` tool.
> 
```bash
zbarimg next_chall.png
```
## This command will scan the image, detect the qr code and output the text that it contains.
    
![zbarimg.jpg](/img/zbarimg.jpg)
    
And we got the flag!
