# The Pow-XOR Equivalence Problem

I stumbled upon a weird math problem recently. This repository documents my initial approach at tackling the problem.

It's entirely possible that I am missing something super basic and this is actually a really easy problem. I don't know. That's the math life, I guess...

## Definition of $X_n$

Let $n \in \mathbb{Z}$, $n \geq 0$.

$X_n$ is the set of solutions $(a, b) \in \mathbb{Z} \times \mathbb{Z}$ to the congruence $a^b \equiv a \oplus b \pmod{2^n}$ for $0 \leq a,b < 2^n$, where $\oplus$ denotes the XOR operation.

## Problem

Determine the side of $X_n$.

## Solution

I am in the process of working on a solution. [Here's what I've done so far](https://raw.githubusercontent.com/SnootierMoon/pow-xor-equivalence/doc/pow_xor_equivalence.pdf).

Update: I basically have a solution to this involving 2-adics. Rather than updating the doc, I added a script to enumerate solutions given inputs a, b, n.

```
$ python3 query.py -log2n 67 -b 42
┌───────────────────────┬───────────────────────┬────┐
│ n                     │ a                     │ b  │
├───────────────────────┼───────────────────────┼────┤
│ 147573952589676412928 │ 7272896840079090435   │ 42 │
│ 147573952589676412928 │ 133248675076127064106 │ 42 │
└───────────────────────┴───────────────────────┴────┘
```

If you plug these values into `python3`, you will see that `pow(a, b, n) == a ^ b`.

You can query with any combination of including/omitting the following arguments: `-n` (or `-log2n`), `-a`, `-b`.
