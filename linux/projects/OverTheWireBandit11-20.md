# OverTheWire Bandit Walkthrough — Levels 11 to 20 (Bandit 10 ➜ 20)

> This section covers Base64, ROT13, compression layers, SSH keys, `diff`, bypassing a forced logout, and setuid binaries.

---

## Level 11 (Bandit 10 ➜ 11) — Base64 decode

**Goal:** `data.txt` is Base64 encoded.

```bash
cat data.txt
base64 -d data.txt
# output includes the password for bandit11
```

---

## Level 12 (Bandit 11 ➜ 12) — ROT13

**Goal:** `data.txt` has letters rotated by 13 positions.

```bash
cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
# output includes the password for bandit12
```

---

## Level 13 (Bandit 12 ➜ 13) — Multi-step decompression (hexdump ➜ extract ➜ extract...)

**Goal:** `data.txt` is a hexdump of a file that has been compressed multiple times.

**Approach:**
1) Work in `/tmp` so you can write files freely  
2) Convert the hexdump back into a binary  
3) Repeatedly use `file` to identify the format, then extract

```bash
tmpdir="$(mktemp -d)"
cd "$tmpdir"
cp ~/data.txt .

# Convert hexdump back to binary
xxd -r data.txt data.bin

# Now repeatedly run `file` then extract based on the result
file data.bin
```

Typical extraction loop (you may need several steps):
```bash
# Example patterns you may hit:
# gzip -> gunzip
# bzip2 -> bunzip2
# tar -> tar xf
# "ASCII text" -> cat to read password

mv data.bin data.gz && gunzip data.gz
file data
mv data data.bz2 && bunzip2 data.bz2
file data
mv data data.tar && tar xf data.tar
file *
# keep going until you get plain text, then:
cat <final-text-file>
# output = password for bandit13
```

---

## Level 14 (Bandit 13 ➜ 14) — SSH private key login

**Goal:** Log into bandit14 using the provided private key.

```bash
ls
# you should see something like: sshkey.private

ssh -i sshkey.private bandit14@localhost -p 2220
```

Once logged in as `bandit14`:
```bash
cat /etc/bandit_pass/bandit14
# output = password for bandit14 (used for next level)
```

---

## Level 15 (Bandit 14 ➜ 15) — Use netcat to talk to a service

**Goal:** A service on localhost port `30000` gives the next password if you provide the current password.

```bash
nc localhost 30000
# paste the current password and press Enter
# output = password for bandit15
```

---

## Level 16 (Bandit 15 ➜ 16) — SSL/TLS connection (openssl)

**Goal:** Submit the current password to localhost port `30001` using SSL/TLS.

```bash
openssl s_client -connect localhost:30001
# paste the current password and press Enter
# output = password for bandit16
```

Tip: If it looks “stuck”, try:
```bash
openssl s_client -connect localhost:30001 -quiet
```

---

## Level 17 (Bandit 16 ➜ 17) — Find the correct SSL service and retrieve an SSH key

**Goal:** One of the ports `31000-32000` has an SSL service that returns the credentials for the next level when you provide the current password.

1) Scan for open ports:
```bash
nmap -p 31000-32000 localhost
```

2) Test the likely SSL ports with `openssl`:
```bash
openssl s_client -connect localhost:<PORT> -quiet
# paste the current password and press Enter
```

If the output contains an SSH private key, save it (copy/paste) into a file:
```bash
nano bandit17.key
# paste the key, save, exit

chmod 600 bandit17.key
ssh -i bandit17.key bandit17@localhost -p 2220
```

Once logged in as `bandit17`:
```bash
cat /etc/bandit_pass/bandit17
# output = password for bandit17
```

---

## Level 18 (Bandit 17 ➜ 18) — `diff` the changed line

**Goal:** Password is the only changed line between `passwords.old` and `passwords.new`.

```bash
diff passwords.old passwords.new
# the line shown as added/changed is the password for bandit18
```

Alternative:
```bash
grep -Fxv -f passwords.old passwords.new
# output = password for bandit18
```

---

## Level 19 (Bandit 18 ➜ 19) — Bypass forced logout via SSH command

**Goal:** `.bashrc` logs you out immediately. Run a command directly over SSH.

```bash
ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat readme"
# output = password for bandit19
```

---

## Level 20 (Bandit 19 ➜ 20) — Use a setuid binary

**Goal:** Use the setuid binary in the home directory to read the next password from `/etc/bandit_pass/`.

1) Check what the binary does:
```bash
ls
./bandit20-do
```

2) Use it to read the next password file:
```bash
./bandit20-do cat /etc/bandit_pass/bandit20
# output = password for bandit20
```
