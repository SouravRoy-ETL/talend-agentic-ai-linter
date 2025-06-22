# 🧠 Talend AI Code Quality Framework

This project automates detection and fixing of Talend job design issues using YAML-based rules, `.item` job files, and OpenRouter LLMs (GPT-based). It supports zipped jobs, generates CSV reports, and shows beautifully formatted CLI output.

---

## 🎥 Demo Video

[![Watch the Demo](https://img.youtube.com/vi/H0oVfQjiWkk/maxresdefault.jpg)](https://youtu.be/H0oVfQjiWkk)

> See the full agentic Talend LLM quality fixer in action!

## ✅ 50+ Production-Grade Code Quality Checks

This framework supports **50+ scalable, production-level rule checks** tailored for enterprise Talend pipelines.  
These cover:

- 🔐 Context misuse & variable scope
- 🧱 Schema issues, nulls, and defaults
- 🚨 Missing error handling (e.g., tDie, tWarn)
- 🪝 Unused metadata & dead code
- 🌀 Infinite loop detection & unsafe joins
- 🎯 Naming conventions, error propagation, subjob limits, and more

> All rules are YAML-defined and support both `auto` fix and LLM-assisted suggestions.


## 🚀 How to Run

1. **Place your zipped Talend Jobs** into:

```
zipped_jobs/
```

2. **Run the full pipeline (after placing your real zipped Talend jobs inside `zipped_jobs/`):**

```bash
python talend_AgenticAI_SouraV1.py --verbose
```

This will:
- ✅ Validate rule YAMLs
- ✅ Extract `.item` files to `jobs/` from nested zips
- ✅ Lint and optionally auto-fix violations
- ✅ Query LLM for unresolved issues
- ✅ Save results to `fixed/` and `reports/fix_summary_report.csv`

---

## 📁 Project Structure

```
├── talend_AgenticAI_SouraV1.py              # Main orchestrator script
├── extract_items_with_delay.py     # Extracts `.item` files from zipped_jobs/
├── validate_syntax.py              # Checks YAML rule format
├── src/
│   ├── main.py                     # Linting and fixing engine
│   └── llm.py                      # LLM handler via OpenRouter API
├── rules/                          # YAML rules for code quality
├── zipped_jobs/                    # Input zipped Talend exports
├── jobs/                           # Extracted .item files
├── fixed/                          # Auto-fixed jobs
└── reports/
    └── fix_summary_report.csv      # CSV summary
```

---

## 🤖 LLM Integration

- **Provider:** OpenRouter.ai
- **Model:** GPT-3.5-Turbo
- **Prompt Example:**  
  `"Fix violation: {rule description}"`
- **Fallback:** Printed clearly in CLI if LLM fails
- **Confidence Score:** Low/Medium/High based on length

---

## 📦 .item Job Extraction Logic

- Looks inside each `zipped_jobs/*.zip`
- Recursively searches folders for `process/` directory
- Copies `.item` files to `jobs/`
- Adds delay of 1.1s per extraction
- Logs each job as:
  ```
  ✅ Extracted job: myJob_0.1.item
  ```

---

## 📊 CSV Report Format

| job_file      | rule_id | status        | llm_suggestion                            | confidence |
|---------------|---------|----------------|-------------------------------------------|------------|
| myJob.item    | RULE_036 | llm-suggested | Defaults in schema don't match data type | medium     |
| myJob2.item   | RULE_028 | fixed          |                                           | 1.0        |

---

## 🧠 Features

- 💬 GPT suggestions for unresolved issues
- 🛠 Auto-fix for rules with `"strategy: auto"`
- 🔄 Caching of LLM responses
- 🐢 1.1s throttled file extraction
- 📋 Emoji-decorated CLI
- 🧪 YAML rule format validation

---

## 🧰 Requirements

- Python 3.9+
- `pip install -r requirements.txt` with:
  - `openai>=1.0.0`
  - `python-dotenv`
  - `PyYAML`

---

## 💡 Future Ideas

- [ ] Rule-specific enable/disable
- [ ] GUI dashboard for job summaries
- [ ] Email report delivery
- [ ] `.env` setup wizard

---


---


## 🔐 OpenRouter API Key Setup

1. Visit [https://openrouter.ai/](https://openrouter.ai/)
2. Sign in and generate an API key from:  
   [https://openrouter.ai/keys](https://openrouter.ai/keys)
3. Copy the API key (starts with `sk-or-...`)

4. Create a `.env` file in your project root with:
```
OPENROUTER_API_KEY=sk-or-your-key-here
```

5. Make sure `python-dotenv` is installed:
```
pip install python-dotenv
```

This allows `llm.py` to securely load your OpenRouter key at runtime.


---


