# Linux Command Line Notes (Zain’s DevOps Learning)

## Table of contents
1. [Introduction](#introduction)
2. [Basic navigation](#basic-navigation)
3. [Working with files](#working-with-files)
4. [Viewing file contents](#viewing-file-contents)
5. [Searching in files](#searching-in-files)
6. [Copying, moving, renaming, deleting](#copying-moving-renaming-deleting)
7. [Creating nested folders and handling spaces](#creating-nested-folders-and-handling-spaces)
8. [Vim basics](#vim-basics)
9. [Users and groups](#users-and-groups)
10. [Groups](#groups)
11. [File permissions](#file-permissions)
12. [Ownership](#ownership)
13. [Redirects and error handling](#redirects-and-error-handling)
14. [Environment variables](#environment-variables)
15. [PATH basics](#path-basics)
16. [Shell scripts](#shell-scripts)
17. [Aliases and command history](#aliases-and-command-history)


---

## Introduction

These are my Linux command line notes as part of my DevOps learning. The goal is to build comfort with:

- navigating the file system
- creating and editing files
- permissions and ownership
- users and groups
- environment variables and basic scripting

Helpful terms:

- **Command**: what you type (example `ls`)
- **Option / flag**: modifies a command (example `head -n 5`)
- **Argument**: target of a command (example `cat file.txt`)

---

## Basic navigation

| Command | What it does | Example |
| --- | --- | --- |
| `ls` | lists files and folders in the current directory | `ls` |
| `pwd` | shows the current directory path | `pwd` |
| `cd` | changes directory | `cd Desktop` |
| `Ctrl + L` | clears the terminal screen | press `Ctrl + L` |

Examples:
```bash
pwd
ls
cd Desktop
```

## Working with files

| Command | What it does | Example |
| --- | --- | --- |
| `touch` | creates an empty file | `touch hello.txt` |
| `echo` | prints text or writes to a file | `echo "hello world" > file.txt` |
| `cat` | prints the full file contents | `cat file.txt` |

Create a new file:

```bash
touch hello.txt
```

Write to a file (overwrites):

```bash
echo "hello world" > file.txt
```

Append to a file (does not overwrite):

```bash
echo "test" >> file.txt
```

Create a second file:

```bash
echo "This is the second file" > myfile2.txt
```

Combine 2 files into a new file:

```bash
cat myfile.txt myfile2.txt > combined.txt
```

## Viewing file contents

| Command | What it does | Example |
| --- | --- | --- |
| `cat` | prints the full file contents | `cat file.txt` |
| `head` | shows the first 10 lines | `head newline.txt` |
| `head -n` | shows the first N lines | `head -n 5 newline.txt` |
| `tail` | shows the last 10 lines | `tail newline.txt` |
| `tail -n` | shows the last N lines | `tail -n 3 newline.txt` |

Examples:

```bash
cat file.txt
head newline.txt
head -n 5 newline.txt
tail newline.txt
tail -n 3 newline.txt
```

Show a "middle section" by piping:

```bash
head -n 10 newline.txt | tail -n 5
```

## Searching in files

| Command | What it does | Example |
| --- | --- | --- |
| `grep` | searches for text inside a file | `grep "hello" file.txt` |

Example:

```bash
grep "hello" file.txt
```

## Copying, moving, renaming, deleting

| Command | What it does | Example |
| --- | --- | --- |
| `cp` | copies a file | `cp newline.txt newline_copy.txt` |
| `mv` | moves or renames a file | `mv old.txt new.txt` |
| `rm` | removes a file | `rm file.txt` |
| `mkdir` | creates a directory | `mkdir hello` |
| `rmdir` | removes an empty directory | `rmdir hello` |
| `rm -r` | removes a directory and its contents | `rm -r my_directory` |

Copy a file:

```bash
cp newline.txt newline_copy.txt
```

Rename a file:

```bash
mv newline_copy.txt newline_backup.txt
```

Move a file into a directory:

```bash
mv newline_backup.txt my_directory
```

Remove a file:

```bash
rm newline_backup.txt
```

Remove a directory and everything inside it:

```bash
rm -r my_directory
```

## Creating nested folders and handling spaces

Create nested directories in one command:

```bash
mkdir -p projects/src/components
```

Create a directory that includes spaces:

```bash
mkdir "my project"
```

## Vim basics

Open or create a file:

```bash
vim example.txt
```

Vim essentials:

| Action | Keys |
| --- | --- |
| Enter insert mode | `i` |
| Exit insert mode | `Esc` |
| Save and quit | `:wq` then `Enter` |
| Quit without saving | `:q!` then `Enter` |

## Users and groups

### Create a new user and set a password

| Command | What it does | Example |
| --- | --- | --- |
| `sudo useradd` | creates a new user | `sudo useradd newuser` |
| `sudo passwd` | sets a password for a user | `sudo passwd newuser` |
| `su -` | switches to another user (login shell) | `su - newuser` |
| `whoami` | shows current user | `whoami` |

Commands:

```bash
sudo useradd newuser
sudo passwd newuser
su - newuser
whoami
```

### Give and remove sudo access

Give sudo access:

```bash
sudo usermod -aG sudo newuser
```

Remove sudo access:

```bash
sudo deluser newuser sudo
```

## Groups

| Command | What it does | Example |
| --- | --- | --- |
| `sudo groupadd` | creates a new group | `sudo groupadd devops` |
| `cat /etc/group` | lists all groups | `cat /etc/group` |
| `sudo usermod -aG` | adds user to a group | `sudo usermod -aG devops newuser` |
| `sudo gpasswd -d` | removes user from a group | `sudo gpasswd -d newuser devops` |
| `sudo groupdel` | deletes a group | `sudo groupdel devops` |
| `grep` | searches within a file | `grep devops /etc/group` |

Create a group:

```bash
sudo groupadd devops
```

View all groups:

```bash
cat /etc/group
```

Add a user to a group:

```bash
sudo usermod -aG devops newuser
```

Remove a user from a group:

```bash
sudo gpasswd -d newuser devops
```

Delete a group:

```bash
sudo groupdel devops
```

Search for a group:

```bash
grep devops /etc/group
```

Add a user to multiple groups at the same time:

```bash
sudo usermod -aG admin,admin2 newuser
```

## File permissions

Permissions are based on:

- `u` = user (owner)
- `g` = group
- `o` = others
- `r` = read
- `w` = write
- `x` = execute

| Symbol | Meaning |
| --- | --- |
| `r` | read |
| `w` | write |
| `x` | execute |

Add and remove specific permissions:

```bash
chmod u+x,g+r,o-w example.txt
```

Set permissions explicitly:

```bash
chmod ug=rw,o=r example.txt
```

## Ownership

| Command | What it does | Example |
| --- | --- | --- |
| `chown` | changes file owner | `sudo chown newuser example.txt` |
| `chgrp` | changes file group | `sudo chgrp admin2 example.txt` |

Change owner of a file:

```bash
sudo chown newuser example.txt
```

Change group of a file:

```bash
sudo chgrp admin2 example.txt
```

## Redirects and error handling

| Redirect | What it does | Example |
| --- | --- | --- |
| `2>` | redirects errors (stderr) to a file | `ls nonexistant 2> error.txt` |

Example:

```bash
ls nonexistant 2> error.txt
cat error.txt
```

## Environment variables

Temporary environment variable (current session only):

```bash
export MY_VAR="Hello world"
echo $MY_VAR
```

Make an environment variable permanent (zsh example):

Edit your config file:

```bash
vim ~/.zshrc
```

Add this line:

```bash
export MY_VAR="hello world"
```

Reload file:

```bash
source ~/.zshrc
```

Check it:

```bash
echo $MY_VAR
```

## PATH basics

| Command | What it does | Example |
| --- | --- | --- |
| `echo $PATH` | prints your PATH | `echo $PATH` |
| `export PATH=...` | adds a directory to PATH (session only) | `export PATH=$PATH:/home/ubuntu` |

Show your current PATH:

```bash
echo $PATH
```

Add a directory to PATH (current session):

```bash
export PATH=$PATH:/home/ubuntu
echo $PATH
```

## Shell scripts

Create a script file:

```bash
vim greet.sh
```

Example script:

```bash
#!/bin/bash
# A simple script to greet user
echo "Hello, $USER! Welcome to $HOSTNAME."
```

Make it executable:

```bash
chmod +x greet.sh
```

Run it:

```bash
./greet.sh
```

## Aliases and command history

### Aliases

Temporary alias (current session):

```bash
alias hello='echo "Hello world"'
hello
```

To make an alias permanent:

Add alias to `~/.zshrc`

Then reload it:

```bash
source ~/.zshrc
```

### History shortcuts

| Shortcut | What it does |
| --- | --- |
| `!` | runs a command from history (example `!34`) |
| `Ctrl + R` | reverse search through previous commands |
