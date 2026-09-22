import subprocess

git_commands = [
    ("Repository History", ["git", "log", "--oneline"]),
    ("Latest Commit", ["git", "log", "-1", "--oneline"]),
    ("Current Branch", ["git", "branch", "--show-current"]),
    ("Remote URLs", ["git", "remote", "-v"]),
    ("Author", ["git", "shortlog", "-sn"])
]

print("-- READING STEINER --\n")

for title, command in git_commands:
    result = subprocess.run(command, capture_output=True, text=True)
    lines = result.stdout.splitlines()

    print(f"=== {title} (Total lines: {len(lines)}) ===")

    if title == "Repository History":
        print(f"Total commits: {len(lines)}")

    for line in lines:
        split_word = line.split()
        
        if title == "Author":
            author_name = ' '.join(split_word[1:])
            print(f"Author is:{author_name}")
            continue

        if split_word and len(split_word) > 1:
            print(f"{split_word[0]} -> {' '.join(split_word[1:])}")
        else:
            print(" ".join(split_word))
            
    print()
