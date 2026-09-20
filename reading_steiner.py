import subprocess

git_commands = [
    ["git", "log", "--oneline"],
]

results = []

for command in git_commands:
    result = subprocess.run(command, capture_output=True, text=True)
    results.append(result.stdout)

print("-- READING STEINER --")

print("Git gave us:")

for result in results:
    print(result)