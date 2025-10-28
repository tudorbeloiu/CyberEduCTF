# Write-up: 
##  conv

**Category:** Cryptography
**Platform:** CyberEdu
**URL:** `https://app.cyber-edu.co/challenges/9d0ddf0e-c491-47f9-bf64-aa001e84059f`

---

After some time of analyzing the given code and using Stack Overflow, I found out that this code uses a mathematical operation called a `discrete convolution`

In simple terms(for guys like me), this function is performing a `polynomial multiplication`.

Think of `plain1` and `key` as 2 polynoms, where each byte is a coefficient:

# plain1 = p[0], p[1], p[2]... => P(x) = p[0] + p[1]*x + p[2]*x*x ...
# key = k[0], k[1]... => K(x) = k[0] + k[0]*x + ...

conv(plain1,key) calculates `C(x) = P(x) * K(x)`.

`res[i] = csum % 256` means all the math is done modulo 256(finite ring)

We already have the cip : `17c080c00398a06e4661e403b2b571b578221bba83e235a0feece7213ad4d65c1d89c2a3afae5ef91bf7f2181f0c797505b7bd55c62d1edf2614b17f88f85eac674fbd6d7be4e2a617605c68e1baf8603cb9b1d32b2bc1ab60d8c62b20be0bc0fb73a546b5641988a3bf8eeb778731e048970308d941a8bd5f6cb56159069364c93b5429afdb85f9dfb5f5b0ca44d314af68bc9d56b39321fe5cc072c9508978693ee60a9bffff5b52f6aa0ca37f9b421eb402a4886b742570926b7479d2b89528caceb7121a338c233164c33a120b9813bc56b855c914124ecb30df3d4a14c92788faa7c9e32b544e24d9d9fe2a5539a280c28466dc6b276ba4b089fa26f8bace95f43f6c5d491e14e5fa09a853fff2dfd73a8cf8d7b54d3d8d693db7b182789f47e343e9cf56f8663e181a1e98276aface8b1052e3ee9c6630d69ad479bfe1106ec1ab585a030ca130a6d849f9c4bed9d0b16f46890f1efa66c8f21f078088f426ef0e1f9af315ae3b2356123df174bb4095ad2361237bedc3e62c294f8ccc135f9766f0ec2a462087cd2648`

To find `plain1`, I have to reverse the operation : DIVISION.
plain1 = (cip/key) % 256

This operation is called `deconvolution`.

I found some big help online with this script(I was not the best at algebra), and I got the flag:


![flag.jpg](img/flag.jpg)

(the solving code is in solve.py)