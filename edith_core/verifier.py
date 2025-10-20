# verifier.py

def verify_results(goal: str, executor_results: list[str]) -> tuple[list[str], bool]:
    print("\n[Verifier] Verifying task outcome...")

    expected_keywords = goal.lower().split()
    matched_keywords = [kw for kw in expected_keywords if any(kw in step.lower() for step in executor_results)]

    print(f"\nMatched keywords: {matched_keywords}")

    # Consider success if 3 or more keywords matched
    success = len(matched_keywords) >= 3

    return matched_keywords, success


