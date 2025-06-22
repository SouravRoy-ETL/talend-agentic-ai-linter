import os
import yaml

def generate_coverage_report(rules_folder: str, report_path: str):
    counts = {"low": 0, "medium": 0, "high": 0, "total": 0}
    for file in os.listdir(rules_folder):
        if file.endswith(".yaml"):
            with open(os.path.join(rules_folder, file), "r", encoding="utf-8") as f:
                rule = yaml.safe_load(f)
                severity = rule.get("severity", "low")
                counts[severity] += 1
                counts["total"] += 1
    with open(report_path, "w", encoding="utf-8") as out:
        for k, v in counts.items():
            out.write(f"{k.upper()}: {v}\n")
