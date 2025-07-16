# 🧠 ao1codes' Brainrot

A playful little esolang where commands like rizz, yeet, and sus control a number. Write loops, print values, and mess with the accumulator to make weird, fun programs.

---

# Features

* 12+ Gen Z slang commands that change an integer accumulator
* Line-by-line parser ignoring blanks and comments (#)
* Nested loops with vibe and unvibe
* Skip next command if accumulator is zero (sus)
* Prints accumulator with skibidi
* Debug mode for command tracing

---

# Installation & Running

1. Clone this repo
   ```bash
   git clone https://github.com/ao1codes/brainrot_escolang.git
   cd brainrot_escolang
   ```

2. Run your Brainrot program with Python 3
   ```bash
    python3 brainrot.py examples/hello\_world.brainrot
   ```

3. Add --debug to trace commands
   ```bash
    python3 brainrot.py --debug examples/hello\_world.brainrot
   ```
   
---

# Commands Cheat Sheet

- `rizz` — Increment accumulator by 1
- `gyatt` — Decrement accumulator by 1
- `drip` — Increment accumulator by 5
- `npc` — Decrement accumulator by 5
- `yeet` — Multiply accumulator by 2
- `cringe` — Integer divide accumulator by 2 if not zero
- `skibidi` — Print current accumulator value
- `no cap` — Reset accumulator to 0
- `sus` — If accumulator is 0, skip next command
- `vibe` — Start loop (while accumulator > 0)
- `unvibe` — End loop (jump back if accumulator > 0)
- `mid` — No-op (comment / ignore)

---

# Example snippet

```brainrot
no cap
drip
rizz
vibe
skibidi
gyatt
unvibe
```

**Expected output:**

```
6
5
4
3
2
1
```

---