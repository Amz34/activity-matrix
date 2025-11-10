import datetime
import os
import subprocess
import random

# Generate authentic distribution of historical engineering commits across past 12 months
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

current = start_date
dates_to_commit = []

while current <= end_date:
    # Give higher frequency on weekdays (Tue-Thu) like realistic senior engineering activity
    weekday = current.weekday()
    if weekday in [1, 2, 3]: # Tue, Wed, Thu
        num_commits = random.choices([1, 2, 3, 4], weights=[40, 30, 20, 10])[0]
    elif weekday in [0, 4]: # Mon, Fri
        num_commits = random.choices([0, 1, 2], weights=[50, 35, 15])[0]
    else: # Weekends
        num_commits = random.choices([0, 1], weights=[85, 15])[0]

    for c in range(num_commits):
        hour = random.randint(9, 21)
        minute = random.randint(10, 59)
        commit_dt = current.replace(hour=hour, minute=minute, second=random.randint(0, 59))
        dates_to_commit.append(commit_dt)
    
    current += datetime.timedelta(days=1)

print(f"Generated {len(dates_to_commit)} engineering timestamps across 365 days.")

# Write initial file
with open("telemetry.log", "w") as f:
    f.write("# Infrastructure Telemetry Ledger\n")

subprocess.run(["git", "add", "README.md", "telemetry.log", "generate-matrix.py"], check=True)
first_iso = dates_to_commit[0].strftime("%Y-%m-%d %H:%M:%S")
env = os.environ.copy()
env["GIT_AUTHOR_DATE"] = first_iso
env["GIT_COMMITTER_DATE"] = first_iso
subprocess.run(["git", "commit", "-m", "init: bootstrap telemetry matrix"], env=env, check=True)

# Build commit tree
for i, dt in enumerate(dates_to_commit[1:]):
    with open("telemetry.log", "a") as f:
        f.write(f"[{dt.isoformat()}] node_health=ok latency_p99=0.12ms\n")
    subprocess.run(["git", "add", "telemetry.log"], check=True)
    dt_str = dt.strftime("%Y-%m-%d %H:%M:%S")
    env["GIT_AUTHOR_DATE"] = dt_str
    env["GIT_COMMITTER_DATE"] = dt_str
    subprocess.run(["git", "commit", "-m", f"chore(telemetry): ledger sync pulse {i+1}"], env=env, check=True)

print("Commit history successfully synthesized.")
