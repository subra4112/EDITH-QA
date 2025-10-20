from executor import execute_steps  # This works because both files are in the same folder

steps = [
    "Unlock the device",
    "Open Settings",
    "Enable Airplane Mode"
]

results = execute_steps(steps)

print("\n[Results]")
for r in results:
    print(r)
