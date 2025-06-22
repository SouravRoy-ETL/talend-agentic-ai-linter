from colorama import init, Fore, Style

init(autoreset=True)

def print_job_start(job_name: str):
    print(Fore.MAGENTA + f"\n🔍 Starting scan: {job_name}")
    print(Fore.MAGENTA + "-" * (len(job_name) + 20))

def print_rule_status(rule_id: str, title: str, suggestion: str, status: str):
    print(Fore.CYAN + f"\n📌 Rule {rule_id}: {title}")
    suggestion_text = f"[LLM fallback suggestion] {suggestion.strip()}"

    if status == "resolved":
        print(Fore.GREEN + f"✅ FIXED: {suggestion_text}")
    elif status == "skipped":
        print(Fore.YELLOW + f"⏭️ SKIPPED: {suggestion_text}")
    elif status == "unresolved":
        print(Fore.RED + f"⚠️ UNRESOLVED: {suggestion_text}")
    else:
        print(Fore.WHITE + f"ℹ️ UNKNOWN STATUS: {suggestion_text}")

def print_job_end(job_name: str, fixed: int, unresolved: int, skipped: int):
    print(Fore.MAGENTA + "-" * (len(job_name) + 20))
    print(Fore.GREEN + f"🎉 Completed: {job_name}")
    print(Fore.CYAN + f"🧾 Summary: {fixed} fixed, {unresolved} unresolved, {skipped} skipped.\n")
