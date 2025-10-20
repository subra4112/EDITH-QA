# executor.py
import time
import os
import numpy as np
import cv2

def mock_render(step_idx: int):
    """Create a mock screenshot image with step number"""
    img = np.ones((240, 240, 3), dtype=np.uint8) * 220
    cv2.putText(img, f"Step {step_idx}", (40, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return img

def execute_steps(step_list: list[str]) -> list[str]:
    print("\n[Executor] Starting execution...\n")
    results = []
    os.makedirs("images", exist_ok=True)

    for idx, step in enumerate(step_list, 1):
        print(f"🟢 Executing Step {idx}: {step}")
        time.sleep(1)

        # 🧪 Create and save a mock screenshot
        frame = mock_render(idx)
        cv2.imwrite(f"images/step_{idx:02}_mock.png", frame)

        results.append(f"{step} — SUCCESS")

    print("\n[Executor] Execution complete.\n")
    return results
