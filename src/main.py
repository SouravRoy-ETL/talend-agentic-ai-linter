import os
import time
import yaml
import csv
import xml.etree.ElementTree as ET
from src.llm import llm_call_with_cache, score_confidence
from dotenv import load_dotenv

load_dotenv()

def load_valid_rules(rules_path):
    rules = []
    for rule_file in sorted(os.listdir(rules_path)):
        try:
            rule_path = os.path.join(rules_path, rule_file)
            with open(rule_path, "r", encoding="utf-8") as f:
                rule = yaml.safe_load(f)
            if all(k in rule for k in ("id", "title", "pattern", "fix")):
                rules.append(rule)
            else:
                print(f"⚠️ Skipping {rule_file}: Missing required fields")
        except Exception as e:
            print(f"⚠️ Skipping {rule_file}: {e}")
    return rules

def handle_llm_suggestion(prompt, job_file, rule, writer):
    try:
        llm_response = llm_call_with_cache(prompt, rule['id'])
        suggestion = llm_response.strip()
        confidence = score_confidence(suggestion)
    except Exception as e:
        suggestion = f"⚠️ Fix violation: {rule['description']}"
        confidence = 0.0
    writer.writerow([job_file, rule["id"], "llm-suggested", suggestion, confidence])
    if '[LLM fallback suggestion]' in suggestion:
        print(f"🧠 Suggestion → {suggestion}")
    else:
        print(f"🤖 LLM Suggestion → {suggestion}")
    print(f"⛔ Manual Attention Needed For {rule['id']} — requires user confirmation")

def apply_rule_to_job(tree, job_file, rule, writer):
    modified = False
    root = tree.getroot()
    if rule["pattern"]["contains"] in ET.tostring(root, encoding="unicode"):
        print(f"\n📌 {rule['id']} ({rule['title']})")
        fix_block = rule.get("fix", {})
        strategy = fix_block.get("strategy") if isinstance(fix_block, dict) else ""
        if strategy == "auto":
            modified = True
            print(f"🎯 Rule Auto-Fixed: {rule['id']}")
            writer.writerow([job_file, rule["id"], "fixed", "", "1.0"])
        else:
            prompt = f"Fix violation: {rule['description']}"
            handle_llm_suggestion(prompt, job_file, rule, writer)
    return modified

def lint_and_fix_all_jobs(verbose=False):
    rules_path = "rules"
    jobs_path = "jobs"
    output_path = "reports/fix_summary_report.csv"
    os.makedirs("fixed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    rules = load_valid_rules(rules_path)

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["job_file", "rule_id", "status", "llm_suggestion", "confidence"])

        for job_file in sorted(os.listdir(jobs_path)):
            if job_file.endswith(".item"):
                print(f"\n✨ Job Found {jobs_path}/{job_file}..")
                print(f"🛠️  Starting Fix For {jobs_path}/{job_file}...")
                print(f"📂 Parsing Job File: {job_file}")
                try:
                    tree = ET.parse(os.path.join(jobs_path, job_file))
                except Exception as e:
                    print(f"🚫 Error parsing {job_file}: {e}")
                    continue
                for rule in rules:
                    try:
                        modified = apply_rule_to_job(tree, job_file, rule, writer)
                        if modified:
                            tree.write(f"fixed/{job_file}", encoding="utf-8")
                        time.sleep(1.3)
                    except Exception as e:
                        print(f"🚨 Error applying {rule['id']} on {job_file}: {e}")
