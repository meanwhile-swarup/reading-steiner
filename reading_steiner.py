import subprocess

git_commands = [
    ["git", "log", "--oneline"],
]

results = []

for command in git_commands:
    result = subprocess.run(command, capture_output=True, text=True)
    results.append(result.stdout)

for result in results:
    wordResult = result.splitlines()

for word in wordResult:
    splitWord = word.split()
    print(f"{splitWord[0]} -> {" ".join(splitWord[1:])}")

print("-- READING STEINER --")

print("Git gave us:")

for result in results:
    print(result)