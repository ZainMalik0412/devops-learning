# Git and GitHub Notes

## Table of contents
1. [Introduction](#introduction)
2. [Core concepts](#core-concepts)
3. [Centralised vs distributed version control](#centralised-vs-distributed-version-control)
4. [How Git stores data](#how-git-stores-data)
5. [The three areas of Git](#the-three-areas-of-git)
6. [Common commands](#common-commands)
7. [Viewing history and changes](#viewing-history-and-changes)
8. [Branches, merging, and conflicts](#branches-merging-and-conflicts)
9. [Rebase vs merge](#rebase-vs-merge)
10. [Stashing work](#stashing-work)
11. [Reset, revert, reflog, and cherry-pick](#reset-revert-reflog-and-cherry-pick)
12. [Git vs GitHub](#git-vs-github)
13. [Forks and pull requests](#forks-and-pull-requests)
14. [Collaboration workflow](#collaboration-workflow)
15. [Trunk based development](#trunk-based-development)
16. [Commit hygiene](#commit-hygiene)
17. [Pre-commit and automation](#pre-commit-and-automation)
18. [Mistakes I want to avoid](#mistakes-i-want-to-avoid)
19. [Security and secrets hygiene](#security-and-secrets-hygiene)
20. [Connecting to GitHub (remotes)](#connecting-to-github-remotes)
21. [Mini command recipes](#mini-command-recipes)
22. [Quick self test](#quick-self-test)

---

## Introduction

These are my Git notes as part of my DevOps learning. The goal is to understand Git properly (not just memorise commands), including how Git stores data, how branching works, and how to collaborate safely with GitHub.

---

## Core concepts

| Term | Meaning |
| --- | --- |
| Version control | Tracks changes to code over time so you can inspect, revert, review, and collaborate safely |
| Commit | A snapshot of files and metadata at a point in time |
| Branch | A movable pointer to a specific commit |
| Remote | A reference to an external Git host (for example GitHub) |
| Staging area | A buffer between your working directory and the repository (what you plan to commit) |
| Refs | Pointers to commits (branches and tags) |
| HEAD | Pointer to your current branch or current commit (if detached) |
| Index | The `.git/index` binary file that holds staging area information |

---

## Centralised vs distributed version control

| Type | What it means | Key points |
| --- | --- | --- |
| Centralised | One central server stores the full history | Often requires a network connection to commit; conflicts were more common; branching/merging tends to be slower |
| Distributed (Git) | Each machine has the full history | Can work offline; fast branching and merging; history exists locally |

My summary:
- Centralised: the server is the source of truth for history.
- Distributed: every clone is a full copy of history, so Git operations are fast and work offline.

---

## How Git stores data

Git stores your project as objects:

| Object | What it stores |
| --- | --- |
| Blobs | The contents of files (just the data) |
| Trees | Filenames, folder structure, and pointers to blobs |
| Commits | Snapshot metadata + pointer to a tree + parent commit(s) |
| Refs | Human-friendly pointers to commits (branches and tags) |

### The `.git` directory (what lives inside)

| Path | What it stores |
| --- | --- |
| `.git/objects/` | All objects (commits, blobs, trees) |
| `.git/refs/` | Branches and tags (pointers) |
| `.git/config` | Repo-specific settings |
| `.git/HEAD` | Where HEAD points (current branch pointer) |
| `.git/index` | Staging area (what you have added but not committed) |

---

## The three areas of Git

| Area | What it is | Example commands |
| --- | --- | --- |
| Working directory | Files you are editing right now | edit files, `git diff` |
| Staging area | Changes marked for commit | `git add`, `git restore --staged` |
| Repository | Commits (snapshots) | `git commit`, `git log` |

Typical flow:
~~~bash
git add .
git commit -m "Meaningful message"
~~~

---

## Common commands

| Command | What it does |
| --- | --- |
| `git init` | Initialises a new Git repo (creates the `.git` directory) |
| `git clone` | Copies a remote repo locally |
| `git status` | Shows staged and unstaged changes |
| `git add` | Stages changes |
| `git commit` | Creates a snapshot (commit) |
| `git log` | Shows commit history |
| `git diff` | Shows what changed |
| `git rm` | Removes files and stages the removal |
| `git mv` | Renames/moves files and stages it |
| `git restore` | Discards local changes (or unstages with `--staged`) |
| `git config` | Sets Git configuration such as name and email |
| `git help <command>` | Built-in docs |

---

## Viewing history and changes

### Logs

| Command | What it shows |
| --- | --- |
| `git log` | Full commit history |
| `git log --oneline` | Compact history |
| `git log --oneline --graph` | Visual branch history |
| `git log --oneline --graph --all` | Full visual view across all branches (great for debugging) |
| `git show <commit>` | A specific commit and its changes |

Examples:
~~~bash
git log
git log --oneline
git log --oneline --graph
git log --oneline --graph --all
git show <commit-hash>
~~~

### Diffs

| Command | What it compares |
| --- | --- |
| `git diff` | Working directory vs last commit |
| `git diff --staged` | Staging area vs last commit |

Examples:
~~~bash
git diff
git diff --staged
~~~

### Blame

| Command | What it does |
| --- | --- |
| `git blame <file>` | Shows who last changed each line in a file |

Example:
~~~bash
git blame README.md
~~~

---

## Branches, merging, and conflicts

### Branch basics

| Command | What it does |
| --- | --- |
| `git branch` | Lists branches (and can create with a name) |
| `git checkout -b <branch>` | Creates and switches to a branch |
| `git switch <branch>` | Switches branches (safer modern approach) |
| `git merge <branch>` | Merges the given branch into the current branch |

Create and switch:
~~~bash
git checkout -b feature1
# or:
git switch -c feature1
~~~

Switch back to main:
~~~bash
git switch main
~~~

Merge feature into main:
~~~bash
git switch main
git merge feature1
~~~

### Conflicts (how I handle them)

1. Check what is conflicted:
~~~bash
git status
~~~

2. Open the conflicted files and resolve the conflict markers.

3. Stage the resolved files:
~~~bash
git add <file>
~~~

4. Finish the merge:
~~~bash
git commit
~~~

---

## Rebase vs merge

| Approach | What it does | When it is useful |
| --- | --- | --- |
| Merge | Preserves history, may create a merge commit | Team workflows, shared branches, clarity |
| Rebase | Rewrites history by replaying commits | Cleaning up local feature branches before merging |

Key point:
- Rebase rewrites history, so avoid rebasing public/shared branches unless you know exactly what you are doing.

---

## Stashing work

Stash is for when you need to switch tasks but you are not ready to commit.

| Command | What it does |
| --- | --- |
| `git stash` | Saves uncommitted changes temporarily |
| `git stash push -m "message"` | Stashes with a message |
| `git stash list` | Lists stashes |
| `git stash apply` | Reapplies a stash (keeps it in the list) |
| `git stash pop` | Reapplies and removes the stash |
| `git stash clear` | Deletes all stashes |

Examples:
~~~bash
git stash push -m "Work in progress: feature.txt changes"
git stash list
git stash apply
git stash pop
git stash clear
~~~

---

## Reset, revert, reflog, and cherry-pick

### Revert (safe for shared history)

| Command | What it does |
| --- | --- |
| `git revert <commit>` | Creates a new commit that undoes another commit |
| `git revert HEAD` | Reverts the most recent commit |

Example:
~~~bash
git revert HEAD
~~~

Use revert when:
- the commit is already pushed
- you want a safe undo without rewriting history (good for shared branches and production)

### Reset (moves branch pointer)

| Command | What it does |
| --- | --- |
| `git reset --soft HEAD~1` | Undo commit but keep changes staged |
| `git reset --mixed HEAD~1` | Undo commit and unstage changes (default) |
| `git reset --hard HEAD~1` | Undo commit and delete changes entirely |

Examples:
~~~bash
git reset --soft HEAD~1
git reset --mixed HEAD~1
git reset --hard HEAD~1
~~~

### Reflog (your safety net)

Reflog tracks where HEAD and branches pointed to, even if commits are no longer visible in normal logs.

~~~bash
git reflog
# use this if you accidentally reset or lost a commit
~~~

### Cherry-pick (bring one commit over)

| Command | What it does |
| --- | --- |
| `git cherry-pick <hash>` | Applies a single commit from another branch onto your current branch |

Example:
~~~bash
git cherry-pick 32bb225
~~~

---

## Git vs GitHub

- Git: the version control tool that runs locally on your machine.
- GitHub: a hosting platform for Git repositories plus collaboration features (pull requests, issues, code review, Actions, projects).

---

## Forks and pull requests

| Term | Meaning |
| --- | --- |
| Fork | Your own copy of someone else’s GitHub repo (on GitHub) |
| Clone | Bringing a repo from GitHub onto your local machine |
| Pull request (PR) | A proposal to merge changes, reviewed before merging |

Typical fork flow:
1. Fork the repo on GitHub
2. Clone your fork locally
3. Create a branch, commit changes, push
4. Open a pull request back to the original repo

---

## Collaboration workflow

### Starting your own project

1) Initialise Git:
~~~bash
git init
~~~

2) Create a new repo on GitHub

3) Link remote:
~~~bash
git remote add origin <REMOTE-URL>
git remote -v
~~~

4) Push main:
~~~bash
git push -u origin main
~~~

### Git basic local lifecycle

1) Modify files locally  
2) Review changes:
~~~bash
git status
git diff
~~~

3) Stage changes:
~~~bash
git add <filename>
# or stage everything:
git add .
~~~

4) Commit changes:
~~~bash
git commit -m "Your commit message"
~~~

5) Push:
~~~bash
git push origin main
~~~

### Git collaboration lifecycle (team workflow)

1) Pull latest before starting:
~~~bash
git pull origin main
~~~

2) Create a feature branch:
~~~bash
git checkout -b feature-branch-name
# or:
git switch -c feature-branch-name
~~~

3) Work and commit:
~~~bash
git status
git diff
git add .
git commit -m "Describe what changed"
~~~

4) Push your branch:
~~~bash
git push origin feature-branch-name
~~~

5) Open a pull request on GitHub for review  
6) Merge into main after approval  
7) Delete the feature branch after merging to keep things clean  
8) Pull updated main:
~~~bash
git pull origin main
~~~

---

## Trunk based development

Trunk based development means:
- everyone commits to `main` or very short-lived branches
- strong CI/testing gates (all commits get tested automatically)
- common in fast moving teams with small, frequent changes

---

## Commit hygiene

Good habits I want to follow:
- Write clear, descriptive commit messages
- One logical change per commit
- Commit often, but keep commits meaningful
- Squash noisy commits before merging a PR if needed

Interactive rebase for squashing:
~~~bash
git rebase -i HEAD~3
# change "pick" to "squash" on the commits you want to combine
~~~

Amend the last commit message:
~~~bash
git commit --amend
~~~

---

## Pre-commit and automation

Pre-commit hooks and automation help prevent broken code entering the repo.

Examples of what teams automate:
- formatting (linting)
- unit tests
- security scanning
- secret scanning

This can run locally (pre-commit hooks) and in CI (GitHub Actions, etc).

---

## Mistakes I want to avoid

- Forgetting to pull before pushing (causes conflicts)
- Force pushing to shared branches
- Merging without review
- Not using `.gitignore` properly
- Accidentally committing secrets

---

## Security and secrets hygiene

- Do not commit secrets into Git history
- Use `.gitignore` to avoid committing local config and secrets
- Use secret scanning tools where possible (for example `git-secrets`)
- If a secret leaks: rotate it and remove it from history (do not rely on deleting the file in a later commit)

---

## Connecting to GitHub (remotes)

| Command | What it does |
| --- | --- |
| `git remote add origin <url>` | Links local repo to GitHub |
| `git remote -v` | Confirms remote URLs |
| `git push -u origin main` | Pushes and sets upstream |
| `git pull` | Brings down changes from GitHub and merges |

Examples:
~~~bash
git remote add origin <url>
git remote -v
git push -u origin main
git pull
~~~

---

## Mini command recipes

### Create a repo and push it to GitHub
~~~bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <REMOTE-URL>
git push -u origin main
~~~

### Basic branch workflow example
~~~bash
git checkout -b feature1
echo "feature branch change" > app.txt
git add app.txt
git commit -m "Add app.txt for feature1"

git checkout main
git merge feature1

git branch
git branch -d feature1
~~~

### Undo changes in a file
Discard local changes and return to the last committed state:
~~~bash
git restore undo.txt
~~~

Unstage a file (move from staged back to unstaged):
~~~bash
git restore --staged undo.txt
~~~

### Undo the most recent commit (choose the right reset)
Keep changes staged:
~~~bash
git reset --soft HEAD~1
~~~

Unstage but keep file changes:
~~~bash
git reset --mixed HEAD~1
~~~

Delete commit and file changes:
~~~bash
git reset --hard HEAD~1
~~~

### Revert safely (recommended for shared branches)
~~~bash
git revert HEAD
~~~

### Stash work in progress
~~~bash
git stash push -m "Work in progress"
git stash list
git stash apply
git stash pop
~~~

### Recover work with reflog
~~~bash
git reflog
# then reset back to the commit you want:
git reset --hard <hash-from-reflog>
~~~

### Grab one commit from another branch
~~~bash
git cherry-pick <commit-hash>
~~~

---


