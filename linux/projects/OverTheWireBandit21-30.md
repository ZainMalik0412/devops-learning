# OverTheWire Bandit Walkthrough — Levels 21 to 30 (Bandit 20 ➜ 30)

> This section covers networking with a local listener, cron jobs, writing your first script for cron execution, brute forcing a 4-digit PIN, breaking out of a restricted shell, and Git-based levels.

---

## Level 21 (Bandit 20 ➜ 21) — Local listener + suconnect

**Goal:** There is a setuid programme that connects to a port you provide. If it receives the correct current password, it returns the next password.

You’ll need **two terminals** (two SSH sessions).

### Terminal A (listener)
```bash
nc -lvnp 3000
```

### Terminal B (run the programme)
```bash
ls
./suconnect 3000
# paste the current password when prompted
```

Back in Terminal A, you should receive the password for `bandit21`.

---

## Level 22 (Bandit 21 ➜ 22) — Cron job output file

**Goal:** A cron job runs on a schedule. Find what it runs and where the output goes.

1) Look at cron config:
```bash
ls -la /etc/cron.d
cat /etc/cron.d/cronjob_bandit22
```

2) Read the script it runs:
```bash
cat /usr/bin/cronjob_bandit22.sh
```

3) The script will show you a `/tmp/...` output file. Read it:
```bash
cat /tmp/<file-mentioned-in-script>
# output = password for bandit22
```

---

## Level 23 (Bandit 22 ➜ 23) — Cron + predictable temp filename

**Goal:** Another cron job runs a script which writes the password into a temp file based on an MD5 value.

1) Read the cron job:
```bash
cat /etc/cron.d/cronjob_bandit23
```

2) Read the script:
```bash
cat /usr/bin/cronjob_bandit23.sh
```

3) If the script computes a filename using something like:
`echo I am user <username> | md5sum`

You can reproduce it for bandit23:
```bash
echo I am user bandit23 | md5sum
# take the first hash value from the output
cat /tmp/<that-hash>
# output = password for bandit23
```

---

## Level 24 (Bandit 23 ➜ 24) — Create your own script for cron to run

**Goal:** A cron job (running as `bandit24`) executes scripts placed in a spool directory, then deletes them.

1) Inspect the cron job and script:
```bash
cat /etc/cron.d/cronjob_bandit24
cat /usr/bin/cronjob_bandit24.sh
```

2) Create a script that copies the password into a readable location:
```bash
tmpdir="$(mktemp -d)"
cd "$tmpdir"

cat > get_bandit24_pass.sh << 'EOF'
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/bandit24_pass.txt
chmod 644 /tmp/bandit24_pass.txt
EOF

chmod 755 get_bandit24_pass.sh
```

3) Drop it into the spool directory the cron job checks (commonly `/var/spool/bandit24/`):
```bash
cp get_bandit24_pass.sh /var/spool/bandit24/
```

4) Wait a minute for cron to run, then:
```bash
cat /tmp/bandit24_pass.txt
# output = password for bandit24
```

---

## Level 25 (Bandit 24 ➜ 25) — Brute force a 4-digit PIN

**Goal:** A daemon on port `30002` needs:
- the current password
- a **4-digit numeric pin**
There is no shortcut: try all `0000` to `9999`.

Send all combinations through one connection:
```bash
PASS="<PASTE_BANDIT24_PASSWORD_HERE>"

for pin in $(seq -w 0000 9999); do
  echo "$PASS $pin"
done | nc localhost 30002
```

When the correct PIN hits, the service returns the password for `bandit25`.

---

## Level 26 (Bandit 25 ➜ 26) — SSH key + restricted shell escape

**Goal:** Log into bandit26 using an SSH key. The shell is not `/bin/bash` and you need to break out.

1) Use the key you find in bandit25’s home directory:
```bash
ls
# likely: bandit26.sshkey
ssh -i bandit26.sshkey bandit26@localhost -p 2220
```

2) You may get dropped into a restricted flow (often using `more`).  
Common trick: **shrink your terminal window** so `more` pauses, then press:
- `v` to open an editor

From `vi/vim`, spawn a shell:
```vim
:set shell=/bin/bash
:shell
```

Now you should have a proper shell as `bandit26`.

---

## Level 27 (Bandit 26 ➜ 27) — Read the next password

**Goal:** Once you have a real shell as bandit26, grab the password for bandit27.

```bash
cat /etc/bandit_pass/bandit27
# output = password for bandit27
```

---

## Level 28 (Bandit 27 ➜ 28) — Git clone over SSH

**Goal:** Clone the repo and find the password in its contents.

```bash
workdir="$(mktemp -d)"
cd "$workdir"

git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
cd repo
ls
cat README
# output = password for bandit28
```

---

## Level 29 (Bandit 28 ➜ 29) — Password in Git history

**Goal:** Repo exists, but the password is not in the current version (it’s often in history).

```bash
workdir="$(mktemp -d)"
cd "$workdir"

git clone ssh://bandit28-git@localhost:2220/home/bandit28-git/repo
cd repo

git log --oneline
git show <commit-id>:README.md
# or:
git show <commit-id>
# find the password for bandit29 in a previous commit
```

---

## Level 30 (Bandit 29 ➜ 30) — Password in another branch

**Goal:** Repo exists, but the password is not on the default branch.

```bash
workdir="$(mktemp -d)"
cd "$workdir"

git clone ssh://bandit29-git@localhost:2220/home/bandit29-git/repo
cd repo

git branch -a
# look for interesting branches (often "dev" or similar)
git checkout <branch-name>

cat README.md
# output = password for bandit30
```
