# run.py

from edith_core import supervisor
import json
from datetime import datetime
import os

if __name__ == "__main__":
    goal = "Enable Airplane Mode from Settings"

    # 🎯 Run the full multi-agent test flow
    result = supervisor.run_task(goal)

    # 📄 Save all data to a structured JSON log
    log_data = {
        "timestamp": datetime.now().isoformat(),
        **result
    }

    os.makedirs("logs", exist_ok=True)
    with open("logs/airplane_mode.json", "w") as f:
        json.dump(log_data, f, indent=2)

    print("📄 QA log saved to logs/airplane_mode.json")
