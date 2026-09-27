import subprocess
from datetime import datetime


def run_git_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout.strip()


check = subprocess.run(
    ["git", "rev-parse", "--is-inside-work-tree"],
    capture_output=True,
    text=True
)

if check.returncode != 0:
    print("Reading Steiner must be run inside a Git repository.")
    exit()


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
    output = run_git_command(command)
    lines = output.splitlines()

    print(f"=== {title} (Total lines: {len(lines)}) ===")

    if title == "Repository History":
        print(f"Total commits: {len(lines)}")

        first_commit = run_git_command(
            ["git", "log", "--reverse", "-1", "--format=%h|%aI|%s"]
        )

        latest_commit = run_git_command(
            ["git", "log", "-1", "--format=%h|%aI|%s"]
        )

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

    if title == "Author":
        print(f"Total contributors: {len(lines)}")

    if title == "Files":
        print(f"Total tracked files: {len(lines)}")
        continue

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

    if title == "Current Branch":
        branch = lines[0].strip() if lines else ""

        if not branch:
            print("Current branch: Unable to determine")
            continue

        print(f"Current branch: {branch}")

        upstream = run_git_command([
            "git",
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{u}"
        ])

        if not upstream:
            print("Tracking branch: None")
            print("Branch is not connected to a remote branch")
            continue

        print(f"Tracking branch: {upstream}")

        count = run_git_command([
            "git",
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{upstream}"
        ])

        if count:
            behind, ahead = count.split()

            print(f"Commits ahead: {ahead}")
            print(f"Commits behind: {behind}")

            if ahead == "0" and behind == "0":
                print("Branch status: Up to date")
            elif ahead != "0" and behind == "0":
                print("Branch status: Local commits need to be pushed")
            elif ahead == "0" and behind != "0":
                print("Branch status: Remote commits need to be pulled")
            else:
                print("Branch status: Branches have diverged")

        continue

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