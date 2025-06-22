import os
import hashlib
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
CACHE_FILE = "llm_cache.json"
model = "gpt-3.5-turbo"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def llm_call_with_cache(prompt: str, rule_id: str = ""):
    cache = load_cache()
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    if prompt_hash in cache:
        return cache[prompt_hash]

    try:
        client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        reply = response.choices[0].message.content
        cache[prompt_hash] = reply
        save_cache(cache)
        return reply
    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        fallback = f"[LLM fallback suggestion] Fix violation: {rule_id or 'unknown'}"
        print(fallback)
        return fallback

def score_confidence(suggestion):
    if not suggestion or suggestion.startswith("⚠️"):
        return "low"
    length = len(suggestion.strip())
    if length > 200:
        return "high"
    elif length > 50:
        return "medium"
    return "low"
