import hashlib
import json
import os

CACHE_PATH = ".llm_cache.json"

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

def get_llm_cached(prompt: str, call_llm_fn):
    cache = load_cache()
    key = hashlib.md5(prompt.encode("utf-8")).hexdigest()
    if key in cache:
        return cache[key]
    response = call_llm_fn(prompt)
    cache[key] = response
    save_cache(cache)
    return response