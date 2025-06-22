import yaml
import argparse

def create_rule():
    data = {
        "id": input("Rule ID: "),
        "title": input("Title: "),
        "description": input("Description: "),
        "component": input("Component: "),
        "trigger": {"type": "component", "match": input("Trigger Match: ")},
        "check": {
            "type": "xpath",
            "path": input("XPath Path: "),
            "condition": input("XPath Condition: "),
        },
        "fix": {
            "type": "suggestion",
            "strategy": "llm",
            "hint": input("Fix Hint: "),
        },
        "severity": input("Severity (low/medium/high): "),
    }
    with open(f"rules/{data['id'].lower()}.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False)
    print("✅ Rule saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--new", action="store_true", help="Create new rule")
    args = parser.parse_args()
    if args.new:
        create_rule()
