from verifier import verify_results

goal = "Enable Airplane Mode"
results = [
    "Step 1: SUCCESS",
    "Step 2: SUCCESS",
    "Step 3: SUCCESS - Airplane Mode Enabled"
]

if verify_results(goal, results):
    print("✅ Goal achieved!")
else:
    print("❌ Goal NOT achieved!")
