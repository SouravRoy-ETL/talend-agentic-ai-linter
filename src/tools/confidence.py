def score_fix_confidence(rule_id: str, llm_response: str) -> float:
    """
    Score the confidence of an LLM-generated fix based on keywords and clarity.
    Returns a float between 0.0 (low confidence) and 1.0 (high confidence).
    """
    keywords = ["replace", "update", "modify", "suggest", "should be", "fix", "solution", "resolved"]
    score = sum(1 for word in keywords if word in llm_response.lower()) / len(keywords)
    if "xml" in llm_response.lower():
        score += 0.1
    return min(round(score, 2), 1.0)
