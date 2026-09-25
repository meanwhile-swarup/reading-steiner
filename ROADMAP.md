# Reading Steiner

> A Python CLI that reads Git history and turns it into useful repository information.

Inspired by the **Reading Steiner** concept from *Steins;Gate*.

## What is it?

Reading Steiner is a small command-line tool for exploring a Git repository without manually running multiple Git commands.

It currently reads information such as:

* Commit history
* First and latest commits
* Repository age
* Current branch
* Tracking branch
* Commits ahead/behind remote
* Remote URLs
* Contributors
* Tracked files
* Working tree status

## Current Output

Example:

```text
-- READING STEINER --

=== Repository History ===
Total commits: 42
First commit: a81f23a -> initial commit
First commit date: 2026-01-12T10:32:41+05:45
Latest commit: 91a82cd -> add repository statistics
Latest commit date: 2026-09-25T18:21:03+05:45
Repository age: 256 days

=== Current Branch ===
Current branch: main
Tracking branch: origin/main
Commits ahead: 0
Commits behind: 0
Branch status: Up to date

=== Author ===
Total contributors: 3
Author is: Swarup Shakya

=== Files ===
Total tracked files: 27

=== Repository Status ===
Working tree is clean
```

## Tech Stack

* **Python**
* `subprocess`
* Git CLI
* `datetime`

No Git library is currently required. Reading Steiner interacts with Git through the command line.
