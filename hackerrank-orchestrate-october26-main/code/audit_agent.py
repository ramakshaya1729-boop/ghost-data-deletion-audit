import json
from pathlib import Path

print("--- DETAILED GHOST DATA AUDIT ---")

project_root = Path(r"C:\Users\ramak\Downloads\hackerrank-orchestrate-october26-main\hackerrank-orchestrate-october26-main")
handover_file = next(project_root.glob("**/customer_account_handover_20261001.txt"), None)

if not handover_file:
    print("[ERROR] Handover file not found.")
    exit()

with open(handover_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

not_found_users = set()
all_records = []

for line in lines:
    if "|" not in line:
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) >= 6:
        timestamp, service, record_id, record_type, status, identifier = parts
        
        # Collect NOT_FOUND user emails from account_service
        if service == "account_service" and status == "NOT_FOUND":
            not_found_users.add(identifier.lower())
            
        all_records.append((service, record_id, status, identifier))

print(f"\n[INFO] NOT_FOUND Users (Target Ghost Candidates):")
for u in not_found_users:
    print(f"  - {u}")

print(f"\n[INFO] Checking all records across downstream services:")
ghost_count = 0
for service, record_id, status, identifier in all_records:
    if service != "account_service":
        # Check if identifier matches any deleted user or if status indicates residual data
        if identifier.lower() in not_found_users:
            print(f"  [FOUND GHOST!] Service: {service} | ID: {record_id} | Status: {status} | Target: {identifier}")
            ghost_count += 1

print(f"\nTotal Ghost Records Detected: {ghost_count}")
print("--- AUDIT COMPLETE ---")