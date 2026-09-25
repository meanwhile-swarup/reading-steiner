import subprocess
from datetime import datetime

git_commands = [
    ("Repository History", ["git", "log", "--oneline"]),
    ("Latest Commit", ["git", "log", "-1", "--oneline"]),
    ("Current Branch", ["git", "branch", "--show-current"]),
    ("Remote URLs", ["git", "remote", "-v"]),
    ("Author", ["git", "shortlog", "-sn"]),
    ("Files", ["git", "ls-files"]),
    ("Repository Status", ["git", "status", "--short"])
]

print("-- READING STEINER --\n")

for title, command in git_commands:
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    print(f"=== {title} (Total lines: {len(lines)}) ===")

    # Repository History
    if title == "Repository History":
        print(f"Total commits: {len(lines)}")

        first_commit = subprocess.run(
            ["git", "log", "--reverse", "-1", "--format=%h|%aI|%s"],
            capture_output=True,
            text=True
        ).stdout.strip()

        latest_commit = subprocess.run(
            ["git", "log", "-1", "--format=%h|%aI|%s"],
            capture_output=True,
            text=True
        ).stdout.strip()

        if first_commit:
            hash_, date, message = first_commit.split("|", 2)

            print(f"First commit: {hash_} -> {message}")
            print(f"First commit date: {date}")

        if latest_commit:
            hash_, date, message = latest_commit.split("|", 2)

            print(f"Latest commit: {hash_} -> {message}")
            print(f"Latest commit date: {date}")

        if first_commit and latest_commit:
            first_commit_date = datetime.fromisoformat(
                first_commit.split("|", 2)[1]
            )

            latest_commit_date = datetime.fromisoformat(
                latest_commit.split("|", 2)[1]
            )

            repo_age = latest_commit_date - first_commit_date

            print(f"Repository age: {repo_age.days} days")

    # Authors
    if title == "Author":
        print(f"Total contributors: {len(lines)}")

    # Files
    if title == "Files":
        print(f"Total tracked files: {len(lines)}")
        continue

    # Repository Status
    if title == "Repository Status":
        if not lines:
            print("Working tree is clean")
        else:
            print(f"Changed files: {len(lines)}")

            for line in lines:
                status = line[:2]
                filename = line[3:]

                print(f"{status} -> {filename}")

        continue

    # Normal output
    for line in lines:
        split_word = line.split()

        if title == "Author":
            author_name = " ".join(split_word[1:])
            print(f"Author is: {author_name}")
            continue

        if split_word and len(split_word) > 1:
            print(f"{split_word[0]} -> {' '.join(split_word[1:])}")
        else:
            print(" ".join(split_word))

    print()
