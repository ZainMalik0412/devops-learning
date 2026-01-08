# OverTheWire Bandit Walkthrough — Levels 1 to 10 (Bandit 0 ➜ 10)

> Bandit is a wargame designed to build Linux terminal confidence. Each level gives you a small task to find the password for the next user.

## Prereqs

- Any Unix-like shell (Linux, macOS, WSL, or a Linux VM)
- SSH client

Login (Level 0):
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220
# default password: bandit0
```

Tip: Each time you find a password, log in to the next level like this:
```bash
ssh bandit1@bandit.labs.overthewire.org -p 2220
```

---

## Level 1 (Bandit 0 ➜ 1) — Read the obvious file

**Goal:** The password is in a file called `readme` in the home directory.

```bash
ls
cat readme
# output = password for bandit1
```

---

## Level 2 (Bandit 1 ➜ 2) — A file literally called "-"

**Goal:** The password is in a file named `-`.

Because `-` can be treated as “stdin” by commands, you should reference it safely:

```bash
ls
cat ./-
# output = password for bandit2
```

---

## Level 3 (Bandit 2 ➜ 3) — Spaces in the filename

**Goal:** The password is in a file called `spaces in this filename`.

Use quotes or escape the spaces:

```bash
ls
cat "spaces in this filename"
# or:
cat spaces\ in\ this\ filename
# output = password for bandit3
```

---

## Level 4 (Bandit 3 ➜ 4) — Hidden file inside `inhere`

**Goal:** Password is stored in a hidden file under `inhere`.

```bash
ls
cd inhere
ls -la
cat .hidden
# output = password for bandit4
```

---

## Level 5 (Bandit 4 ➜ 5) — Only human-readable file

**Goal:** Password is in the only human-readable file in `inhere`.

Use `file` to identify the readable one:

```bash
cd inhere
file ./*
# find the one that says "ASCII text" (or similar)
cat ./<the-readable-file>
# output = password for bandit5
```

---

## Level 6 (Bandit 5 ➜ 6) — Find by properties (size, readable, not executable)

**Goal:** Somewhere under `inhere` there is a file that is:
- human-readable
- exactly 1033 bytes
- not executable

```bash
cd inhere
find . -type f -size 1033c ! -executable -exec file {} \; | grep -i text
# then cat the matching file:
cat ./<path-to-file>
# output = password for bandit6
```

---

## Level 7 (Bandit 6 ➜ 7) — Find system-wide by owner/group/size

**Goal:** Find a file anywhere on the server that is:
- owned by `bandit7`
- grouped by `bandit6`
- 33 bytes in size

Ignore permission errors by redirecting them to `/dev/null`:

```bash
find / -type f -size 33c -user bandit7 -group bandit6 2>/dev/null
cat /path/returned/by/find
# output = password for bandit7
```

---

## Level 8 (Bandit 7 ➜ 8) — Grep the right line

**Goal:** Password is in `data.txt` next to the word `millionth`.

```bash
grep -n "millionth" data.txt
# output includes the password for bandit8
```

---

## Level 9 (Bandit 8 ➜ 9) — The only unique line

**Goal:** `data.txt` contains many duplicate lines. Password is the only line that occurs once.

```bash
sort data.txt | uniq -u
# output = password for bandit9
```

---

## Level 10 (Bandit 9 ➜ 10) — Hidden string in a binary

**Goal:** Password is in `data.txt` among human-readable strings, preceded by `=====`.

```bash
strings data.txt | grep "==="
# output = password for bandit10
```
